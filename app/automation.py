from app.models import LeadCreate


def assign_action(lead: LeadCreate, score: int) -> str:
    """Define la acción automática para equipos comerciales en España (UE compliant)."""
    if score >= 75:
        return "Llamar en <5 min y enviar email de oferta personalizada"

    if lead.preferred_channel == "sms":
        return "Enviar SMS de confirmación y programar llamada en 30 min"

    if lead.preferred_channel == "email":
        return "Enviar email con planes y activar recordatorio de llamada"

    # WhatsApp se deja como secundario para no depender del canal en UE.
    if lead.preferred_channel == "whatsapp":
        return "Enviar email + SMS y pedir autorización explícita antes de WhatsApp"

    return "Programar llamada comercial en la franja horaria seleccionada"
