import time

from celery import shared_task

from config import config
from enums import EventKeys
from utils import get_redis_client


@shared_task
def answer_on_message(channel_id: str):
    r = get_redis_client()
    r.xadd(channel_id, {"message": EventKeys.START.value})
    for i in range(20):
        time.sleep(1)
        msg = f"Message {i} from worker"
        print(f"Publishing: {msg}")
        r.xadd(channel_id, {"message": msg})
    r.xadd(channel_id, {"message": EventKeys.END.value})
