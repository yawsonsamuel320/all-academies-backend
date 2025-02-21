from fastapi import APIRouter, HTTPException, Depends
from models.user import User, UserType
from schemas.user import UserCreate, UserResponse
from core.security import get_password_hash

router = APIRouter(prefix="/teachers")

@router.post("/register", response_model=UserResponse)
async def register_teacher(user_data: UserCreate):
    """Teacher self-registration endpoint"""
    
    # Check if email is already registered
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create teacher user
    teacher = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        user_type=UserType.teacher,
        school_id=user_data.school_id,
        subjects_taught=user_data.subjects_taught,
        is_active=False  # Must be approved by admin
    )
    
    await teacher.insert()
    return teacher
