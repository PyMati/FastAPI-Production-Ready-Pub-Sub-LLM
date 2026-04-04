from logging import getLogger

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from config import config

logger = getLogger(__name__)

EXCLUDED_ROUTES = ["/api/auth/login", "/api/auth/register"]
CSRF_REQUIRED_METHODS = {"POST", "PUT", "DELETE", "PATCH"}


class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        if (
            request.url.path in EXCLUDED_ROUTES
            or request.method not in CSRF_REQUIRED_METHODS
        ):
            return await call_next(request)

        session_token = request.headers.get(config.CSRF_HEADER_NAME)
        csrf_token = request.cookies.get(config.CSRF_TOKEN_NAME)
        if not csrf_token:
            return JSONResponse(
                content={"error": "CSRF token missing"},
                status_code=status.HTTP_403_FORBIDDEN,
            )
        elif session_token != csrf_token:
            return JSONResponse(
                content={"error": "Invalid CSRF token"},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        response = await call_next(request)
        return response
