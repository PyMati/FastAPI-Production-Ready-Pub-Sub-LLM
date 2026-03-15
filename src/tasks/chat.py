from celery import shared_task

from ai import Actor
from enums import EventKeys
from utils import get_redis_client


@shared_task
def chat_with_user(channel_id: str, message: str):
    r = get_redis_client()
    r.xadd(channel_id, {"message": EventKeys.START.value})
    print(f"Received message: {message}")
    actor = Actor()
    for actor_message in actor.stream(message):
        print(f"Publishing: {actor_message}")
        token, metadata = actor_message["data"]
        print(f"Token: {token.content}, Metadata: {metadata}")
        r.xadd(channel_id, {"message": token.content})
    r.xadd(channel_id, {"message": EventKeys.END.value})
