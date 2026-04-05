from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, StreamingResponse

from permissions.auth import is_authenticated
from services import ChannelManager, EventReader
from tasks import chat_with_user

from .models import ChatMessage

router = APIRouter(
    prefix="/chat", tags=["chat"], dependencies=[Depends(is_authenticated)]
)


@router.get("/message/{channel_id}/read")
async def read_response(channel_id: str):
    reader = await EventReader.create(channel_id)
    return StreamingResponse(reader.read_events(), media_type="text/event-stream")


@router.post("/message")
async def send_message(message: ChatMessage):
    new_channel_id = ChannelManager.create_new_channel_id("chat")
    chat_with_user.delay(new_channel_id, message.content)
    return JSONResponse(
        content={"channel_id": new_channel_id}, status_code=status.HTTP_200_OK
    )
