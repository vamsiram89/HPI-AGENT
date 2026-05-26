# HPI AI

End-to-end Human Potential Identifier app with:

- Streamlit frontend dashboard
- FastAPI backend
- Tool-using AI agent endpoint
- Optional OpenAI LLM upgrade when `OPENAI_API_KEY` is configured
- Deterministic fallback agent so the app works without paid API access

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run Backend

```powershell
.\scripts\start_backend.ps1
```

Health check:

```powershell
curl http://127.0.0.1:8010/health
```

## Run Frontend

Open a second terminal:

```powershell
.\scripts\start_frontend.ps1
```

The frontend reads `HPI_API_URL`, defaulting to:

```text
http://127.0.0.1:8010/api/dashboard
```

## Optional LLM Mode

Set an API key before starting the backend:

```powershell
$env:OPENAI_API_KEY="your_api_key"
$env:OPENAI_MODEL="gpt-4.1-mini"
.\scripts\start_backend.ps1
```

Without `OPENAI_API_KEY`, the backend still returns useful agent responses using local career-analysis tools.
