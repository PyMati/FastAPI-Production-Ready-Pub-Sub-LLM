from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse

from services import ChannelManager, EventReader
from tasks import answer_on_message

router = APIRouter(prefix="/chat")


@router.get("/message/{channel_id}/read")
async def read_response(channel_id: str):
    reader = EventReader(channel_id)
    return StreamingResponse(reader.read_events(), media_type="text/event-stream")


@router.post("/message")
async def send_message():
    new_channel_id = ChannelManager.create_new_channel("chat")
    answer_on_message.delay(new_channel_id)
    return JSONResponse(
        content={"channel_id": new_channel_id}, status_code=HTTPStatus.CREATED
    )
