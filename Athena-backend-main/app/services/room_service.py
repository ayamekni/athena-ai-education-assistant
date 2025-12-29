"""
Room service - Business logic for collaboration rooms
"""
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pymongo import ReturnDocument
from fastapi import HTTPException, status

from app.models.room import Room
from app.db.mongodb import get_database


async def validate_teacher_supervisor(teacher_id: str) -> bool:
    """
    Validate that a teacher supervisor exists
    
    Args:
        teacher_id: Teacher user ID
        
    Returns:
        True if teacher exists, False otherwise
    """
    db = get_database()
    teacher = await db.users.find_one({"_id": ObjectId(teacher_id), "role": "teacher"})
    return teacher is not None


async def create_room(current_user: dict, room_data: dict) -> dict:
    """
    Create a new collaboration room
    
    Rules:
    - Students create public rooms (type="student")
    - Teachers create private rooms (type="teacher")
    - Creator is auto-added to members
    - maxMembers must be >= 2
    - teacherSupervisorId is validated if provided
    
    Args:
        current_user: Authenticated user
        room_data: Room creation data
        
    Returns:
        Created room document
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    user_role = current_user["role"]
    
    # Validate maxMembers
    if room_data["maxMembers"] < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="maxMembers must be at least 2"
        )
    
    # Validate teacher supervisor if provided
    if room_data.get("teacherSupervisorId"):
        if not await validate_teacher_supervisor(room_data["teacherSupervisorId"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher supervisor not found"
            )
    
    # Determine room type based on creator role
    room_type = "student" if user_role == "student" else "teacher"
    
    # Create room document
    room_doc = Room.create(
        creator_id=user_id,
        room_type=room_type,
        title=room_data["title"],
        purpose=room_data["purpose"],
        skills_needed=room_data.get("skillsNeeded", []),
        deadline=room_data["deadline"],
        max_members=room_data["maxMembers"],
        teacher_supervisor_id=room_data.get("teacherSupervisorId")
    )
    
    # Insert into database
    result = await db.rooms.insert_one(room_doc)
    room_doc["_id"] = str(result.inserted_id)
    
    print(f"✅ Room created: {room_doc['title']} by {user_role} {user_id}")
    
    return Room.to_response(room_doc)


async def get_all_rooms(current_user: dict) -> List[dict]:
    """
    Get all rooms visible to current user
    
    Rules:
    - Students: See student rooms + teacher rooms they're invited to
    - Teachers: See all rooms they created or supervise
    
    Args:
        current_user: Authenticated user
        
    Returns:
        List of room documents
    """
    db = get_database()
    user_id = current_user["user_id"]
    user_role = current_user["role"]
    
    rooms = []
    
    if user_role == "student":
        # Get all student-created rooms
        student_rooms = await db.rooms.find({"type": "student"}).to_list(length=None)
        rooms.extend(student_rooms)
        
        # Get teacher rooms where student is invited or a member
        teacher_rooms = await db.rooms.find({
            "type": "teacher",
            "$or": [
                {"invitedUsers": user_id},
                {"members": user_id}
            ]
        }).to_list(length=None)
        rooms.extend(teacher_rooms)
        
    elif user_role == "teacher":
        # Get all rooms created by this teacher
        created_rooms = await db.rooms.find({"creatorId": user_id}).to_list(length=None)
        rooms.extend(created_rooms)
        
        # Get rooms where teacher is supervisor
        supervised_rooms = await db.rooms.find({"teacherSupervisorId": user_id}).to_list(length=None)
        rooms.extend(supervised_rooms)
    
    return [Room.to_response(room) for room in rooms]


async def get_my_rooms(current_user: dict) -> List[dict]:
    """
    Get rooms where user is a member
    
    Args:
        current_user: Authenticated user
        
    Returns:
        List of rooms where user is in members list
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    rooms = await db.rooms.find({"members": user_id}).to_list(length=None)
    return [Room.to_response(room) for room in rooms]


