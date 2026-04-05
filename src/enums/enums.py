from enum import Enum


class RequestStateKeys(str, Enum):
    USER_ID = "user_id"


class ChannelKeys(str, Enum):
    CHAT = "chat"


class EventKeys(str, Enum):
    END = "[END]"
    START = "[START]"
