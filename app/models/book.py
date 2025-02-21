from beanie import Document
from pydantic import BaseModel
from typing import Optional

class Book(Document):
    title: str
    description: Optional[str] = None
    course: Optional[str] = None
    author_id: str  # Links to User
    author_name: str
    file_url: str

    class Settings:
        collection = "books"  # MongoDB collection name

    def dict(self, *args, **kwargs):
        """Overrides dict() to return MongoDB ID as 'id'."""
        data = super().dict(*args, **kwargs)
        data["id"] = str(self.id)
        return data
