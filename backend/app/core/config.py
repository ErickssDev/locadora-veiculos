from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    frontend_url: str
    cors_origins: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
