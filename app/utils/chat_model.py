from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from schemas.question_response_set import QuestionResponseSet
from schemas.question_attempt_pair import QuestionAttemptPair

load_dotenv()

model_name = 'llama-3.3-70b-versatile'

llm = ChatGroq(temperature=0, 
               model_name=model_name,
               api_key=os.getenv('GROQ_API_KEY'))

structured_llm = llm.with_structured_output(QuestionResponseSet)


evaluator_model_name = 'llama-3.3-70b-versatile'
evaluator_llm = ChatGroq(temperature=0, 
               model_name=evaluator_model_name,
               api_key=os.getenv('GROQ_API_KEY'))

structured_evaluator_llm = evaluator_llm.with_structured_output(QuestionAttemptPair)
