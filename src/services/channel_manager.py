from typing import Literal
from uuid import uuid4

from enums import ChannelKeys

CHANNEL_TYPES = Literal["chat"]


class ChannelManager:
    @staticmethod
    def create_new_channel_id(channel_type: CHANNEL_TYPES) -> str:
        match channel_type:
            case "chat":
                return str(f"{ChannelKeys.CHAT.value}_{uuid4()}")
