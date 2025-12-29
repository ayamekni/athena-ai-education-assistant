"""
Pydantic schemas for room requests and responses
"""
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class RoomCreateSchema(BaseModel):
    """Schema for creating a new room"""
    title: str = Field(..., min_length=1, max_length=100, description="Room title")
    purpose: str = Field(..., min_length=1, max_length=500, description="Room purpose/description")
    skillsNeeded: List[str] = Field(default_factory=list, description="Skills required for room")
    deadline: Union[datetime, str] = Field(..., description="Project deadline (ISO 8601 format)")
    maxMembers: int = Field(..., ge=2, le=20, description="Maximum number of members (2-20)")
    teacherSupervisorId: Optional[str] = Field(None, description="Optional teacher supervisor ID")
    
    @field_validator('deadline', mode='before')
    @classmethod
    def parse_deadline(cls, v):
        """Parse deadline from string or datetime"""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid datetime format. Use ISO 8601 format (e.g., '2025-12-31T23:59:59' or '2025-12-31T23:59:59Z')")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "AI Study Group",
                "purpose": "Collaborative learning for machine learning fundamentals",
                "skillsNeeded": ["Python", "Machine Learning"],
                "deadline": "2025-12-31T23:59:59Z",
                "maxMembers": 5,
                "teacherSupervisorId": None
            }
        }


class RoomUpdateSchema(BaseModel):
    """Schema for updating a room (creator only)"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Room title")
    purpose: Optional[str] = Field(None, min_length=1, max_length=500, description="Room purpose/description")
    skillsNeeded: Optional[List[str]] = Field(None, description="Skills required for room")
    deadline: Optional[Union[datetime, str]] = Field(None, description="Project deadline (ISO 8601 format)")
    maxMembers: Optional[int] = Field(None, ge=2, le=20, description="Maximum number of members (2-20)")
    teacherSupervisorId: Optional[str] = Field(None, description="Optional teacher supervisor ID")
    
    @field_validator('deadline', mode='before')
    @classmethod
    def parse_deadline(cls, v):
        """Parse deadline from string or datetime"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid datetime format. Use ISO 8601 format (e.g., '2025-12-31T23:59:59' or '2025-12-31T23:59:59Z')")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated AI Study Group",
                "purpose": "Updated description",
                "deadline": "2025-12-31T23:59:59Z"
            }
        }


class RoomResponseSchema(BaseModel):
    """Schema for room response"""
    _id: str
    creatorId: str
    type: str  # "student" or "teacher"
    title: str
    purpose: str
    skillsNeeded: List[str]
    deadline: str  # ISO format
    teacherSupervisorId: Optional[str]
    maxMembers: int
    members: List[str]
    pendingRequests: List[str]
    invitedUsers: List[str]
    createdAt: str  # ISO format

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "creatorId": "507f1f77bcf86cd799439012",
                "type": "student",
                "title": "AI Study Group",
                "purpose": "Collaborative learning",
                "skillsNeeded": ["Python", "ML"],
                "deadline": "2025-12-31T23:59:59Z",
                "teacherSupervisorId": None,
                "maxMembers": 5,
                "members": ["507f1f77bcf86cd799439012"],
                "pendingRequests": [],
                "invitedUsers": [],
                "createdAt": "2025-12-09T10:00:00Z"
            }
        }


class RoomDetailedResponseSchema(RoomResponseSchema):
    """Extended room response with user context"""
    isMember: bool = Field(description="Is current user a member?")
    isCreator: bool = Field(description="Is current user the creator?")
    canJoin: bool = Field(description="Can current user join this room?")
    pending: bool = Field(description="Does user have a pending request?")

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "creatorId": "507f1f77bcf86cd799439012",
                "type": "student",
                "title": "AI Study Group",
                "purpose": "Collaborative learning",
                "skillsNeeded": ["Python", "ML"],
                "deadline": "2025-12-31T23:59:59Z",
                "teacherSupervisorId": None,
                "maxMembers": 5,
                "members": ["507f1f77bcf86cd799439012"],
                "pendingRequests": [],
                "invitedUsers": [],
                "createdAt": "2025-12-09T10:00:00Z",
                "isMember": False,
                "isCreator": False,
                "canJoin": True,
                "pending": False
            }
        }


class JoinRequestSchema(BaseModel):
    """Schema for join request approval/rejection"""
    studentId: str = Field(..., description="Student ID to approve/reject")

    class Config:
        json_schema_extra = {
            "example": {
                "studentId": "507f1f77bcf86cd799439013"
            }
        }


class InviteSchema(BaseModel):
    """Schema for inviting a student to a room"""
    studentId: str = Field(..., description="Student ID to invite")

    class Config:
        json_schema_extra = {
            "example": {
                "studentId": "507f1f77bcf86cd799439013"
            }
        }


class RoomMessageResponse(BaseModel):
    """Generic message response for room operations"""
    message: str
    room: Optional[dict] = None  # Optional room data for create operations

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "room": {
                    "roomId": "507f1f77bcf86cd799439011",
                    "title": "Example Room",
                    "type": "student"
                }
            }
        }


class RoomErrorResponse(BaseModel):
    """Error response for room operations"""
    error: str

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Operation failed: Room not found"
            }
        }
