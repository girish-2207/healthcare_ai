import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

TRAIN_PATH = "disease/data/Training.csv"
TEST_PATH  = "disease/data/Testing.csv"
MODEL_PATH = "models/disease_model.pkl"
ENC_PATH   = "models/label_encoder.pkl"
SYMP_PATH  = "models/symptom_list.pkl"


def load_and_preprocess():
    train_df = pd.read_csv(TRAIN_PATH)
    test_df  = pd.read_csv(TEST_PATH)

    # drop unnamed columns if any
    train_df = train_df.loc[:, ~train_df.columns.str.contains("^Unnamed")]
    test_df  = test_df.loc[:, ~test_df.columns.str.contains("^Unnamed")]

    # the last column is the label
    label_col = "prognosis"

    # all other columns are symptoms (already binary 0/1)
    symptom_cols = [c for c in train_df.columns if c != label_col]
    symptom_list = symptom_cols

    X_train = train_df[symptom_cols].values
    X_test  = test_df[symptom_cols].values

    le = LabelEncoder()
    le.fit(pd.concat([train_df[label_col], test_df[label_col]]))

    y_train = le.transform(train_df[label_col])
    y_test  = le.transform(test_df[label_col])

    return X_train, X_test, y_train, y_test, le, symptom_list


def train():
    os.makedirs("models", exist_ok=True)
    print("[DiseaseTrain] Loading data...")
    X_train, X_test, y_train, y_test, le, symptom_list = load_and_preprocess()
    print(f"[DiseaseTrain] Train size: {len(X_train)}, Test size: {len(X_test)}")
    print(f"[DiseaseTrain] Total symptoms: {len(symptom_list)}")
    print(f"[DiseaseTrain] Total diseases: {len(le.classes_)}")

    print("[DiseaseTrain] Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_acc = accuracy_score(y_test, rf.predict(X_test))
    print(f"[DiseaseTrain] Random Forest Accuracy: {rf_acc:.4f}")

    print("[DiseaseTrain] Training XGBoost...")
    xgb = XGBClassifier(
        n_estimators=100,
        random_state=42,
        eval_metric="mlogloss",
        verbosity=0,
    )
    xgb.fit(X_train, y_train)
    xgb_acc = accuracy_score(y_test, xgb.predict(X_test))
    print(f"[DiseaseTrain] XGBoost Accuracy: {xgb_acc:.4f}")

    # save best model
    best_model = rf if rf_acc >= xgb_acc else xgb
    best_name  = "RandomForest" if rf_acc >= xgb_acc else "XGBoost"
    print(f"[DiseaseTrain] Best model: {best_name}")

    joblib.dump(best_model,   MODEL_PATH)
    joblib.dump(le,           ENC_PATH)
    joblib.dump(symptom_list, SYMP_PATH)
    print("[DiseaseTrain] Models saved to /models")


if __name__ == "__main__":
    train()