from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
import os

# Import models
from models.user import User
from models.student import Student
from models.school.school import School
from models.book import Book
from models.school.academic_session import AcademicSession
from models.question import Question
from models.assessment import Assessment

load_dotenv()

uri = os.environ.get("DB_URL")

async def init_db():
    client = AsyncIOMotorClient(uri)
    database = client.all_academies  # Use the correct database name

    # Initialize Beanie with the models
    await init_beanie(database, document_models=[User, Student, School, Book, AcademicSession, Question, Assessment])
