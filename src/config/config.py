from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # JWT Token settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 10_080  # 7 days

    # Cookie settings
    ACCESS_COOKIE_NAME: str = "access"
    REFRESH_COOKIE_NAME: str = "refresh"
    COOKIE_DOMAIN: str = "localhost"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    # CSRF Cookie settings
    CSRF_TOKEN_NAME: str = "csrf_token"
    CSRF_COOKIE_EXPIRE_MINUTES: int = JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    CSRF_HEADER_NAME: str = "X-CSRF-Token"

    # CORS settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Celery
    CELERY_WORKER_NAME: str = "worker"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    # XAI
    XAI_API_KEY: str

    # OPENAI
    OPENAI_API_KEY: str

    # Database
    DATABASE_URL: str = (
        "postgresql://your_username:your_password@postgres:5432/your_database"
    )

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
