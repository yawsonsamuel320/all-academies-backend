from pydantic import BaseModel
from typing import Optional

class EvaluationRequest(BaseModel):
    question: str
    expected_response: str
    attempted_response: str
    allocated_mark: int

class Evaluation(BaseModel):
    question: str
    attempted_response: str
    score: str
    explanation: str