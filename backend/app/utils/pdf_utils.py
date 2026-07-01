from typing import Tuple

def is_pdf(bytes_data: bytes) -> bool:
    # Simple header check for PDF files
    return bytes_data.startswith(b"%PDF-")

def validate_pdf(bytes_data: bytes, max_size_bytes: int = 5 * 1024 * 1024) -> Tuple[bool, str]:
    if not is_pdf(bytes_data):
        return False, "Not a valid PDF file"
    if len(bytes_data) > max_size_bytes:
        return False, "File exceeds maximum allowed size"
    return True, "ok"
