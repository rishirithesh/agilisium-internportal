from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import AIRPException
from app.models.user import User
from app.schemas.auth import (
    CurrentUser,
    LoginRequest,
    OtpRequestSchema,
    OtpVerifySchema,
    RefreshRequest,
    TokenResponse,
    RegisterRequest,
)
from app.services.auth_service import AuthService
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        _, tokens = await AuthService(db).login_with_password(payload.email, payload.password)
        return tokens
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.post("/otp/request", status_code=204)
async def request_otp(payload: OtpRequestSchema, db: AsyncSession = Depends(get_db)) -> None:
    await AuthService(db).request_otp(payload.email)


@router.post("/otp/verify", response_model=TokenResponse)
async def verify_otp(payload: OtpVerifySchema, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        user, tokens = await AuthService(db).verify_otp(payload.email, payload.otp_code)
        if user is None and tokens is None:
            # Pre-registration OTP verified; return 204 to indicate next step (create account)
            from fastapi import Response

            return Response(status_code=204)
        return tokens
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        # Ensure pre-registration verified for non-admin/employee flows when appropriate
        from app.repositories.pre_registration_repository import PreRegistrationRepository

        pre_repo = PreRegistrationRepository(db)
        pre = await pre_repo.get_by_email(str(payload.email).lower())
        if not pre or not pre.verified:
            raise AIRPException("Email not verified via OTP. Please request and verify OTP before creating account.")

        user = await AuthService(db).register(email=payload.email, full_name=payload.full_name, password=payload.password, role=payload.role)
        # Clean up pre-registration
        await pre_repo.delete(pre)
        _, tokens = await AuthService(db).login_with_password(payload.email, payload.password)
        return tokens
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        return await AuthService(db).refresh_access_token(payload.refresh_token)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.get("/me", response_model=CurrentUser)
async def me(user: User = Depends(get_current_user)) -> CurrentUser:
    return CurrentUser.model_validate(user)
