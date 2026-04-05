from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from database import get_session
from permissions.auth import is_authenticated
from repositories import TokenRepository, UserRepository
from services import CookieService, JwtService
from utils import process_authentication_response, process_refresh_response

from .models import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login_user(
    request: LoginRequest, session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    user_interface = UserRepository(session)
    user = await user_interface.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    return process_authentication_response(user)


@router.post("/register")
async def register_user(
    request: RegisterRequest, session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    user_interface = UserRepository(session)
    try:
        user = await user_interface.create_user(
            request.email, request.password, request.gender
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    return process_authentication_response(user)


@router.post("/logout")
async def logout_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
    _=Depends(is_authenticated),
) -> JSONResponse:
    json_response = JSONResponse(content={"detail": "Logged out"})
    CookieService.delete_cookie(json_response, config.ACCESS_COOKIE_NAME)
    CookieService.delete_cookie(json_response, config.REFRESH_COOKIE_NAME)
    CookieService.delete_cookie(json_response, config.CSRF_TOKEN_NAME)
    refresh = request.cookies.get(config.REFRESH_COOKIE_NAME)
    if refresh is None:
        return json_response
    await TokenRepository(session).blacklist_token(refresh)
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
    session: AsyncSession = Depends(get_session),
    _=Depends(is_authenticated),
) -> JSONResponse:
    refresh_token = request.cookies.get(config.REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )

    token_interface = TokenRepository(session)
    if await token_interface.is_token_blacklisted(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted"
        )

    try:
        user_id = JwtService.verify_token(refresh_token)["user_id"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e

    user_interface = UserRepository(session)
    user = await user_interface.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return process_refresh_response(user_id)
