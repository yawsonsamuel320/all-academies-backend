from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from bson import ObjectId
from passlib.context import CryptContext
from dependencies.auth import get_current_user
from datetime import datetime, timezone

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create a new user
@router.post("/signup", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_doc = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hash_password(user.password),  # Store hashed password
        user_type=user.user_type,
        school_id=user.school_id,
        avatar=user.avatar,
        created_at=datetime.now(timezone.utc),
    )
    await user_doc.insert()
    return user_doc

@router.get("/me", response_model=User)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return current_user


@router.patch("/me", response_model=User)
async def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    """Update the currently authenticated user with only the provided fields using Beanie."""
    
    update_data = user_update.dict(exclude_unset=True)  # Only update provided fields
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided")

    # Hash the password if it is being updated
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(current_user, key, value)

    await current_user.save()  # Save the updated user document

    return await User.get(current_user.id)  # Return the updated user

# Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await User.get(ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

