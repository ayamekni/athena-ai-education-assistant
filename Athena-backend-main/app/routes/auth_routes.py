"""
Authentication routes
"""
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime

from app.schemas.auth import LoginInput, TokenResponse
from app.schemas.student import StudentCreate
from app.schemas.teacher import TeacherCreate
from app.schemas.user import AdminCreate
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, require_role
from app.db.mongodb import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/student", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_student(student_data: StudentCreate):
    """Register a new student"""
    db = get_database()
    
    # Check if email already exists
    existing_user = await db.users.find_one({"email": student_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create user document
    hashed_password = hash_password(student_data.password)
    user_doc = {
        "email": student_data.email,
        "password": hashed_password,
        "role": "student",
        "createdAt": datetime.utcnow()
    }
    
    # Insert user
    user_result = await db.users.insert_one(user_doc)
    user_id = str(user_result.inserted_id)
    
    # Create student profile
    student_profile = {
        "userId": user_id,
        "firstName": student_data.firstName,
        "lastName": student_data.lastName,
        "institute": student_data.institute,
        "year": student_data.year,
        "speciality": student_data.speciality,
        "phone": student_data.phone,
        "skills": student_data.skills or [],
        "bio": student_data.bio,
        "links": student_data.links.dict() if student_data.links else None,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    await db.students.insert_one(student_profile)
    
    # Generate tokens
    token_data = {
        "sub": user_id,
        "email": student_data.email,
        "role": "student"
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user_id,
            "email": student_data.email,
            "role": "student",
            "firstName": student_data.firstName,
            "lastName": student_data.lastName
        }
    )


@router.post("/register/teacher", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_teacher(teacher_data: TeacherCreate):
    """Register a new teacher"""
    db = get_database()
    
    # Check if email already exists
    existing_user = await db.users.find_one({"email": teacher_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create user document
    hashed_password = hash_password(teacher_data.password)
    user_doc = {
        "email": teacher_data.email,
        "password": hashed_password,
        "role": "teacher",
        "createdAt": datetime.utcnow()
    }
    
    # Insert user
    user_result = await db.users.insert_one(user_doc)
    user_id = str(user_result.inserted_id)
    
    # Create teacher profile
    teacher_profile = {
        "userId": user_id,
        "firstName": teacher_data.firstName,
        "lastName": teacher_data.lastName,
        "teaching": teacher_data.teaching,
        "institute": teacher_data.institute,
        "phone": teacher_data.phone,
        "availability": teacher_data.availability.dict() if teacher_data.availability else None,
        "bio": teacher_data.bio,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    await db.teachers.insert_one(teacher_profile)
    
    # Generate tokens
    token_data = {
        "sub": user_id,
        "email": teacher_data.email,
        "role": "teacher"
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user_id,
            "email": teacher_data.email,
            "role": "teacher",
            "firstName": teacher_data.firstName,
            "lastName": teacher_data.lastName
        }
    )


@router.post("/register/admin", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_admin(
    admin_data: AdminCreate,
    current_user: dict = Depends(require_role(["admin"]))
):
    """Register a new admin (only accessible by existing admins)"""
    db = get_database()
    
    # Check if email already exists
    existing_user = await db.users.find_one({"email": admin_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create admin user document
    hashed_password = hash_password(admin_data.password)
    user_doc = {
        "email": admin_data.email,
        "password": hashed_password,
        "role": "admin",
        "createdAt": datetime.utcnow()
    }
    
    # Insert user
    user_result = await db.users.insert_one(user_doc)
    user_id = str(user_result.inserted_id)
    
    # Generate tokens
    token_data = {
        "sub": user_id,
        "email": admin_data.email,
        "role": "admin"
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user_id,
            "email": admin_data.email,
            "role": "admin"
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginInput):
    """Login endpoint for all user types"""
    try:
        print(f"🔐 Login attempt for: {credentials.email}")
        db = get_database()
        
        # Find user by email
        user = await db.users.find_one({"email": credentials.email})
        
        if not user:
            print(f"❌ User not found: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        print(f"✅ User found: {credentials.email}, role: {user.get('role')}")
        
        # Verify password
        if not verify_password(credentials.password, user["password"]):
            print(f"❌ Invalid password for: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        print(f"✅ Password verified for: {credentials.email}")
        
        user_id = str(user["_id"])
        role = user["role"]
        
        # Get profile data based on role
        user_info = {
            "id": user_id,
            "email": user["email"],
            "role": role
        }
        
        if role == "student":
            profile = await db.students.find_one({"userId": user_id})
            if profile:
                user_info["firstName"] = profile.get("firstName")
                user_info["lastName"] = profile.get("lastName")
        elif role == "teacher":
            profile = await db.teachers.find_one({"userId": user_id})
            if profile:
                user_info["firstName"] = profile.get("firstName")
                user_info["lastName"] = profile.get("lastName")
        
        # Generate tokens
        token_data = {
            "sub": user_id,
            "email": user["email"],
            "role": role
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        print(f"✅ Login successful for: {credentials.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user_info
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
