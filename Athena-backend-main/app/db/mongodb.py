"""
MongoDB connection and database management
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from typing import Optional


class MongoDB:
    """MongoDB connection manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Establish connection to MongoDB Atlas"""
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGO_URI)
        mongodb.db = mongodb.client[settings.DATABASE_NAME]
        
        # Test the connection
        await mongodb.client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        print("🔌 MongoDB connection closed")


async def create_indexes():
    """Create database indexes for better query performance"""
    if mongodb.db is not None:
        # Unique index on user email
        await mongodb.db.users.create_index("email", unique=True)
        
        # Index on role for faster filtering
        await mongodb.db.users.create_index("role")
        
        # Index on userId in student and teacher profiles
        await mongodb.db.students.create_index("userId", unique=True)
        await mongodb.db.teachers.create_index("userId", unique=True)
        
        # Indexes for rooms collection
        await mongodb.db.rooms.create_index("creatorId")
        await mongodb.db.rooms.create_index("type")
        await mongodb.db.rooms.create_index("members")
        await mongodb.db.rooms.create_index("teacherSupervisorId")
        await mongodb.db.rooms.create_index("createdAt")
        
        print("✅ Database indexes created")


def get_database() -> AsyncIOMotorDatabase:
    """Get the database instance"""
    if mongodb.db is None:
        raise Exception("Database not initialized")
    return mongodb.db
