"""
Teacher routes
"""
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
from typing import List

from app.schemas.teacher import TeacherResponse, TeacherProfileUpdate
from app.core.security import require_role, get_current_user
from app.db.mongodb import get_database

router = APIRouter(prefix="/teacher", tags=["Teacher"])


@router.get("/all", response_model=List[dict])
async def get_all_teachers(current_user: dict = Depends(get_current_user)):
    """Get all teachers (for supervisor selection in room creation)"""
    db = get_database()
    
    # Get all users with teacher role
    teachers = await db.users.find(
        {"role": "teacher"},
        {"_id": 1, "email": 1}
    ).to_list(length=None)
    
    # Format response
    teachers_list = []
    for teacher in teachers:
        teacher_id = str(teacher["_id"])
        # Get teacher profile for fullName, department, position
        teacher_profile = await db.teachers.find_one({"userId": teacher_id})
        
        # Extract fields with proper fallbacks
        full_name = ""
        department = ""
        position = ""
        
        if teacher_profile:
            # Try multiple possible field names for name
            full_name = teacher_profile.get("fullName") or teacher_profile.get("firstName", "")
            if not full_name and "lastName" in teacher_profile:
                full_name = f"{teacher_profile.get('firstName', '')} {teacher_profile.get('lastName', '')}".strip()
            department = teacher_profile.get("institute", "")
            position = teacher_profile.get("teaching", "")
        
        teachers_list.append({
            "id": teacher_id,
            "email": teacher.get("email", ""),
            "fullName": full_name,
            "department": department,
            "position": position
        })
    
    return teachers_list


@router.get("/profile", response_model=TeacherResponse)
async def get_teacher_profile(current_user: dict = Depends(require_role(["teacher"]))):
    """Get current teacher's profile"""
    db = get_database()
    
    # Get teacher profile
    profile = await db.teachers.find_one({"userId": current_user["user_id"]})
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )
    
    # Convert ObjectId to string
    profile["_id"] = str(profile["_id"])
    profile["email"] = current_user["email"]
    
    return profile


@router.put("/profile", response_model=TeacherResponse)
async def update_teacher_profile(
    profile_update: TeacherProfileUpdate,
    current_user: dict = Depends(require_role(["teacher"]))
):
    """Update current teacher's profile"""
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
    updated_profile = await db.teachers.find_one_and_update(
        {"userId": current_user["user_id"]},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )
    
    # Convert ObjectId to string and add email
    updated_profile["_id"] = str(updated_profile["_id"])
    updated_profile["email"] = current_user["email"]
    
    return updated_profile
