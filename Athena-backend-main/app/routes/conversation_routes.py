"""
Conversation routes for ATHENA chat history system
Handles saving, retrieving, and deleting conversation history
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId

from app.db.mongodb import get_database
from app.core.security import require_role
from app.schemas.conversation import (
    ConversationResponse,
    ConversationListItem,
    DeleteResponse
)

router = APIRouter(prefix="/assistant", tags=["Conversations"])


def conversation_helper(conversation: dict) -> dict:
    """Convert MongoDB conversation document to dict with string ID"""
    if not conversation:
        return None
    
    conversation["_id"] = str(conversation["_id"])
    return conversation


@router.get("/conversations", response_model=List[ConversationListItem])
async def get_conversations(
    current_user: dict = Depends(require_role(["student", "teacher"]))
):
    """
    Get all conversations for the current user
    Returns list sorted by newest first
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Find all conversations for this user
    conversations = await db.conversations.find(
        {"userId": user_id}
    ).sort("updatedAt", -1).to_list(None)
    
    # Format response
    result = []
    for conv in conversations:
        message_count = len(conv.get("messages", []))
        last_message = None
        
        if message_count > 0:
            # Get last message content (truncate if too long)
            last_msg = conv["messages"][-1]
            last_message = last_msg["content"][:100] + "..." if len(last_msg["content"]) > 100 else last_msg["content"]
        
        result.append({
            "_id": str(conv["_id"]),
            "userId": conv["userId"],
            "messageCount": message_count,
            "lastMessage": last_message,
            "createdAt": conv["createdAt"],
            "updatedAt": conv["updatedAt"]
        })
    
    return result


@router.get("/conversation/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: dict = Depends(require_role(["student", "teacher"]))
):
    """
    Get a specific conversation by ID
    Only returns if conversation belongs to current user
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Validate ObjectId
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    
    # Find conversation
    conversation = await db.conversations.find_one({
        "_id": ObjectId(conversation_id),
        "userId": user_id
    })
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation_helper(conversation)


@router.delete("/conversation/{conversation_id}", response_model=DeleteResponse)
async def delete_conversation(
    conversation_id: str,
    current_user: dict = Depends(require_role(["student", "teacher"]))
):
    """
    Delete a specific conversation
    Only deletes if conversation belongs to current user
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Validate ObjectId
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    
    # Delete conversation
    result = await db.conversations.delete_one({
        "_id": ObjectId(conversation_id),
        "userId": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or already deleted"
        )
    
    return {
        "message": "Conversation deleted",
        "deleted_count": result.deleted_count
    }


@router.delete("/conversations/clear", response_model=DeleteResponse)
async def clear_all_conversations(
    current_user: dict = Depends(require_role(["student", "teacher"]))
):
    """
    Delete ALL conversations for the current user
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Delete all conversations for this user
    result = await db.conversations.delete_many({"userId": user_id})
    
    return {
        "message": "All conversations cleared",
        "deleted_count": result.deleted_count
    }


@router.delete("/conversation/{conversation_id}/message/{message_index}", response_model=DeleteResponse)
async def delete_message_from_conversation(
    conversation_id: str,
    message_index: int,
    current_user: dict = Depends(require_role(["student", "teacher"]))
):
    """
    Delete a specific message from a conversation by index
    This will remove the message at the specified index from the messages array
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Validate ObjectId
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    
    # Find conversation
    conversation = await db.conversations.find_one({
        "_id": ObjectId(conversation_id),
        "userId": user_id
    })
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = conversation.get("messages", [])
    
    # Validate message index
    if message_index < 0 or message_index >= len(messages):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid message index. Must be between 0 and {len(messages) - 1}"
        )
    
    # Remove message at index
    messages.pop(message_index)
    
    # Update conversation
    await db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$set": {
                "messages": messages,
                "updatedAt": datetime.utcnow()
            }
        }
    )
    
    return {
        "message": f"Message at index {message_index} deleted",
        "deleted_count": 1
    }
