from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Celery
    CELERY_WORKER_NAME: str = "worker"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    # XAI
    XAI_API_KEY: str

    # OPENAI
    OPENAI_API_KEY: str

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Logs
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"

    class Config:
        env_file = ".env"


config = Config()
