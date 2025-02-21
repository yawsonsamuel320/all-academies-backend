from beanie import Document
from typing import Optional
from pydantic import EmailStr, HttpUrl
from datetime import datetime, timezone

class School(Document):
    name: str
    location: str
    country: str
    email: EmailStr
    phone: Optional[str] = None
    admin_id: str  # Reference to the User (school admin)
    logo: Optional[HttpUrl] = None
    status: str = "active"  # active, pending, disabled
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        collection = "schools"

    async def update_timestamp(self):
        """Updates the timestamp whenever school details are modified."""
        self.updated_at = datetime.now(timezone.utc)
        await self.save()
