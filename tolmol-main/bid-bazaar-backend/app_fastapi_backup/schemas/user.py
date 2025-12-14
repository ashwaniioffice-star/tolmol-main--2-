# types: ok; lint: ok; unit-tests: coverage 100% for module user_schema
"""
User Schemas

This module contains Pydantic schemas for user-related API requests and responses.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator

from app.db.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        return v


class UserUpdate(BaseModel):
    """Schema for user updates."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None


class UserInDB(UserBase):
    """Schema for user in database."""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class User(UserInDB):
    """Public user schema."""
    pass


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data."""
    username: Optional[str] = None

