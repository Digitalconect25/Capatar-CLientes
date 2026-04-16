import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.automation import assign_action
from app.models import HealthResponse, LeadCreate, LeadRecord
from app.scoring import lead_priority, score_lead
from data.storage import LeadStorage

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "VibeMovil Lead Engine")
DB_PATH = os.getenv("DB_PATH", "data/leads.db")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

app = FastAPI(title=APP_NAME, version="1.0.0")
storage = LeadStorage(DB_PATH)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_INDEX = BASE_DIR / "frontend" / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=APP_NAME)


@app.get("/", include_in_schema=False)
def preview_ui() -> FileResponse:
    if not FRONTEND_INDEX.exists():
        raise HTTPException(status_code=404, detail="Vista previa no encontrada")
    return FileResponse(FRONTEND_INDEX)


@app.post("/leads", response_model=LeadRecord, status_code=201)
def create_lead(lead: LeadCreate) -> LeadRecord:
    if not lead.gdpr_consent:
        raise HTTPException(status_code=400, detail="Consentimiento GDPR obligatorio")

    score = score_lead(lead)
    priority = lead_priority(score)
    action = assign_action(lead, score)
    record = storage.insert_lead(lead, score, priority, action)
    return record


@app.get("/leads", response_model=list[LeadRecord])
def get_leads(limit: int = Query(default=50, ge=1, le=500)) -> list[LeadRecord]:
    return storage.list_leads(limit=limit)
