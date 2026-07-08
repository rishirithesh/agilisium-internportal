import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/airp"
    JWT_SECRET: str = "9825b741029c017d23a49f87ef9280cdb90a12e2c56aef7b62c451db93ff0e81"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Supabase (for file storage)
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = ""  # service_role key from Supabase dashboard

    # SMTP Defaults (from env, will be fallback if not in DB settings)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_FROM: str = "Agilisium Intern Portal <noreply@example.com>"
    
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        extra = "ignore"

settings = Settings()
