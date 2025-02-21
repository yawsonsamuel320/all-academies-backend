from fastapi import APIRouter, HTTPException
from models.question_model import Question
from database import db
from utils.mongo_db_helper import mongo_obj_to_dict
from models.question_model import QuestionGenerator
from schemas.question_response_set import QuestionResponseSet, QuestionResponsePair
from utils.chat_model import structured_llm
from utils.prompt import prompt
from utils.uuid_generator import generate_uuid

router = APIRouter()

@router.post("/generate")
def generate_question(question_generator: QuestionGenerator):
    question_response_set = structured_llm.invoke(prompt.format(input=question_generator.text))

    question_response_set = QuestionResponseSet(
        id=generate_uuid(),
        set=[
            QuestionResponsePair(
                id=generate_uuid(),
                question=pair.question,
                sample_answer=pair.sample_answer,
                allocated_mark=pair.allocated_mark
            )

            for pair in question_response_set.set
        ]
    )
    return question_response_set


@router.post("/")
def create_question(question: Question):
    db.questions.insert_one(question.model_dump())
    return {"message": "Question created successfully!", "question": question}

@router.get("/")
def get_questions():
    questions = list(db.questions.find())
    questions = mongo_obj_to_dict(questions)
    return {"questions": questions}