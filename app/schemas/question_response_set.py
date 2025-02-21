from pydantic import BaseModel, Field
from typing import Optional, List
from utils.uuid_generator import generate_uuid
from utils.prompt import prompt

from schemas.question_response_pair import QuestionResponsePair

class QuestionResponseSet(BaseModel):
    """Question response set"""
    id: Optional[str] = Field(description="Unique id for this question response set")
    set: List[QuestionResponsePair] = Field(description="This is the question response set")

