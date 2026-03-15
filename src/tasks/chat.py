from celery import shared_task

from ai import Actor
from enums import EventKeys
from utils import get_redis_client


@shared_task
def chat_with_user(channel_id: str, message: str):
    r = get_redis_client()
    r.xadd(channel_id, {"message": EventKeys.START.value})
    actor = Actor()
    for actor_message in actor.stream(message):
        print(f"Publishing: {actor_message}")
        r.xadd(channel_id, {"message": actor_message})
    r.xadd(channel_id, {"message": EventKeys.END.value})
