from fastapi import APIRouter, HTTPException
from models.evaluation_model import Evaluation, EvaluationRequest
from database import db
from utils.chat_model import structured_evaluator_llm

router = APIRouter()

@router.post("/")
def evaluate_response(evaluation_request: EvaluationRequest):

    
    question_attempt_pair = structured_evaluator_llm.invoke(
        f'Given the question, attempted_response, total allocated mark, and the expected response, score the user: Question: {evaluation_request.question} \nAttempted Response: {evaluation_request.attempted_response} \nExpected Response: {evaluation_request.expected_response} \nTotal Allocated Mark: {evaluation_request.allocated_mark}'
    )

    # db.evaluations.insert_one(question_attempt_pair.model_dump())

    return {"message": "Response evaluated successfully!", "evaluation": question_attempt_pair}