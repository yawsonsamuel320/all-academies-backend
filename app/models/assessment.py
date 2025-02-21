from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime, timezone
from schemas.assessment import Section, SectionUpdate

# ✅ Assessment Model (Covers Exams, Quizzes, Tests, Classwork)
class Assessment(Document):
    title: str
    description: Optional[str] = None
    type: str = Field(..., pattern="^(exam|quiz|test|classwork|self-assessment|practice_test)$", description="Type of assessment")
    sections: Optional[List[Section]] = None  # List of sections in this assessment
    creator_id: str  # Teacher/Contributor who created the assessment
    total_marks: Optional[int] = None
    exam_format: Optional[str] = Field(None, description="The exam format this question is associated with, e.g., 'SAT', 'WASSCE', 'IGCSE'")
    scheduled_at: Optional[datetime] = None  # If the assessment has a scheduled date/time
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        collection = "assessments"

# ✅ Student Submission Model
class AssessmentSubmission(Document):
    assessment_id: str  # Links to an assessment
    student_id: str  # ID of the student submitting
    responses: Dict[str, str]  # Question ID -> Answer mapping
    score: Optional[int] = None  # Final score after grading
    submitted_at: datetime = datetime.now(timezone.utc)
    graded_at: Optional[datetime] = None  # Timestamp when graded

    class Settings:
        collection = "assessment_submissions"
