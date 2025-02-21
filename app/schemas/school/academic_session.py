from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class AcademicSessionCreate(BaseModel):
    school_id: str
    session_type: Literal["semester", "trimester"]
    start_date: datetime
    end_date: datetime

class AcademicSessionUpdate(BaseModel):
    session_type: Optional[Literal["semester", "trimester"]] = None
