from fastapi import APIRouter, HTTPException, Depends, status
from schemas.question import QuestionType
from schemas.question_collection import QuestionCollection
from core.dependencies import get_current_contributor
from models.user import User
from typing import List
from models.question import Question
from models.question_collection import QuestionCollection
from beanie import PydanticObjectId

from datetime import datetime, timezone

router = APIRouter()


# ✅ Create a new question
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_question(collection_id: str, question: QuestionType, current_user: User = Depends(get_current_contributor)):
    try:
        question_doc = Question(
            question_data=question,
            contributor_id=str(current_user.id),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            collection_id=collection_id
        )
        await question_doc.insert()
        return {"message": "Question created successfully", "question_id": str(question_doc.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Get all questions
@router.get("/", response_model=List[Question])
async def get_all_questions():
    questions = await Question.find_all().to_list()
    return questions

# ✅ Get a question by ID
@router.get("/{question_id}", response_model=Question)
async def get_question(question_id: PydanticObjectId):
    question = await Question.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

# ✅ Update a question
@router.put("/{question_id}", response_model=dict)
async def update_question(
    question_id: PydanticObjectId, updated_data: QuestionType, current_user: User = Depends(get_current_contributor)
):
    question = await Question.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.contributor_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="You can only update your own questions")

    updated_data_dict = updated_data.dict(exclude_unset=True)
    updated_data_dict["updated_at"] = datetime.now(timezone.utc)  # Update timestamp

    await question.set(updated_data_dict)
    return {"message": "Question updated successfully", "question_id": str(question.id)}

# ✅ Delete a question
@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: PydanticObjectId, current_user: User = Depends(get_current_contributor)):
    question = await Question.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.contributor_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="You can only delete your own questions")

    await question.delete()
    return {"message": "Question deleted successfully"}