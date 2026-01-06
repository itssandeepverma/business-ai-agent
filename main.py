from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from api.router import router 


app = FastAPI(title="Business AI Agent", version="1.0.0")

#Include Router
app.include_router(router)

#include Mount
app.mount("/app", StaticFiles(directory="ui", html=True), name="ui")

@app.get("/")
async def root():
    return RedirectResponse("/app")



if __name__ == "__main__":
    print("Starting AI Agent Server")
    print("Visit http://localhost:8000/app to access the application")
    uvicorn.run(host="0.0.0.0", port = 8000, app="main:app", reload=True)