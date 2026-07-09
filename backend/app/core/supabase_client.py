from pathlib import Path
from typing import Optional

from supabase import Client, create_client

from app.core.config import settings


class SupabaseStorageService:
    def __init__(self) -> None:
        self.client: Optional[Client] = None
        self.error: Optional[str] = None

        if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_KEY:
            try:
                self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
            except Exception as exc:  # pragma: no cover - defensive fallback
                self.error = str(exc)
        else:
            self.error = "Supabase credentials are not configured. Set SUPABASE_URL and SUPABASE_SERVICE_KEY."

    def is_configured(self) -> bool:
        return self.client is not None

    def upload_file(self, bucket: str, file_name: str, file_bytes: bytes, content_type: str) -> str:
        if self.client is not None:
            self.client.storage.from_(bucket).upload(
                path=file_name,
                file=file_bytes,
                file_options={"content-type": content_type, "upsert": "false"},
            )
            return self.client.storage.from_(bucket).get_public_url(file_name)

        upload_dir = Path(settings.UPLOAD_DIR) / bucket
        upload_dir.mkdir(parents=True, exist_ok=True)
        target_path = upload_dir / file_name
        target_path.write_bytes(file_bytes)
        return f"/uploads/{bucket}/{file_name}"


storage_service = SupabaseStorageService()


def upload_file_to_storage(bucket: str, file_name: str, file_bytes: bytes, content_type: str) -> str:
    return storage_service.upload_file(bucket, file_name, file_bytes, content_type)
