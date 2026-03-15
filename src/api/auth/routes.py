from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from config import config
from database import get_session
from interfaces import TokenInterface, UserInterface
from services import CookieService, JwtService

from .models import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login_user(
    request: LoginRequest, session: Session = Depends(get_session)
) -> JSONResponse:
    user_interface = UserInterface(session)
    user = user_interface.authenticate_user(request.email, request.password)
    if not user:
        return JSONResponse(
            content={"error": "Invalid email or password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    tokens = JwtService.create_tokens(user.id)
    json_response = JSONResponse(
        content={
            "id": user.id,
            "email": user.email,
            "gender": user.gender,
        }
    )
    CookieService.set_auth_cookies(
        json_response, tokens["access_token"], tokens["refresh_token"]
    )
    return json_response


@router.post("/register")
async def register_user(
    request: RegisterRequest, session: Session = Depends(get_session)
) -> JSONResponse:
    user_interface = UserInterface(session)
    try:
        user = user_interface.create_user(
            request.email, request.password, request.gender
        )
    except IntegrityError:
        return JSONResponse(
            content={"error": "Email already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content={"id": user.id, "email": user.email, "gender": user.gender}
    )


@router.post("/verify")
async def verify_token(request: Request) -> JSONResponse:
    access = request.cookies.get(config.ACCESS_COOKIE_NAME)
    try:
        JwtService.verify_token(access)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_401_UNAUTHORIZED
        )
    return JSONResponse(content={"detail": "Token is valid"})


@router.post("/logout")
async def logout_user(
    request: Request, session: Session = Depends(get_session)
) -> JSONResponse:
    json_response = JSONResponse(content={"detail": "Logged out"})
    CookieService.delete_cookie(json_response, config.ACCESS_COOKIE_NAME)
    CookieService.delete_cookie(json_response, config.REFRESH_COOKIE_NAME)
    refresh = request.cookies.get(config.REFRESH_COOKIE_NAME)
    TokenInterface(session).blacklist_token(refresh)
    return json_response
