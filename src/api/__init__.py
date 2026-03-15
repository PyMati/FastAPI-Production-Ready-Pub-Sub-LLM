from .chat import router as chat_router
from .health import router as health_router

routers = [health_router, chat_router]


__all__ = ["routers"]
