"""
Room routes - API endpoints for collaboration rooms
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.room import (
    RoomCreateSchema,
    RoomResponseSchema,
    RoomDetailedResponseSchema,
    RoomUpdateSchema,
    JoinRequestSchema,
    InviteSchema,
    RoomMessageResponse,
    RoomErrorResponse
)
from app.core.security import get_current_user, require_role
from app.services import room_service


router = APIRouter()


@router.post(
    "/create",
    response_model=RoomMessageResponse,
    summary="Create a new collaboration room",
    description="Students create public rooms (approval-based), teachers create private rooms (invite-only)"
)
async def create_room(
    room_data: RoomCreateSchema,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new collaboration room
    
    **Rules:**
    - Students: Create public rooms (type="student") where others can request to join
    - Teachers: Create private rooms (type="teacher") that are invite-only
    - Creator is auto-added to members
    - maxMembers must be between 2-20
    - deadline must be a future date
    """
    try:
        room = await room_service.create_room(current_user, room_data.dict())
        return RoomMessageResponse(
            message="Room created successfully",
            room=room
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error creating room: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create room"
        )


@router.get(
    "/all",
    summary="Get all visible rooms",
    description="Returns rooms based on user role and access permissions"
)
async def get_all_rooms(
    current_user: dict = Depends(get_current_user)
):
    """
    Get all rooms visible to current user
    
    **Visibility Rules:**
    - Students: See all student-created rooms + teacher rooms they're invited to
    - Teachers: See all rooms they created or supervise
    """
    try:
        rooms = await room_service.get_all_rooms(current_user)
        return {"rooms": rooms}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching rooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch rooms"
        )


@router.get(
    "/my",
    summary="Get my rooms",
    description="Returns rooms where user is a member"
)
async def get_my_rooms(
    current_user: dict = Depends(get_current_user)
):
    """
    Get rooms where user is a member
    
    Returns only rooms where the user is in the members list
    """
    try:
        rooms = await room_service.get_my_rooms(current_user)
        return {"rooms": rooms}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching my rooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch your rooms"
        )


