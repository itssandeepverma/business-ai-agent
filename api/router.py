from fastapi import APIRouter, Form

router = APIRouter()

@router.post("/run-agent")
async def run_agent(
    business_task : str = Form(...),
    tone : str = Form(...),
    depth : str = Form(...)
):
    return "Hello"
