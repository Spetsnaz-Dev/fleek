import os
import shutil

from app.core.config import settings

class LocalMediaStorage:
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    async def save(self, filename: str, content: bytes) -> str:
        full_path = os.path.join(self.base_path, filename)
        with open(full_path, "wb") as out:
            out.write(content)
        return full_path

# Extend later for S3/MinIO backend.
def get_media_client():
    if settings.STORAGE_BACKEND == "local":
        return LocalMediaStorage(settings.LOCAL_MEDIA_PATH)
    else:
        raise NotImplementedError("S3/MinIO TODO here.")
