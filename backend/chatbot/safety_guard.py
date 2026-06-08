class SafetyGuard:
    EMERGENCY_KEYWORDS = [
        "chest pain", "can't breathe", "cannot breathe",
        "unconscious", "overdose", "heart attack", "stroke",
        "severe bleeding", "not breathing", "suicidal",
    ]

    DISCLAIMER = (
        "\n\n⚠️ Disclaimer: This is AI-generated information for educational "
        "purposes only. Please consult a licensed healthcare professional "
        "for personal medical advice."
    )

    def is_emergency(self, query: str) -> bool:
        q = query.lower()
        return any(kw in q for kw in self.EMERGENCY_KEYWORDS)

    def emergency_response(self) -> str:
        return (
            "🚨 This sounds like a medical emergency. "
            "Please call emergency services (108 / 112) immediately "
            "or go to the nearest hospital. Do not wait."
        )

    def add_disclaimer(self, response: str) -> str:
        disclaimer = "⚠️ Disclaimer: This is AI-generated information for educational purposes only. Please consult a licensed healthcare professional for personal medical advice."
        if "Disclaimer" not in response:
            return response + "\n\n" + disclaimer
        return response