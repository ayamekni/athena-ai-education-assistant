"""
Student Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class StudentLinks(BaseModel):
    """Student social/portfolio links"""
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None


class StudentCreate(BaseModel):
    """Student registration schema"""
    # User fields
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    # Student profile fields (required)
    firstName: str = Field(..., min_length=1)
    lastName: str = Field(..., min_length=1)
    institute: str = Field(..., min_length=1)
    year: str = Field(..., pattern="^(1st|2nd|3rd|4th|5th)$")
    speciality: str = Field(..., min_length=1)
    
    # Optional fields
    phone: Optional[str] = None
    skills: Optional[List[str]] = []
    
    class Config:
        extra = "ignore"  # Ignore extra fields from frontend
    bio: Optional[str] = None
    links: Optional[StudentLinks] = None


class StudentProfileUpdate(BaseModel):
    """Student profile update schema - all fields optional"""
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    institute: Optional[str] = None
    year: Optional[str] = Field(None, pattern="^(1st|2nd|3rd|4th|5th)$")
    speciality: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    bio: Optional[str] = None
    links: Optional[StudentLinks] = None
    
    class Config:
        extra = "ignore"  # Ignore extra fields from frontend


class StudentResponse(BaseModel):
    """Student profile response schema"""
    id: str = Field(..., alias="_id")
    userId: str
    firstName: str
    lastName: str
    email: str
    institute: str
    year: str
    speciality: str
    phone: Optional[str] = None
    skills: Optional[List[str]] = []
    bio: Optional[str] = None
    links: Optional[StudentLinks] = None
    
    class Config:
        populate_by_name = True
