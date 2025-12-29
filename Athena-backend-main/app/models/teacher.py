"""
Teacher profile database model
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class TeacherAvailability(BaseModel):
    """Teacher availability schedule"""
    days: List[str] = []  # e.g., ["Monday", "Wednesday", "Friday"]
    hours: Optional[str] = None  # e.g., "9:00 AM - 5:00 PM"


class TeacherInDB(BaseModel):
    """Teacher profile model as stored in database"""
    id: Optional[str] = Field(default=None, alias="_id")
    userId: str  # Reference to User._id
    firstName: str
    lastName: str
    teaching: str  # Subject taught
    institute: str
    phone: Optional[str] = None
    availability: Optional[TeacherAvailability] = None
    bio: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
