from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class QuestionAttemptPair(BaseModel):
    """Question response pair"""

    id: Optional[str] = Field(description="Unique identifier for this question response pair")
    question: str = Field(description="The question from the book")
    attmpted_response: str = Field(description="The attempted response by the user")
    score: str = Field(description="The mark allocated to user's attempted response over (/) the total mark")
    explantion_of_evaluation: str = Field(description="A concise reason for the allocated score")