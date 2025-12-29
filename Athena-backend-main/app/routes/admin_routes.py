"""
Admin routes
"""
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List, Dict

from app.core.security import require_role
from app.db.mongodb import get_database

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
async def get_all_users(current_user: dict = Depends(require_role(["admin"]))):
    """Get all users (admin only)"""
    db = get_database()
    
    users = []
    
    # Fetch all users
    async for user in db.users.find():
        user_data = {
            "id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"],
            "createdAt": user["createdAt"].isoformat()
        }
        
        # Fetch profile data based on role
        if user["role"] == "student":
            profile = await db.students.find_one({"userId": str(user["_id"])})
            if profile:
                user_data["profile"] = {
                    "firstName": profile.get("firstName"),
                    "lastName": profile.get("lastName"),
                    "institute": profile.get("institute"),
                    "year": profile.get("year"),
                    "speciality": profile.get("speciality")
                }
        elif user["role"] == "teacher":
            profile = await db.teachers.find_one({"userId": str(user["_id"])})
            if profile:
                user_data["profile"] = {
                    "firstName": profile.get("firstName"),
                    "lastName": profile.get("lastName"),
                    "institute": profile.get("institute"),
                    "teaching": profile.get("teaching")
                }
        
        users.append(user_data)
    
    return {"users": users, "total": len(users)}


@router.delete("/user/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_role(["admin"]))
):
    """Delete a user and their profile (admin only)"""
    db = get_database()
    
    # Validate ObjectId
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    # Find user
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if str(user["_id"]) == current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete profile based on role
    if user["role"] == "student":
        await db.students.delete_one({"userId": user_id})
    elif user["role"] == "teacher":
        await db.teachers.delete_one({"userId": user_id})
    
    # Delete user
    await db.users.delete_one({"_id": ObjectId(user_id)})
    
    return {
        "message": f"User {user['email']} deleted successfully",
        "deleted_user_id": user_id
    }


@router.get("/stats")
async def get_platform_stats(current_user: dict = Depends(require_role(["admin"]))):
    """Get platform statistics (admin only)"""
    db = get_database()
    
    total_users = await db.users.count_documents({})
    total_students = await db.users.count_documents({"role": "student"})
    total_teachers = await db.users.count_documents({"role": "teacher"})
    total_admins = await db.users.count_documents({"role": "admin"})
    
    return {
        "total_users": total_users,
        "students": total_students,
        "teachers": total_teachers,
        "admins": total_admins
    }
