from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from database import get_session
from interfaces import UserInterface

from .models import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login_user(request: LoginRequest) -> JSONResponse:
    pass


@router.post("/register")
async def register_user(
    request: RegisterRequest, session: Session = Depends(get_session)
) -> JSONResponse:
    user_interface = UserInterface(session)
    try:
        user = user_interface.create_user(
            email=request.email, password=request.password, gender=request.gender
        )
    except IntegrityError:
        return JSONResponse(
            content={"error": "Email already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content={"id": user.id, "email": user.email, "gender": user.gender}
    )
