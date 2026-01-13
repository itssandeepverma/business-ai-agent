import json
import time

from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse

from agent.executor import AgentExecutor

router = APIRouter()


@router.post("/run-agent")
async def run_agent(
    business_task: str = Form(...),
    tone: str = Form(...),
    depth: str = Form(...)
):
    executor = AgentExecutor(tone=tone, depth=depth)

    async def event_stream():
        try:
            async for event in executor.run_extreme(business_task):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as exc:
            error_event = {
                "type": "log",
                "content": {
                    "step": "ERROR",
                    "message": str(exc),
                    "timestamp": time.time()
                }
            }
            yield f"data: {json.dumps(error_event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
