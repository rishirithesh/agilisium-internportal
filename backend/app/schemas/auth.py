import uuid

from pydantic import BaseModel, EmailStr, Field

from app.core.permissions import Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class OtpRequestSchema(BaseModel):
    email: EmailStr


class OtpVerifySchema(BaseModel):
    email: EmailStr
    otp_code: str = Field(min_length=6, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class CurrentUser(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: Role
    is_email_verified: bool

    model_config = {"from_attributes": True}


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)
    role: Role = Role.EMPLOYEE
