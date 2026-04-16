from app.models import LeadCreate


def score_lead(lead: LeadCreate) -> int:
    score = 0

    if lead.source == "meta_ads":
        score += 20
    elif lead.source == "referido":
        score += 30
    else:
        score += 10

    if lead.wants_portability:
        score += 40

    if lead.has_confirmed_coverage:
        score += 25

    if lead.best_time_slot in {"manana", "tarde"}:
        score += 15
    else:
        score += 5

    if 20 <= lead.budget_eur <= 60:
        score += 20
    elif lead.budget_eur > 60:
        score += 10

    if lead.lead_type == "fibra_movil":
        score += 15
    elif lead.lead_type == "autonomo_pyme":
        score += 20

    return min(score, 100)


def lead_priority(score: int) -> str:
    if score >= 75:
        return "alta"
    if score >= 45:
        return "media"
    return "baja"
