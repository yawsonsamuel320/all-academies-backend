from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    question: str
    sample_answer: str
    allocated_mark: str

class QuestionGenerator(BaseModel):
    text: str
    # subject_name: str
    # number_of_questions: int
    # mode_of_questions: str