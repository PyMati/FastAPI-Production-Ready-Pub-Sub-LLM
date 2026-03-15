from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health")


@router.get("/check/")
async def health_check():
    return JSONResponse(content={"status": "ok"})
