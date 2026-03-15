from .auth import router as auth_router
from .chat import router as chat_router
from .health import router as health_router

routers = [auth_router, chat_router, health_router]


__all__ = ["routers"]
