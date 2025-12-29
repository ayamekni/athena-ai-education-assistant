"""
Student profile database model
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class StudentLinks(BaseModel):
    """Student social/portfolio links"""
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None


class StudentInDB(BaseModel):
    """Student profile model as stored in database"""
    id: Optional[str] = Field(default=None, alias="_id")
    userId: str  # Reference to User._id
    firstName: str
    lastName: str
    institute: str
    year: str  # 1st, 2nd, 3rd, 4th, 5th
    speciality: str
    phone: Optional[str] = None
    skills: Optional[List[str]] = []
    bio: Optional[str] = None
    links: Optional[StudentLinks] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
