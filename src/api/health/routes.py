from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .models import HealthCheckResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/check", response_model=HealthCheckResponse)
async def health_check():
    return JSONResponse(content=HealthCheckResponse().model_dump())
