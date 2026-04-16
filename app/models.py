from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


LeadType = Literal["portabilidad", "fibra_movil", "solo_movil", "autonomo_pyme"]
PreferredChannel = Literal["llamada", "email", "sms", "whatsapp"]


class LeadCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    phone: str = Field(min_length=9, max_length=20)
    email: Optional[EmailStr] = None
    postal_code: str = Field(min_length=5, max_length=5)
    city: str = Field(min_length=2, max_length=100)
    region: str = Field(min_length=2, max_length=100)
    lead_type: LeadType
    budget_eur: float = Field(gt=0, le=300)
    wants_portability: bool = False
    preferred_channel: PreferredChannel = "llamada"
    best_time_slot: Literal["manana", "tarde", "noche"] = "tarde"
    has_confirmed_coverage: bool = False
    gdpr_consent: bool
    source: Literal["meta_ads", "web", "referido", "organico"]

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 9:
            raise ValueError("El teléfono debe tener al menos 9 dígitos")
        return value


class LeadRecord(LeadCreate):
    id: int
    score: int
    priority: Literal["alta", "media", "baja"]
    assigned_action: str
    created_at: datetime


class HealthResponse(BaseModel):
    status: str
    app: str
