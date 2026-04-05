import asyncio
from typing import AsyncGenerator

from redis.asyncio import Redis as AsyncRedis

from enums import EventKeys


class EventReader:
    MAX_IDLE_ROUNDS = 12  # 12 * 5s block = 60 s without new events before giving up
    DEFAULT_BLOCK_TIME = 5000  # ms
    DEFAULT_COUNT = 10

    def __init__(self, channel_id: str, last_id: str = "0"):
        self.channel_id = channel_id
        self.last_id = last_id
        self.redis = None

    @classmethod
    def create(cls, channel_id: str, last_id: str = "0") -> "EventReader":
        from utils import get_redis_client

        instance = cls(channel_id, last_id)
        instance.redis = get_redis_client(async_=True)
        return instance

    async def read_events(self) -> AsyncGenerator[str, None]:
        idle_rounds = 0
        self.redis: AsyncRedis

        while idle_rounds < self.MAX_IDLE_ROUNDS:
            entries = await self.redis.xread(
                {self.channel_id: self.last_id},
                block=self.DEFAULT_BLOCK_TIME,
                count=self.DEFAULT_COUNT,
            )

            if not entries:
                idle_rounds += 1
                await asyncio.sleep(0)
                yield "data: EMPTY\n\n"  # Send a heartbeat to keep the connection alive
                continue

            idle_rounds = 0
            for _stream, messages in entries:
                for msg_id, data in messages:
                    self.last_id = msg_id
                    text = data[b"message"].decode("utf-8")

                    if text == EventKeys.END.value:
                        return
                    if text == EventKeys.START.value:
                        continue

                    yield f"data: {text}\n\n"

            await asyncio.sleep(0)
