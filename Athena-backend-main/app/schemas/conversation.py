"""
Conversation schemas for ATHENA chat history
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    """Single message in a conversation"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")


class ConversationCreate(BaseModel):
    """Schema for creating a new conversation"""
    userId: str
    messages: List[Message] = Field(default_factory=list)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class ConversationResponse(BaseModel):
    """Schema for conversation response"""
    id: str = Field(..., alias="_id", description="Conversation ID")
    userId: str
    messages: List[Message]
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ConversationListItem(BaseModel):
    """Schema for conversation list item (without full messages)"""
    id: str = Field(..., alias="_id")
    userId: str
    messageCount: int
    lastMessage: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DeleteResponse(BaseModel):
    """Schema for delete operation response"""
    message: str
    deleted_count: Optional[int] = None
