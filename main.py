from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn


app = FastAPI(title="Business AI Agent", version="1.0.0")

@app.get("/")
async def root():
    return RedirectResponse("/app")


if __name__ == "main":
    print("Starting AI Agent Server")
    print("Visit http://localhost:8000/app to access the application")
    uvicorn.run(host="0.0.0.0", port = 8000, app="main:app", reload=True)