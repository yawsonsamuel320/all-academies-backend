from models.user import User
from typing import Optional, List

# MongoDB Document for Students (Extends User)
class Student(User):
    program_of_study: Optional[str] = None
    education_level: Optional[str] = None
    courses: Optional[List[str]] = None

    class Settings:
        collection = "students"