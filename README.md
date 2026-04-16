# VibeMovil Lead Engine (España)

Sistema completo (MVP funcional) para captación y gestión automática de leads para telecom en España, con enfoque RGPD y operación comercial rápida.

## Qué incluye

- API para capturar leads desde Meta Ads, web o referidos.
- Scoring automático de prioridad.
- Acción comercial recomendada automáticamente.
- Persistencia en SQLite.
- Endpoints para listar y operar leads.

## Arquitectura

1. **Adquisición**: Meta Ads / Web / Referidos.
2. **Captura**: endpoint `POST /leads`.
3. **Validación**: datos mínimos + consentimiento RGPD obligatorio.
4. **Scoring**: puntaje 0-100 para prioridad comercial.
5. **Orquestación**: acción automática sugerida (llamada/email/sms).
6. **Almacenamiento**: base local SQLite (`data/leads.db`).

## Requisitos

- Python 3.11+

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Ejecución

```bash
uvicorn app.main:app --reload --port 8000
```

## Ejemplo de creación de lead

```bash
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Laura García",
    "phone": "+34 612345678",
    "email": "laura@example.com",
    "postal_code": "28001",
    "city": "Madrid",
    "region": "Madrid",
    "lead_type": "fibra_movil",
    "budget_eur": 45,
    "wants_portability": true,
    "preferred_channel": "llamada",
    "best_time_slot": "tarde",
    "has_confirmed_coverage": true,
    "gdpr_consent": true,
    "source": "meta_ads"
  }'
```

## Endpoints

- `GET /health`: estado del servicio.
- `POST /leads`: crea lead y ejecuta scoring/acción automática.
- `GET /leads?limit=50`: lista leads recientes.

## Próximos pasos recomendados

- Integrar CRM (HubSpot/Zoho) vía webhook.
- Añadir autenticación (API key/JWT).
- Automatizar campañas y seguimiento con n8n/Make.
- Crear panel de métricas (CPL, contactabilidad, conversión).


## Vista previa rápida (UI demo)

Abre `frontend/index.html` en tu navegador para ver una maqueta funcional de captura y listado de leads.

1. Levanta la API:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
2. Abre la UI servida por FastAPI en:
   - `http://localhost:8000/`
3. (Opcional) También puedes abrir `frontend/index.html` de forma manual.
4. Verifica que `API Base URL` sea `http://localhost:8000` y crea leads reales desde la vista.

## Despliegue en GitHub

Este repositorio ya incluye automatización para CI y despliegue:

- **CI** (`.github/workflows/ci.yml`): instala dependencias, ejecuta tests y valida build Docker.
- **Deploy API** (`.github/workflows/deploy-ghcr.yml`): publica imagen Docker en GHCR al hacer push a `main`.
- **Deploy Frontend** (`.github/workflows/deploy-pages.yml`): publica `frontend/` en GitHub Pages.

### Pasos para activar el despliegue

1. Sube el repositorio a GitHub y configura la rama por defecto como `main`.
2. En **Settings → Pages**, selecciona **GitHub Actions** como source.
3. Haz push a `main`:
   - Se ejecutará CI automáticamente.
   - Se publicará la imagen API en `ghcr.io/<tu-org-o-usuario>/vibemovil-lead-engine`.
   - Se desplegará la vista previa frontend en GitHub Pages.

### Ejecutar contenedor publicado (API)

```bash
docker run -p 8000:8000 \
  -e DB_PATH=data/leads.db \
  ghcr.io/<tu-org-o-usuario>/vibemovil-lead-engine:latest
```
