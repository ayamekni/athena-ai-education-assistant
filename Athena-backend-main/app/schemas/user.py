"""
User Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8)
    role: str


class UserResponse(BaseModel):
    """User response schema"""
    id: str = Field(..., alias="_id")
    email: str
    role: str
    createdAt: str
    
    class Config:
        populate_by_name = True


class AdminCreate(BaseModel):
    """Admin creation schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)