async def get_room(room_id: str, current_user: dict) -> dict:
    """
    Get detailed room information with user context
    
    Returns:
    - room: Full room data
    - isMember: Is user a member?
    - isCreator: Is user the creator?
    - canJoin: Can user join?
    - pending: Does user have pending request?
    
    Rules:
    - Teacher rooms hidden unless invited/member
    
    Args:
        room_id: Room ID
        current_user: Authenticated user
        
    Returns:
        Room data with user context
        
    Raises:
        HTTPException: If room not found or not accessible
    """
    db = get_database()
    user_id = current_user["user_id"]
    user_role = current_user["role"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check visibility for teacher rooms
    if room["type"] == "teacher":
        if user_id not in room["members"] and user_id not in room["invitedUsers"] and user_id != room["creatorId"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this room"
            )
    
    # Calculate user context
    is_member = user_id in room["members"]
    is_creator = user_id == room["creatorId"]
    pending = user_id in room["pendingRequests"]
    
    # Determine if user can join
    can_join = False
    if not is_member:
        if room["type"] == "student" and user_role == "student":
            # Student rooms: can join if not full and not already pending
            can_join = len(room["members"]) < room["maxMembers"] and not pending
        elif room["type"] == "teacher":
            # Teacher rooms: can join only if invited
            can_join = user_id in room["invitedUsers"] and len(room["members"]) < room["maxMembers"]
    
    # Build response
    room_response = Room.to_response(room)
    room_response.update({
        "isMember": is_member,
        "isCreator": is_creator,
        "canJoin": can_join,
        "pending": pending
    })
    
    return room_response


async def send_join_request(room_id: str, current_user: dict) -> dict:
    """
    Send join request to a student-created room
    
    Rules:
    - Only students can request
    - Room must be type="student"
    - Cannot request twice
    - Cannot request if already member
    - Cannot exceed maxMembers
    
    Args:
        room_id: Room ID
        current_user: Authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    user_role = current_user["role"]
    
    # Only students can send join requests
    if user_role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can send join requests"
        )
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Must be student room
    if room["type"] != "student":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only request to join student-created rooms"
        )
    
    # Check if already member
    if user_id in room["members"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a member of this room"
        )
    
    # Check if already pending
    if user_id in room["pendingRequests"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending request for this room"
        )
    
    # Check if room is full
    if len(room["members"]) >= room["maxMembers"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is full"
        )
    
    # Add to pending requests
    await db.rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$addToSet": {"pendingRequests": user_id}}
    )
    
    print(f"📨 Join request sent: User {user_id} → Room {room_id}")
    
    return {"message": "Join request sent successfully"}


async def approve_request(room_id: str, current_user: dict, student_id: str) -> dict:
    """
    Approve a join request
    
    Rules:
    - Only room creator can approve
    - Move student from pendingRequests to members
    - Cannot exceed maxMembers
    
    Args:
        room_id: Room ID
        current_user: Authenticated user (must be creator)
        student_id: Student ID to approve
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Must be creator
    if room["creatorId"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room creator can approve requests"
        )
    
    # Check if student has pending request
    if student_id not in room["pendingRequests"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending request from this student"
        )
    
    # Check if room is full
    if len(room["members"]) >= room["maxMembers"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is full"
        )
    
    # Approve: remove from pending, add to members
    await db.rooms.update_one(
        {"_id": ObjectId(room_id)},
        {
            "$pull": {"pendingRequests": student_id},
            "$addToSet": {"members": student_id}
        }
    )
    
    print(f"✅ Join request approved: Student {student_id} → Room {room_id}")
    
    return {"message": "Join request approved successfully"}


async def reject_request(room_id: str, current_user: dict, student_id: str) -> dict:
    """
    Reject a join request
    
    Rules:
    - Only room creator can reject
    - Remove student from pendingRequests
    
    Args:
        room_id: Room ID
        current_user: Authenticated user (must be creator)
        student_id: Student ID to reject
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Must be creator
    if room["creatorId"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room creator can reject requests"
        )
    
    # Check if student has pending request
    if student_id not in room["pendingRequests"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending request from this student"
        )
    
    # Reject: remove from pending
    await db.rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$pull": {"pendingRequests": student_id}}
    )
    
    print(f"❌ Join request rejected: Student {student_id} ✗ Room {room_id}")
    
    return {"message": "Join request rejected successfully"}


async def invite_user(room_id: str, current_user: dict, student_id: str) -> dict:
    """
    Invite a student to a room
    
    Rules:
    - Only teachers or room creators can invite
    - Add student to invitedUsers
    - Student can then join the room
    
    Args:
        room_id: Room ID
        current_user: Authenticated user (must be creator or teacher)
        student_id: Student ID to invite
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Must be creator
    if room["creatorId"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room creator can invite students"
        )
    
    # Validate student exists
    student = await db.users.find_one({"_id": ObjectId(student_id), "role": "student"})
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if already member
    if student_id in room["members"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already a member"
        )
    
    # Check if already invited
    if student_id in room["invitedUsers"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already invited"
        )
    
    # Add to invited list
    await db.rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$addToSet": {"invitedUsers": student_id}}
    )
    
    print(f"📧 Student invited: {student_id} → Room {room_id}")
    
    return {"message": "Student invited successfully"}


