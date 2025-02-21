from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class QuestionResponsePair(BaseModel):
    """Question response pair"""

    id: Optional[str] = Field(description="Unique identifier for this question response pair")
    question: str = Field(description="The question from the book")
    sample_answer: str = Field(description="A sample response by the LLM")
    allocated_mark: str = Field(description="The mark allocated to the question")

