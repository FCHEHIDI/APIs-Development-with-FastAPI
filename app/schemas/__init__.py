"""
Pydantic schemas for request/response models.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Post Schemas
class PostBase(BaseModel):
    """Base post schema."""
    title: str
    content: str
    is_published: bool = False


class PostCreate(PostBase):
    """Schema for post creation."""
    pass


class PostUpdate(BaseModel):
    """Schema for post updates."""
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


class PostResponse(PostBase):
    """Schema for post response."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner: UserResponse
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str


# Generic Response Schemas
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    error_code: Optional[str] = None


# Pagination Schema
class PaginatedResponse(BaseModel):
    """Paginated response schema."""
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int
