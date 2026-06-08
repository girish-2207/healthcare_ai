import numpy as np
import joblib
import io
from keras.models import load_model
from PIL import Image

MODEL_PATH   = "models/xray_model.h5"
CLASSES_PATH = "models/xray_classes.pkl"
IMG_SIZE     = (224, 224)


class XrayClassifier:
    def __init__(self):
        print("[XrayClassifier] Loading model...")
        self.model   = load_model(MODEL_PATH)
        self.classes = joblib.load(CLASSES_PATH)
        print(f"[XrayClassifier] Classes: {self.classes}")
        print("[XrayClassifier] Model loaded")

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(IMG_SIZE)
        array = np.array(image) / 255.0
        return np.expand_dims(array, axis=0)

    def classify(self, image_bytes: bytes) -> dict:
        tensor     = self.preprocess(image_bytes)
        prediction = self.model.predict(tensor)[0]
        class_idx  = int(np.argmax(prediction))
        confidence = round(float(prediction[class_idx]) * 100, 2)
        result     = self.classes[class_idx]

        print(f"[XrayClassifier] Result: {result} ({confidence}%)")
        return {
            "result":     result,
            "confidence": confidence,
            "all_scores": {
                self.classes[i]: round(float(prediction[i]) * 100, 2)
                for i in range(len(self.classes))
            },
        }