@router.get(
    "/{room_id}",
    response_model=RoomDetailedResponseSchema,
    summary="Get detailed room information",
    description="Returns room data with user context (isMember, isCreator, canJoin, pending)"
)
async def get_room(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed room information with user context
    
    **Returns:**
    - room: Full room data
    - isMember: Is user a member?
    - isCreator: Is user the creator?
    - canJoin: Can user join this room?
    - pending: Does user have a pending join request?
    
    **Note:** Teacher rooms are hidden unless user is invited/member
    """
    try:
        room = await room_service.get_room(room_id, current_user)
        return room
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching room {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch room details"
        )


@router.put(
    "/{room_id}",
    response_model=RoomMessageResponse,
    summary="Update room details (creator only)",
    description="Update room information"
)
async def update_room(
    room_id: str,
    room_data: RoomUpdateSchema,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a room
    
    **Rules:**
    - Only room creator can update
    - Can update: title, purpose, skillsNeeded, deadline, maxMembers, teacherSupervisorId
    - Cannot reduce maxMembers below current member count
    
    **Fields:**
    - title: Room title
    - purpose: Room description/purpose
    - skillsNeeded: List of required skills
    - deadline: Project deadline
    - maxMembers: Maximum members (2-20)
    - teacherSupervisorId: Teacher supervisor (optional)
    """
    try:
        result = await room_service.update_room(
            room_id,
            current_user,
            room_data.dict(exclude_unset=True)
        )
        return RoomMessageResponse(
            message="Room updated successfully",
            room=result
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error updating room {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update room"
        )


@router.post(
    "/{room_id}/request-join",
    response_model=RoomMessageResponse,
    summary="Send join request (students only)",
    description="Send a join request to a student-created room"
)
async def request_join(
    room_id: str,
    current_user: dict = Depends(require_role(["student"]))
):
    """
    Send join request to a student-created room
    
    **Rules:**
    - Only students can send join requests
    - Room must be type="student"
    - Cannot request twice
    - Cannot request if already a member
    - Room must not be full
    
    **Note:** Room creator must approve the request
    """
    try:
        result = await room_service.send_join_request(room_id, current_user)
        return RoomMessageResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error sending join request to {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send join request"
        )


@router.post(
    "/{room_id}/approve",
    response_model=RoomMessageResponse,
    summary="Approve join request (creator only)",
    description="Approve a pending join request"
)
async def approve_request(
    room_id: str,
    request_data: JoinRequestSchema,
    current_user: dict = Depends(get_current_user)
):
    """
    Approve a join request
    
    **Rules:**
    - Only room creator can approve
    - Student must have pending request
    - Room must not be full
    - Moves student from pendingRequests to members
    """
    print(f"🔍 Approve request received:")
    print(f"   Room ID: {room_id}")
    print(f"   Student ID: {request_data.studentId}")
    print(f"   Student ID type: {type(request_data.studentId)}")
    try:
        result = await room_service.approve_request(
            room_id,
            current_user,
            request_data.studentId
        )
        return RoomMessageResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error approving request in {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve join request"
        )


@router.post(
    "/{room_id}/reject",
    response_model=RoomMessageResponse,
    summary="Reject join request (creator only)",
    description="Reject a pending join request"
)
async def reject_request(
    room_id: str,
    request_data: JoinRequestSchema,
    current_user: dict = Depends(get_current_user)
):
    """
    Reject a join request
    
    **Rules:**
    - Only room creator can reject
    - Student must have pending request
    - Removes student from pendingRequests
    """
    try:
        result = await room_service.reject_request(
            room_id,
            current_user,
            request_data.studentId
        )
        return RoomMessageResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error rejecting request in {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject join request"
        )


@router.post(
    "/{room_id}/invite",
    response_model=RoomMessageResponse,
    summary="Invite student to room (creator only)",
    description="Invite a student to join the room"
)
async def invite_user(
    room_id: str,
    invite_data: InviteSchema,
    current_user: dict = Depends(get_current_user)
):
    """
    Invite a student to the room
    
    **Rules:**
    - Only room creator can invite
    - Student must exist and not be a member
    - Student must not already be invited
    - Adds student to invitedUsers list
    
    **Note:** Useful for teacher rooms (invite-only) or proactive invitations
    """
    try:
        result = await room_service.invite_user(
            room_id,
            current_user,
            invite_data.studentId
        )
        return RoomMessageResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error inviting user to {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to invite student"
        )


@router.post(
    "/{room_id}/join",
    response_model=RoomMessageResponse,
    summary="Join room (for invited users)",
    description="Join a room (must be invited for teacher rooms)"
)
async def join_room(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Join a room
    
    **Rules:**
    - For teacher rooms: Must be invited
    - Room must not be full
    - Cannot join if already a member
    - Moves user from invitedUsers to members
    """
    try:
        result = await room_service.join_room(room_id, current_user)
        return RoomMessageResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error joining room {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to join room"
        )


@router.delete(
    "/{room_id}/leave",
    response_model=RoomMessageResponse,
    summary="Leave room",
    description="Leave a room (creator cannot leave, must delete instead)"
)
async def leave_room(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Leave a room
    
    **Rules:**
    - Creator cannot leave (must delete room instead)
    - Must be a member to leave
    - Removes user from members list
    """
    try:
        result = await room_service.leave_room(room_id, current_user)
        return RoomMessageResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error leaving room {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to leave room"
        )


@router.delete(
    "/{room_id}",
    response_model=RoomMessageResponse,
    summary="Delete room (creator only)",
    description="Permanently delete a room"
)
async def delete_room(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a room
    
    **Rules:**
    - Only room creator can delete
    - Permanently removes room and all data
    - All members will lose access
    """
    try:
        result = await room_service.delete_room(room_id, current_user)
        return RoomMessageResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting room {room_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete room"
        )
