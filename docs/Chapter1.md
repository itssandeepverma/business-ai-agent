# Chapter 1: FastAPI App Overview

## What this app does
- Creates a FastAPI service (`main.py`) with a single router (`api/router.py`).
- Serves a static frontend from `ui/` at `/app`, defaulting to `ui/index.html`.
- Redirects the root path `/` to `/app`.

## Request flow
1) Client hits `/` → redirected to `/app`.
2) `/app` is handled by `StaticFiles`, which serves `ui/index.html` and other assets under `ui/`.
3) API calls from the frontend (e.g., POST `/run-agent`) are routed through `api/router.py`.

## Key Python / FastAPI concepts
- `FastAPI` app instance: central object that registers routes, middleware, and mounts.
- Router composition: `app.include_router(router)` keeps endpoint definitions modular.
- Static file mounting: `app.mount("/app", StaticFiles(..., html=True))` maps URL paths to filesystem assets and serves `index.html` by default.
- Redirect responses: `RedirectResponse("/app")` issues an HTTP redirect to the static frontend.
- ASGI server: `uvicorn.run(..., app="main:app", reload=True)` runs the app with hot reload for development.
- `if __name__ == "__main__":` guard ensures the dev server only starts when running `python main.py`, not when imported.

## Code walkthrough
### main.py
```python
app = FastAPI(title="Business AI Agent", version="1.0.0")

app.include_router(router)  # pulls in API endpoints from api/router.py

app.mount("/app", StaticFiles(directory="ui", html=True), name="ui")
# html=True makes index.html the default when hitting /app or /app/

@app.get("/")
async def root():
    return RedirectResponse("/app")  # push root visitors to the frontend

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app="main:app", reload=True)
```

### api/router.py
```python
router = APIRouter()

@router.post("/run-agent")
async def run_agent(business_task: str = Form(...), tone: str = Form(...), depth: str = Form(...)):
    return "Hello"  # placeholder to be replaced with real agent logic
```
- `APIRouter` lets you group related endpoints and include them into the main app.
- `Form(...)` extracts form fields from `application/x-www-form-urlencoded` or `multipart/form-data` requests.

### config.py (current shape)
```python
load_dotenv()

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY (or CLAUDE_API_KEY) is not set...")

MODEL_NAME = "claude-3-sonnet-20240229"
```
- Uses environment variables for secrets to avoid hardcoding keys.
- Provides a central place for model selection and path definitions.

## How to run (development)
```bash
source venv/bin/activate      # activate your virtualenv
pip install fastapi uvicorn   # install dependencies if needed
python main.py                # or: uvicorn main:app --reload
```

## Notes for next steps
- Replace the placeholder return in `/run-agent` with real business logic.
- Add validation and error handling for incoming form data.
- Consider CORS settings if the frontend will be served from another origin.