async def join_room(room_id: str, current_user: dict) -> dict:
    """
    Join a room (for invited users in teacher rooms)
    
    Rules:
    - Must be invited (for teacher rooms)
    - Cannot exceed maxMembers
    - Remove from invitedUsers, add to members
    
    Args:
        room_id: Room ID
        current_user: Authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if already member
    if user_id in room["members"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a member of this room"
        )
    
    # Check if room is full
    if len(room["members"]) >= room["maxMembers"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is full"
        )
    
    # For teacher rooms, must be invited
    if room["type"] == "teacher":
        if user_id not in room["invitedUsers"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be invited to join this room"
            )
    
    # Join: add to members, remove from invited
    await db.rooms.update_one(
        {"_id": ObjectId(room_id)},
        {
            "$addToSet": {"members": user_id},
            "$pull": {"invitedUsers": user_id}
        }
    )
    
    print(f"✅ User joined room: {user_id} → Room {room_id}")
    
    return {"message": "Joined room successfully"}


async def leave_room(room_id: str, current_user: dict) -> dict:
    """
    Leave a room
    
    Rules:
    - Creator cannot leave (must delete room instead)
    - Remove user from members
    
    Args:
        room_id: Room ID
        current_user: Authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Creator cannot leave
    if room["creatorId"] == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room creator cannot leave. Delete the room instead"
        )
    
    # Check if user is member
    if user_id not in room["members"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of this room"
        )
    
    # Leave: remove from members
    await db.rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$pull": {"members": user_id}}
    )
    
    print(f"👋 User left room: {user_id} ← Room {room_id}")
    
    return {"message": "Left room successfully"}


async def update_room(room_id: str, current_user: dict, update_data: dict) -> dict:
    """
    Update a room
    
    Rules:
    - Only creator can update
    - Can update: title, purpose, skillsNeeded, deadline, maxMembers, teacherSupervisorId
    - Cannot update: type, members, requests, invitations
    
    Args:
        room_id: Room ID
        current_user: Authenticated user (must be creator)
        update_data: Fields to update
        
    Returns:
        Updated room document
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Must be creator
    if room["creatorId"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room creator can update the room"
        )
    
    # Prepare update data (only allow specific fields)
    allowed_fields = {"title", "purpose", "skillsNeeded", "deadline", "maxMembers", "teacherSupervisorId"}
    update_fields = {k: v for k, v in update_data.items() if k in allowed_fields and v is not None}
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )
    
    # Validate maxMembers if provided
    if "maxMembers" in update_fields:
        max_members = update_fields["maxMembers"]
        if max_members < 2 or max_members > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="maxMembers must be between 2 and 20"
            )
        # Ensure maxMembers is not less than current members
        if max_members < len(room.get("members", [])):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot reduce maxMembers below current member count ({len(room.get('members', []))})"
            )
    
    # Validate teacherSupervisorId if provided
    if "teacherSupervisorId" in update_fields and update_fields["teacherSupervisorId"]:
        if not await validate_teacher_supervisor(update_fields["teacherSupervisorId"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid teacher supervisor ID"
            )
    
    # Add updated timestamp
    update_fields["updatedAt"] = datetime.utcnow()
    
    # Update room
    updated_room = await db.rooms.find_one_and_update(
        {"_id": ObjectId(room_id)},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )
    
    # Convert to response format
    room_response = Room.to_response(updated_room)
    
    print(f"✏️ Room updated: {room_id} by {user_id}")
    
    return room_response


async def delete_room(room_id: str, current_user: dict) -> dict:
    """
    Delete a room
    
    Rules:
    - Only creator can delete
    - Permanently removes room and all data
    
    Args:
        room_id: Room ID
        current_user: Authenticated user (must be creator)
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If validation fails
    """
    db = get_database()
    user_id = current_user["user_id"]
    
    # Get room
    try:
        room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Must be creator
    if room["creatorId"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room creator can delete the room"
        )
    
    # Delete room
    await db.rooms.delete_one({"_id": ObjectId(room_id)})
    
    print(f"🗑️ Room deleted: {room_id} by {user_id}")
    
    return {"message": "Room deleted successfully"}
