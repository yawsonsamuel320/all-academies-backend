from beanie import Document
from typing import Literal
from datetime import datetime

class AcademicSession(Document):
    school_id: str
    session_type: Literal["semester", "trimester"]
    start_date: datetime
    end_date: datetime
    status: Literal["upcoming", "ongoing", "completed"] = "upcoming"

    class Settings:
        collection = "academic_sessions"
