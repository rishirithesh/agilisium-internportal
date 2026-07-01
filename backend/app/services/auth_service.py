import re
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AuthenticationError, ConflictError, ValidationError
from app.core.security import (
    TokenType,
    create_token,
    decode_token,
    generate_otp,
    hash_password,
    verify_password,
)
from app.models.user import RefreshToken, User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse
from app.services.audit_service import AuditService
from app.services.email_service import EmailService
from app.models.pre_registration import PreRegistration
from app.repositories.pre_registration_repository import PreRegistrationRepository
from datetime import datetime, timezone


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)
        self.audit = AuditService(db)
        self.email = EmailService(db=self.db)
        self.pre_reg = PreRegistrationRepository(db)

    async def register(self, *, email: str, full_name: str, password: str, role: str) -> User:
        email_clean = email.strip().lower()

        # Simple domain rules enforcement per INSTRUCTIONS.md
        if role in ("EMPLOYEE", "ADMIN", "MAIN_ADMIN"):
            if not email_clean.endswith("@agilisium.com"):
                raise ValidationError("Employee/Admin/Main Admin accounts must use an @agilisium.com email")
        if role == "INTERN":
            if email_clean.endswith("@agilisium.com"):
                raise ValidationError("Intern accounts must NOT use an @agilisium.com email")

        existing = await self.users.get_by_email(email_clean)
        if existing:
            raise ConflictError("A user with this email already exists")

        # Password policy: min 8 chars, uppercase, lowercase, digit, special char
        policy = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9]).{8,}")
        if not policy.match(password):
            raise ValidationError(
                "Password must be at least 8 characters and include uppercase, lowercase, number and special character"
            )

        user = User(
            email=email_clean,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
        )
        user = await self.users.create(user)
        await self.audit.log(actor_id=user.id, action="USER_REGISTERED", resource_type="User", resource_id=str(user.id))
        return user

    async def login_with_password(self, email: str, password: str) -> tuple[User, TokenResponse]:
        user = await self.users.get_by_email(email)
        if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        if not user.is_active:
            raise AuthenticationError("This account has been deactivated")

        user.last_login_at = datetime.now(timezone.utc)
        await self.users.save(user)
        tokens = await self._issue_tokens(user)
        await self.audit.log(actor_id=user.id, action="USER_LOGIN", resource_type="User", resource_id=str(user.id))
        return user, tokens

    async def request_otp(self, email: str) -> None:
        # Support both login OTP (existing user) and registration OTP (pre-registration)
        user = await self.users.get_by_email(email)
        otp = generate_otp()
        expires = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

        if user:
            user.otp_code_hash = hash_password(otp)
            user.otp_expires_at = expires
            await self.users.save(user)
            await self.email.send_otp_email(to_email=user.email, full_name=user.full_name, otp_code=otp)
            return

        # Pre-registration flow: create/update a pre-registration record
        pre = await self.pre_reg.get_by_email(email)
        if pre is None:
            pre = PreRegistration(email=email, otp_hash=hash_password(otp), otp_expires_at=expires, verified=False, attempts=0)
        else:
            pre.otp_hash = hash_password(otp)
            pre.otp_expires_at = expires
            pre.verified = False
            pre.attempts = 0
        await self.pre_reg.create_or_update(pre)
        await self.email.send_otp_email(to_email=email, full_name=email, otp_code=otp)

    async def verify_otp(self, email: str, otp_code: str) -> tuple[User, TokenResponse]:
        # Prefer existing user OTP (login). If not present, check pre-registration
        user = await self.users.get_by_email(email)
        now = datetime.now(timezone.utc)

        if user and user.otp_code_hash and user.otp_expires_at:
            if now > user.otp_expires_at:
                raise AuthenticationError("OTP has expired")
            if not verify_password(otp_code, user.otp_code_hash):
                raise AuthenticationError("Invalid OTP")

            user.otp_code_hash = None
            user.otp_expires_at = None
            user.is_email_verified = True
            user.last_login_at = now
            await self.users.save(user)

            tokens = await self._issue_tokens(user)
            await self.audit.log(actor_id=user.id, action="USER_LOGIN_OTP", resource_type="User", resource_id=str(user.id))
            return user, tokens

        pre = await self.pre_reg.get_by_email(email)
        if pre and pre.otp_hash and pre.otp_expires_at:
            if now > pre.otp_expires_at:
                raise AuthenticationError("OTP has expired")
            if not verify_password(otp_code, pre.otp_hash):
                raise AuthenticationError("Invalid OTP")

            pre.verified = True
            await self.pre_reg.create_or_update(pre)
            # For registration OTP, return no user but indicate success via raising AuthenticationError is not appropriate
            # We'll return (None, None) to signal verified pre-registration; callers should handle creating account next.
            return None, None

        raise AuthenticationError("Invalid or expired OTP")

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except ValueError as exc:
            raise AuthenticationError("Invalid refresh token") from exc

        if payload.get("type") != TokenType.REFRESH.value:
            raise AuthenticationError("Invalid token type")

        jti = payload["jti"]
        from sqlalchemy import select

        result = await self.db.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        stored = result.scalar_one_or_none()
        if not stored or not stored.is_active:
            raise AuthenticationError("Refresh token has been revoked or expired")

        user = await self.users.get_by_id(uuid.UUID(payload["sub"]))
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")

        # Rotate: revoke old, issue new pair.
        stored.revoked_at = datetime.now(timezone.utc)
        await self.db.flush()
        return await self._issue_tokens(user)

    async def _issue_tokens(self, user: User) -> TokenResponse:
        access_token, _ = create_token(subject=str(user.id), role=user.role.value, token_type=TokenType.ACCESS)
        refresh_token, refresh_jti = create_token(
            subject=str(user.id), role=user.role.value, token_type=TokenType.REFRESH
        )

        record = RefreshToken(
            jti=refresh_jti,
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        self.db.add(record)
        await self.db.flush()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
