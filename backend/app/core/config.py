from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str

    # Auth
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    OTP_EXPIRE_MINUTES: int = 10

    # SMTP
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_APP_PASSWORD: str = Field(
        default="",
        validation_alias=AliasChoices("SMTP_APP_PASSWORD", "SMTP_PASS"),
    )
    SMTP_FROM_NAME: str = "AIRP"
    SMTP_FROM_EMAIL: str | None = None
    SMTP_FROM: str | None = None

    # Storage
    STORAGE_BACKEND: str = "local"
    STORAGE_LOCAL_PATH: str = "./uploads"
    S3_BUCKET: str | None = None
    S3_REGION: str | None = None
    S3_ACCESS_KEY_ID: str | None = None
    S3_SECRET_ACCESS_KEY: str | None = None

    # App
    ENVIRONMENT: str = "local"
    CORS_ORIGINS: str = "http://localhost:5173"
    APP_BASE_URL: str = "http://localhost:8000"
    FRONTEND_BASE_URL: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def smtp_from_display_name(self) -> str:
        if self.SMTP_FROM:
            if "<" in self.SMTP_FROM and ">" in self.SMTP_FROM:
                return self.SMTP_FROM.split("<", 1)[0].strip()
            return self.SMTP_FROM
        return self.SMTP_FROM_NAME or "AIRP"

    @property
    def smtp_from_address(self) -> str:
        if self.SMTP_FROM_EMAIL:
            return self.SMTP_FROM_EMAIL
        if self.SMTP_FROM and "<" in self.SMTP_FROM and ">" in self.SMTP_FROM:
            return self.SMTP_FROM.split("<", 1)[1].rstrip(">\"").strip()
        return self.SMTP_USER


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
