import joblib
import numpy as np

MODEL_PATH = "models/disease_model.pkl"
ENC_PATH   = "models/label_encoder.pkl"
SYMP_PATH  = "models/symptom_list.pkl"


class DiseasePredictor:
    def __init__(self):
        print("[DiseasePredictor] Loading model...")
        self.model        = joblib.load(MODEL_PATH)
        self.encoder      = joblib.load(ENC_PATH)
        self.symptom_list = joblib.load(SYMP_PATH)
        print("[DiseasePredictor] Model loaded")

    def get_symptom_list(self):
        return self.symptom_list

    def predict(self, symptoms: list) -> dict:
        # encode input symptoms as binary vector
        symptoms_clean = [s.strip().lower() for s in symptoms]
        vector = [
            1 if s.lower() in symptoms_clean else 0
            for s in self.symptom_list
        ]
        vector = np.array(vector).reshape(1, -1)

        # get top 3 predictions with confidence
        probabilities = self.model.predict_proba(vector)[0]
        top3_indices  = np.argsort(probabilities)[::-1][:3]

        predictions = []
        for idx in top3_indices:
            predictions.append({
                "disease":    self.encoder.inverse_transform([idx])[0],
                "confidence": round(float(probabilities[idx]) * 100, 2),
            })

        print(f"[DiseasePredictor] Top prediction: {predictions[0]}")
        return {
            "predictions": predictions,
            "symptoms_received": symptoms,
        }