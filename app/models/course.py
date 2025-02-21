from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Student(BaseModel):
    student_id: str
    name: str
    email: str

class Course(Document):
    course_id: Indexed[str] = Field(unique=True)
    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "courses"