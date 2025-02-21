from beanie import Document
from typing import Optional, List, Dict
from pydantic import EmailStr, HttpUrl
from core.security import get_password_hash
from enum import Enum
from datetime import datetime, timezone
from schemas.user import UserType, Subject
import random

class InviteStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"
    registered = "registered"

class User(Document):
    first_name: str
    last_name: str
    email: EmailStr
    password_hash: str  # Store only hashed passwords!
    is_active: bool = True
    is_superuser: bool = False
    user_type: UserType
    avatar: Optional[HttpUrl] = None
    created_at: datetime = datetime.now(timezone.utc)

    # School details
    school: Optional[Dict[str, str | InviteStatus]] = None  # {'school_id': str, 'status': InviteStatus}

    # Student-specific fields
    student_index_number: Optional[str] = None  # 8-digit unique identifier
    class_level: Optional[str] = None

    # Teacher-specific fields
    subjects_taught: Optional[List[Subject]] = None  # List of subjects (if teacher)
    
    # Dashboard
    events: Optional[List]

    class Settings:
        collection = "users"  

    async def set_password(self, password: str):
        """Hashes and sets the user's password."""
        self.password_hash = get_password_hash(password)
        await self.save()

    @staticmethod
    def generate_student_index():
        """Generate a unique 8-digit student index number."""
        return str(random.randint(10000000, 99999999))  # 8-digit number
    
