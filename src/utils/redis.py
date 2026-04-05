from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from config import config


def get_redis_client(
    host: str = config.REDIS_HOST,
    port: int = config.REDIS_PORT,
    db: int = config.REDIS_DB,
    async_: bool = False,
) -> Redis | AsyncRedis:
    if async_:
        return AsyncRedis(host=host, port=port, db=db)
    return Redis(host=host, port=port, db=db)
