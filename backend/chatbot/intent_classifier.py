class IntentClassifier:
    INTENT_KEYWORDS = {
        "drug": [
            "medicine", "drug", "tablet", "capsule", "dosage",
            "dose", "medication", "prescription", "side effect", "antibiotic",
        ],
        "disease": [
            "disease", "condition", "diagnosis", "disorder", "infection",
            "syndrome", "illness", "predict", "cause", "treatment", "cure",
        ],
        "symptom": [
            "symptom", "feeling", "pain", "fever", "cough", "headache",
            "vomit", "nausea", "fatigue", "tired", "ache", "rash",
        ],
        "diet": [
            "food", "eat", "diet", "nutrition", "avoid", "drink",
            "meal", "vegetable", "fruit", "supplement",
        ],
    }

    def classify(self, query: str) -> str:
        query_lower = query.lower()
        scores = {intent: 0 for intent in self.INTENT_KEYWORDS}

        for intent, keywords in self.INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in query_lower:
                    scores[intent] += 1

        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return "general"

        print(f"[IntentClassifier] Intent: {best}")
        return best