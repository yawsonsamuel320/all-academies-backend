from pydantic import BaseModel, EmailStr, Field, HttpUrl, BeforeValidator, constr
from typing import Optional, Annotated, List
from enum import Enum
from bson import ObjectId

# Enum for user types
class UserType(str, Enum):
    student = "student"
    parent = "parent"
    school_admin = "school_admin"
    teacher = "teacher"
    moderator = "moderator"
    author = "author"
    exam_contributor = "exam_contributor"

# Custom type to handle MongoDB ObjectId conversion
PyObjectId = Annotated[str, BeforeValidator(str)]


class Subject(BaseModel):
    subject_name: str
    class_level: str

# Base schema (shared fields)
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_type: UserType
    school_id: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    # Teacher-specific fields
    subjects_taught: Optional[List[Subject]] = None
    
    # Student-specific fields
    student_index_number: Optional[str] = None  # 8-digit unique identifier
    class_level: Optional[str] = None

# Schema for creating a user (API request)
class UserCreate(UserBase):
    password: Optional[str] = Field(None, min_length=8)  # Accepts plain passwords

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    school_id: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    password: Optional[str] = Field(None, min_length=8)
    subjects_taught: Optional[List[Subject]] = None
    # Student-specific fields
    student_index_number: Optional[str] = None  # 8-digit unique identifier
    class_level: Optional[str] = None

# Schema for API response (prevents exposing password)
class UserResponse(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        from_attributes = True  # Allows auto-conversion from MongoDB objects
        populate_by_name = True  # Ensures `_id` is recognized as `id`
        json_encoders = {ObjectId: str}  # Converts ObjectId to string
 
class InviteTeacherRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    # Teacher-specific fields
    subjects_taught: Optional[List[Subject]] = None


class AcceptInviteRequest(BaseModel):
    token: str  # The invitation token sent via email

class CompleteSignupRequest(BaseModel):
    email: EmailStr  # The teacher's email (pre-filled from invite)
    first_name: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=50)]
    last_name: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=50)]
    password: Annotated[str, constr(min_length=8)]  # Enforcing a minimum password length
    # Teacher-specific fields
    subjects_taught: Optional[List[Subject]] = None
    # Student specific fields
    class_level: Optional[str] = None

