"""
Student routes
"""
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime
from pymongo import ReturnDocument

from app.schemas.student import StudentResponse, StudentProfileUpdate
from app.core.security import require_role
from app.db.mongodb import get_database

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/profile", response_model=StudentResponse)
async def get_student_profile(current_user: dict = Depends(require_role(["student"]))):
    """Get current student's profile"""
    db = get_database()
    
    # Get student profile
    profile = await db.students.find_one({"userId": current_user["user_id"]})
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    # Convert ObjectId to string
    profile["_id"] = str(profile["_id"])
    profile["email"] = current_user["email"]
    
    return profile


@router.put("/profile", response_model=StudentResponse)
async def update_student_profile(
    profile_update: StudentProfileUpdate,
    current_user: dict = Depends(require_role(["student"]))
):
    """Update current student's profile"""
    db = get_database()
    
    # Prepare update data (only non-None fields)
    update_data = {
        k: v for k, v in profile_update.dict(exclude_unset=True).items() if v is not None
    }
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Add updatedAt timestamp
    update_data["updatedAt"] = datetime.utcnow()
    
    # Update profile and return updated document
    updated_profile = await db.students.find_one_and_update(
        {"userId": current_user["user_id"]},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    # Convert ObjectId to string and add email
    updated_profile["_id"] = str(updated_profile["_id"])
    updated_profile["email"] = current_user["email"]
    
    return updated_profile
