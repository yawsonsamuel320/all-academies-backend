from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone

class QuestionCollection(Document):
    title: str
    description: Optional[str] = None
    question_ids: List[str]
    contributor_id: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    visibility: str = Field(default="private", pattern="^(private|public)$", description="Visibility of the question collection, either 'private' or 'public'")

    class Settings:
        collection = "question_collections"