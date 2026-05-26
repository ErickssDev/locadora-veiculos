import cloudinary
import cloudinary.uploader

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


async def upload_file(file_bytes: bytes, folder: str, filename: str) -> dict:
    response = cloudinary.uploader.upload(
        file_bytes,
        folder=folder,
        public_id=filename,
        resource_type="auto",
    )

    return {
        "url": response.get("secure_url"),
        "public_id": response.get("public_id"),
    }


async def delete_file(public_id: str) -> dict:
    return cloudinary.uploader.destroy(public_id, invalidate=True)
