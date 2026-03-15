from enum import Enum


class ChannelKeys(str, Enum):
    MESSAGE = "message"


class EventKeys(str, Enum):
    END = "[END]"
    START = "[START]"
