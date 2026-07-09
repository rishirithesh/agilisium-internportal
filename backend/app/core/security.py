<<<<<<< HEAD
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_otp(length: int = 6) -> str:
    """Cryptographically secure numeric OTP, e.g. for intern/employee login."""
    return "".join(secrets.choice("0123456789") for _ in range(length))


def create_token(
    *, subject: str, role: str, token_type: TokenType, extra_claims: dict[str, Any] | None = None
) -> tuple[str, str]:
    """Returns (encoded_jwt, jti). jti is persisted for refresh-token revocation."""
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())

    if token_type == TokenType.ACCESS:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": subject,
        "role": role,
        "type": token_type.value,
        "jti": jti,
        "iat": now,
        "exp": expire,
    }
    if extra_claims:
        payload.update(extra_claims)

    encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded, jti


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc
=======
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.hash import pbkdf2_sha256
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Union[str, None]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None
>>>>>>> master
