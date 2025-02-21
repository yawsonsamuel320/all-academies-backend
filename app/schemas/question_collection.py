from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone

class Section(Document):
    title: str
    description: Optional[str] = None  # Preamble for the section
    question_ids: List[str]  # List of question IDs associated with this section

class QuestionCollection(Document):
    title: str = Field(..., min_length=3, max_length=100, description="Title of the question collection")
    description: Optional[str] = Field(None, max_length=500, description="Brief description of the collection")
    question_ids: List[str] = Field(default=[], description="List of question IDs included in the collection")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when the collection was created")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when the collection was last updated")
    visibility: str = Field(default="private", pattern="^(private|public)$", description="Collection visibility: 'private' or 'public'")
    contributor_id: str

    class Settings:
        collection = "question_collections"

    class Config:
        schema_extra = {
            "example": {
                "title": "Geography Revision Questions",
                "description": "A collection of geography questions for final exams",
                "question_ids": ["656f7d5c4b2e3a001c0f1a5d", "656f7d5c4b2e3a001c0f1a5e"],
                "created_at": "2024-02-17T12:00:00Z",
                "updated_at": "2024-02-17T12:00:00Z",
                "visibility": "private"
            }
        }
