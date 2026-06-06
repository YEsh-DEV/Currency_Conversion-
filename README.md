Currency Conversion (Backend)

This repository contains a scaffold for a currency-conversion backend using Python + FastAPI.

Quick start (PowerShell):

```powershell
# create virtual env and install
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
# set environment variables from .env or set them manually
# recommended: copy .env.example -> .env and fill keys
uvicorn backend.app:app --reload --port 8001
```

Docker (dev):

```powershell
docker build -t currency-conv:dev .
docker run --rm -p 8001:8000 --env-file .env currency-conv:dev
```

API endpoints:
- `GET /health` - simple health check
- `POST /convert` - convert payload (see `backend/schemas.py`)

Notes:
- The Agent currently is a deterministic stub. It will be replaced with a LangChain + Gemini integration.
- Do not commit real API keys. Use `.env.example` as a template.
