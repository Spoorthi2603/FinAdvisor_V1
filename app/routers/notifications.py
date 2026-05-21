import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.notification_service import notification_hub

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.get("/stream/{user_id}")
async def stream_notifications(user_id: str) -> StreamingResponse:
    async def event_stream():
        while True:
            try:
                message = await asyncio.wait_for(notification_hub.get_queue(user_id).get(), timeout=25)
                yield f"data: {message}\n\n"
            except asyncio.TimeoutError:
                yield ": ping\n\n"
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(1)
                continue

    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(event_stream(), media_type="text/event-stream", headers=headers)
