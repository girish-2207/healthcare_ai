import sqlite3
import os

DB_PATH = "database/medical.db"

MEDICINE_DATA = [
    ("Typhoid",   "Ciprofloxacin", "500mg twice daily for 10 days",  "Nausea, diarrhea, dizziness"),
    ("Typhoid",   "Azithromycin",  "500mg once daily for 7 days",    "Nausea, abdominal pain"),
    ("Diabetes",  "Metformin",     "500mg twice daily with meals",    "Nausea, stomach upset"),
    ("Diabetes",  "Insulin",       "As prescribed by doctor",         "Hypoglycemia, weight gain"),
    ("Pneumonia", "Amoxicillin",   "500mg three times daily",         "Rash, diarrhea, nausea"),
    ("Pneumonia", "Azithromycin",  "500mg once daily for 5 days",    "Nausea, abdominal pain"),
    ("Malaria",   "Chloroquine",   "As prescribed by doctor",         "Headache, nausea, vomiting"),
    ("Malaria",   "Artemether",    "As prescribed by doctor",         "Dizziness, nausea"),
    ("Tuberculosis", "Isoniazid",  "300mg once daily",                "Liver toxicity, nausea"),
    ("Tuberculosis", "Rifampicin", "600mg once daily",                "Orange urine, liver toxicity"),
]


class MedicineRecommender:
    def __init__(self):
        self._init_db()
        self._seed_data()
        print("[MedicineRecommender] Ready")

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                disease      TEXT NOT NULL,
                medicine     TEXT NOT NULL,
                dosage       TEXT NOT NULL,
                side_effects TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _seed_data(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicines")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany("""
                INSERT INTO medicines (disease, medicine, dosage, side_effects)
                VALUES (?, ?, ?, ?)
            """, MEDICINE_DATA)
            conn.commit()
            print("[MedicineRecommender] Database seeded with medicine data")
        conn.close()

    def recommend(self, disease: str) -> dict:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT medicine, dosage, side_effects
            FROM medicines
            WHERE LOWER(disease) = LOWER(?)
        """, (disease,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {
                "disease":  disease,
                "medicines": [],
                "message":  "No medicine data found for this disease. Please consult a doctor.",
            }

        medicines = [
            {
                "medicine":     row[0],
                "dosage":       row[1],
                "side_effects": row[2],
            }
            for row in rows
        ]

        print(f"[MedicineRecommender] Found {len(medicines)} medicines for {disease}")
        return {
            "disease":  disease,
            "medicines": medicines,
            "message":  "Always consult a doctor before taking any medication.",
        }