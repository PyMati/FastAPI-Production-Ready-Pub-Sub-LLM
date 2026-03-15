from redis import Redis
from config import config


def get_redis_client(
    host: str = config.REDIS_HOST,
    port: int = config.REDIS_PORT,
    db: int = config.REDIS_DB,
) -> Redis:
    return Redis(host=host, port=port, db=db)
