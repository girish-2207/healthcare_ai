import os
import joblib
import tensorflow as tf
from keras.applications import MobileNetV2
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras.models import Model
from keras.callbacks import ModelCheckpoint, EarlyStopping

DATA_DIR   = "xray/data"
MODEL_PATH = "models/xray_model.h5"
IMG_SIZE   = (224, 224)
BATCH_SIZE = 32
EPOCHS     = 10


def build_model(num_classes: int):
    base = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False

    x      = base.output
    x      = GlobalAveragePooling2D()(x)
    x      = Dropout(0.3)(x)
    x      = Dense(128, activation="relu")(x)
    x      = Dropout(0.2)(x)
    output = Dense(num_classes, activation="softmax")(x)

    return Model(inputs=base.input, outputs=output)


def train():
    os.makedirs("models", exist_ok=True)

    # use tf.keras.utils instead of ImageDataGenerator
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        os.path.join(DATA_DIR, "train"),
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )
    test_dataset = tf.keras.utils.image_dataset_from_directory(
        os.path.join(DATA_DIR, "test"),
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )

    class_names = train_dataset.class_names
    num_classes = len(class_names)
    print(f"[XrayTrain] Classes found: {class_names}")

    joblib.dump(class_names, "models/xray_classes.pkl")

    # normalize pixel values
    normalization = tf.keras.layers.Rescaling(1.0 / 255)
    train_dataset = train_dataset.map(lambda x, y: (normalization(x), y))
    test_dataset  = test_dataset.map(lambda x, y: (normalization(x), y))

    # performance optimization
    train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
    test_dataset  = test_dataset.prefetch(tf.data.AUTOTUNE)

    model = build_model(num_classes)
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor="val_accuracy"),
        EarlyStopping(patience=3, restore_best_weights=True),
    ]

    print("[XrayTrain] Training started...")
    model.fit(
        train_dataset,
        validation_data=test_dataset,
        epochs=EPOCHS,
        callbacks=callbacks,
    )
    print(f"[XrayTrain] Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()