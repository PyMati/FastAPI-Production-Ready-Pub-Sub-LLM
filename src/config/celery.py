from celery import Celery

from .config import config

worker_app = Celery(
    config.CELERY_WORKER_NAME,
    backend=config.CELERY_RESULT_BACKEND,
    broker=config.CELERY_BROKER_URL,
)


worker_app.conf.include = ["tasks.chat"]
