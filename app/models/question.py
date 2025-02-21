from beanie import Document
from typing import Union
from schemas.question import QuestionType
from datetime import datetime, timezone
from pydantic import Field

# ✅ Define Beanie ODM Model for Exam Questions
class Question(Document):
    contributor_id: str
    question_data: QuestionType  # ✅ Store full question object dynamically
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    collection_id: str

    class Settings:
        collection = "questions"
