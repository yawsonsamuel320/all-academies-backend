from typing import List, Union, Optional
from pydantic import BaseModel, Field

# ✅ Base Schema for All Questions
class BaseQuestion(BaseModel):
    text: str = Field(..., title="Question Text")
    subject: str = Field(..., title="Subject")
    source: str = Field(..., title="Source", pattern="^(manual|ai-generated)$")
    topic: Optional[str] = Field(None, title="Topic")
    sub_topic: Optional[str] = Field(None, title="Subtopic")
    explanation: Optional[str] = Field(None, title="Explanation")
    difficulty: Optional[str] = Field(None, title="Difficulty Level", pattern="^(easy|medium|hard)$")
    marks: int    
# ✅ Define Each Specific Question Type
class MCQQuestion(BaseQuestion):
    type: str = "mcq"
    options: List[str]
    answer: str

class TrueFalseQuestion(BaseQuestion):
    type: str = "true_false"
    answer: bool

class FillBlankQuestion(BaseQuestion):
    type: str = "fill_blank"
    answer: str

class MatchingQuestion(BaseQuestion):
    type: str = "matching"
    pairs: List[dict]  # Example: [{"question": "2+2", "answer": "4"}]

class ShortAnswerQuestion(BaseQuestion):
    type: str = "short_answer"
    answer: str

class CalculationQuestion(BaseQuestion):
    type: str = "calculation"
    answer: float

class DiagramQuestion(BaseQuestion):
    type: str = "diagram"
    image_url: str
    answer: str

class StepwiseQuestion(BaseQuestion):
    type: str = "stepwise"
    steps: List[str]
    answer: str

class EssayQuestion(BaseQuestion):
    type: str = "essay"
    word_limit: Optional[int] = None

class CaseStudyQuestion(BaseQuestion):
    type: str = "case_study"
    passage: str
    questions: List[str]


# ✅ Union of all Question Types
QuestionType = Union[
    MCQQuestion, TrueFalseQuestion, FillBlankQuestion, MatchingQuestion,
    ShortAnswerQuestion, CalculationQuestion, DiagramQuestion, StepwiseQuestion,
    EssayQuestion, CaseStudyQuestion
]
