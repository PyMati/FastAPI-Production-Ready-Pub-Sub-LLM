from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import config
from database import get_session
from interfaces import TokenInterface, UserInterface
from permissions.auth import is_authenticated
from services import CookieService, JwtService
from utils import process_authentication_response, process_refresh_response

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
    return process_authentication_response(user)


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
    return process_authentication_response(user)


@router.post("/logout")
async def logout_user(
    request: Request,
    session: Session = Depends(get_session),
    _=Depends(is_authenticated),
) -> JSONResponse:
    json_response = JSONResponse(content={"detail": "Logged out"})
    CookieService.delete_cookie(json_response, config.ACCESS_COOKIE_NAME)
    CookieService.delete_cookie(json_response, config.REFRESH_COOKIE_NAME)
    CookieService.delete_cookie(json_response, config.CSRF_TOKEN_NAME)
    refresh = request.cookies.get(config.REFRESH_COOKIE_NAME)
    if refresh is None:
        return json_response
    TokenInterface(session).blacklist_token(refresh)
    return json_response


@router.post("/verify")
async def verify_token(
    request: Request,
    _=Depends(is_authenticated),
) -> JSONResponse:
    return JSONResponse(content={"detail": "Token is valid"})


@router.post("/refresh")
async def refresh_token(
    request: Request,
    session: Session = Depends(get_session),
    _=Depends(is_authenticated),
) -> JSONResponse:
    refresh_token = request.cookies.get(config.REFRESH_COOKIE_NAME)
    if not refresh_token:
        return JSONResponse(
            content={"error": "Refresh token missing"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    token_interface = TokenInterface(session)
    if token_interface.is_token_blacklisted(refresh_token):
        return JSONResponse(
            content={"error": "Invalid refresh token"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        user_id = JwtService.verify_token(refresh_token)["user_id"]
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user_interface = UserInterface(session)
    user = user_interface.get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            content={"error": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return process_refresh_response(user_id)
