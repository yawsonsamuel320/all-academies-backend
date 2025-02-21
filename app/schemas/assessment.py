from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Section(BaseModel):
    title: str
    description: Optional[str] = None
    question_ids: List[str] = []  # List of question IDs for this section
    total_marks: Optional[int] = None

class SectionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    question_ids: Optional[List[str]] = None
    total_marks: Optional[int] = None

class AssessmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: str = Field(..., pattern="^(exam|quiz|test|classwork|self-assessment|practice_test)$", description="Type of assessment")
    sections: Optional[List[Section]] = None  # List of sections in this assessment
    total_marks: Optional[int] = None
    exam_format: Optional[str] = Field(None, description="The exam format this question is associated with, e.g., 'SAT', 'WASSCE', 'IGCSE'")
    scheduled_at: Optional[datetime] = None  # If the assessment has a scheduled date/time

    class Config:
        orm_mode = True
