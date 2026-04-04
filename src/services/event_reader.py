import asyncio
from typing import AsyncGenerator

from enums import EventKeys


class EventReader:
    MAX_IDLE_ROUNDS = 12  # 12 * 5s block = 60s bez danych → koniec
    DEFAULT_BLOCK_TIME = 5000  # ms
    DEFAULT_COUNT = 10

    def __init__(self, channel_id: str, last_id: str = "0"):
        from utils import get_redis_client

        self.channel_id = channel_id
        self.last_id = last_id
        self.redis = get_redis_client()

    async def read_events(self) -> AsyncGenerator[str, None]:
        idle_rounds = 0

        while idle_rounds < self.MAX_IDLE_ROUNDS:
            entries = self.redis.xread(
                {self.channel_id: self.last_id},
                block=self.DEFAULT_BLOCK_TIME,
                count=self.DEFAULT_COUNT,
            )

            if not entries:
                idle_rounds += 1
                await asyncio.sleep(0)
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
