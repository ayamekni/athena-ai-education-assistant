"""
Teacher Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class TeacherAvailability(BaseModel):
    """Teacher availability schedule"""
    days: List[str] = []
    hours: Optional[str] = None


class TeacherCreate(BaseModel):
    """Teacher registration schema"""
    # User fields
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    # Teacher profile fields (required)
    firstName: str = Field(..., min_length=1)
    lastName: str = Field(..., min_length=1)
    teaching: str = Field(..., min_length=1)
    institute: str = Field(..., min_length=1)
    
    # Optional fields
    phone: Optional[str] = None
    availability: Optional[TeacherAvailability] = None
    bio: Optional[str] = None
    
    class Config:
        extra = "ignore"  # Ignore extra fields from frontend


class TeacherProfileUpdate(BaseModel):
    """Teacher profile update schema - all fields optional"""
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    teaching: Optional[str] = None
    institute: Optional[str] = None
    phone: Optional[str] = None
    availability: Optional[TeacherAvailability] = None
    bio: Optional[str] = None
    
    class Config:
        extra = "ignore"  # Ignore extra fields from frontend


class TeacherResponse(BaseModel):
    """Teacher profile response schema"""
    id: str = Field(..., alias="_id")
    userId: str
    firstName: str
    lastName: str
    email: str
    teaching: str
    institute: str
    phone: Optional[str] = None
    availability: Optional[TeacherAvailability] = None
    bio: Optional[str] = None
    
    class Config:
        populate_by_name = True
