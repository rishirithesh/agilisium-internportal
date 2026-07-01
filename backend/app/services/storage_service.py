import os
import uuid
from pathlib import Path
from typing import BinaryIO

from app.core.config import settings


class StorageService:
    def __init__(self):
        self.base = Path(settings.STORAGE_LOCAL_PATH)
        self.base.mkdir(parents=True, exist_ok=True)

    def save_pdf(self, file_bytes: bytes, dest_folder: str | None = None, original_name: str | None = None) -> str:
        folder = self.base
        if dest_folder:
            folder = folder / dest_folder
        folder.mkdir(parents=True, exist_ok=True)

        ext = ".pdf"
        filename = f"{uuid.uuid4()}{ext}"
        path = folder / filename
        with open(path, "wb") as f:
            f.write(file_bytes)

        # return storage key relative to base
        return str(path.relative_to(self.base))

    def get_path(self, storage_key: str) -> Path:
        return self.base / storage_key

    def read(self, storage_key: str) -> bytes:
        path = self.get_path(storage_key)
        with open(path, "rb") as f:
            return f.read()
