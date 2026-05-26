from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    user_type: str
    avatar_url: str | None = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfile(UserBase):
    id: int


class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None


class UserDocumentResponse(BaseModel):
    id: int
    document_type: str
    file_url: str
    public_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
