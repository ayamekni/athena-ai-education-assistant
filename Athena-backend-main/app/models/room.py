"""
Room model for MongoDB
Handles both student and teacher collaboration rooms
"""
from datetime import datetime
from typing import List, Optional
from bson import ObjectId


class Room:
    """
    MongoDB Room Model
    
    Fields:
    - _id: Unique room identifier
    - creatorId: User who created the room (student or teacher)
    - type: "student" or "teacher" (determines visibility & join rules)
    - title: Room name
    - purpose: Room description
    - skillsNeeded: List of required skills
    - deadline: Project deadline
    - teacherSupervisorId: Optional teacher supervisor (for student rooms)
    - maxMembers: Maximum number of members allowed
    - members: List of userIds (always includes creatorId)
    - pendingRequests: Students requesting to join (student rooms only)
    - invitedUsers: Students invited to join (teacher rooms only)
    - createdAt: Room creation timestamp
    """
    
    @staticmethod
    def create(
        creator_id: str,
        room_type: str,
        title: str,
        purpose: str,
        skills_needed: List[str],
        deadline: datetime,
        max_members: int,
        teacher_supervisor_id: Optional[str] = None
    ) -> dict:
        """
        Create a new room document
        
        Args:
            creator_id: User ID of room creator
            room_type: "student" or "teacher"
            title: Room title
            purpose: Room purpose/description
            skills_needed: Required skills list
            deadline: Project deadline
            max_members: Maximum members allowed
            teacher_supervisor_id: Optional teacher supervisor
            
        Returns:
            Room document ready for MongoDB insertion
        """
        return {
            "creatorId": creator_id,
            "type": room_type,
            "title": title,
            "purpose": purpose,
            "skillsNeeded": skills_needed,
            "deadline": deadline,
            "teacherSupervisorId": teacher_supervisor_id,
            "maxMembers": max_members,
            "members": [creator_id],  # Creator is always first member
            "pendingRequests": [],
            "invitedUsers": [],
            "createdAt": datetime.utcnow()
        }
    
    @staticmethod
    def to_response(room: dict) -> dict:
        """
        Convert MongoDB room document to API response format
        
        Args:
            room: Room document from MongoDB
            
        Returns:
            Room data with _id converted to string and roomId added
        """
        if not room:
            return None
            
        room_copy = room.copy()
        if "_id" in room_copy:
            room_id = str(room_copy["_id"])
            room_copy["_id"] = room_id
            room_copy["roomId"] = room_id  # Add roomId for frontend compatibility
        if "deadline" in room_copy and isinstance(room_copy["deadline"], datetime):
            room_copy["deadline"] = room_copy["deadline"].isoformat()
        if "createdAt" in room_copy and isinstance(room_copy["createdAt"], datetime):
            room_copy["createdAt"] = room_copy["createdAt"].isoformat()
        
        # Convert ObjectId instances in arrays to strings
        for field in ["members", "pendingRequests", "invitedUsers"]:
            if field in room_copy and room_copy[field]:
                room_copy[field] = [str(item) if isinstance(item, ObjectId) else item for item in room_copy[field]]
        
        # Convert creatorId if it's an ObjectId
        if "creatorId" in room_copy and isinstance(room_copy["creatorId"], ObjectId):
            room_copy["creatorId"] = str(room_copy["creatorId"])
        
        # Convert teacherSupervisorId if it's an ObjectId
        if "teacherSupervisorId" in room_copy and isinstance(room_copy["teacherSupervisorId"], ObjectId):
            room_copy["teacherSupervisorId"] = str(room_copy["teacherSupervisorId"])
        
        return room_copy
