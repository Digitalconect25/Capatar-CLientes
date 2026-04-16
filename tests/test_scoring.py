from app.models import LeadCreate
from app.scoring import lead_priority, score_lead


def base_lead(**overrides):
    payload = {
        "full_name": "Cliente Test",
        "phone": "+34 600000000",
        "email": "test@example.com",
        "postal_code": "08001",
        "city": "Barcelona",
        "region": "Cataluña",
        "lead_type": "fibra_movil",
        "budget_eur": 50,
        "wants_portability": True,
        "preferred_channel": "llamada",
        "best_time_slot": "tarde",
        "has_confirmed_coverage": True,
        "gdpr_consent": True,
        "source": "meta_ads",
    }
    payload.update(overrides)
    return LeadCreate(**payload)


def test_score_high_priority():
    lead = base_lead()
    score = score_lead(lead)
    assert score >= 75
    assert lead_priority(score) == "alta"


def test_score_low_priority():
    lead = base_lead(
        source="web",
        wants_portability=False,
        has_confirmed_coverage=False,
        budget_eur=10,
        lead_type="solo_movil",
        best_time_slot="noche",
    )
    score = score_lead(lead)
    assert score < 45
    assert lead_priority(score) == "baja"
