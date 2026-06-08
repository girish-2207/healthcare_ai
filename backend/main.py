import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv

from chatbot   import MedicalChatbot
from disease   import DiseasePredictor
from medicine  import MedicineRecommender
from xray      import XrayClassifier

load_dotenv()

app = FastAPI(title="Healthcare AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# load all modules once at startup
chatbot    = MedicalChatbot(
    docs_dir="medical_docs",
    index_path="vector_store/faiss_index",
    db_path="database/medical.db",
    llm_model="llama-3.1-8b-instant",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    rebuild_index=False,
)
predictor   = DiseasePredictor()
recommender = MedicineRecommender()
classifier  = XrayClassifier()

# ── request models ──
class ChatRequest(BaseModel):
    user_id: str
    query: str
    external_context: Optional[dict] = None

class ResetRequest(BaseModel):
    user_id: str

class PredictRequest(BaseModel):
    symptoms: List[str]

# ── chatbot routes ──
@app.post("/chat")
def chat(req: ChatRequest):
    return chatbot.chat(req.user_id, req.query, req.external_context)

@app.post("/chat/reset")
def reset(req: ResetRequest):
    return chatbot.reset(req.user_id)

@app.get("/chat/history/{user_id}")
def history(user_id: str):
    return {"history": chatbot.history.get(user_id, last_n=20)}

# ── disease prediction routes ──
@app.post("/predict/disease")
def predict_disease(req: PredictRequest):
    return predictor.predict(req.symptoms)

@app.get("/predict/symptoms")
def get_symptoms():
    return {"symptoms": predictor.get_symptom_list()}

# ── medicine routes ──
@app.get("/medicine/{disease}")
def get_medicine(disease: str):
    return recommender.recommend(disease)

# ── xray routes ──
@app.post("/predict/xray")
async def predict_xray(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return classifier.classify(image_bytes)

# ── health check ──
@app.get("/health")
def health():
    return {"status": "ok"}