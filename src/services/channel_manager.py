from uuid import uuid4
from typing import Literal
from enums import ChannelKeys

CHANNEL_TYPES = Literal["chat"]


class ChannelManager:
    @staticmethod
    def create_new_channel(channel_type: CHANNEL_TYPES) -> str:
        match channel_type:
            case "chat":
                return str(f"{ChannelKeys.MESSAGE.value}_{uuid4()}")
