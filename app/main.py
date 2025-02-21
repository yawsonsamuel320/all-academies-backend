from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from routes.user import router as user_router
from routes.auth import router as auth_router
from routes.school.crud import router as school_router
from routes.school.teacher import router as school_teacher_router
from routes.teacher import router as teacher_router
from routes.books.author import router as book_author_router
from routes.school.student import router as school_student_router
from routes.school.academic_session import router as school_academic_session_router
from routes.question import router as question_router
from routes.school.student import router as school_student_router
from routes.assessment import router as assessment_router

from database import init_db
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
# app.include_router(question_router, prefix="/questions", tags=["Questions"])
# app.include_router(evaluation_router, prefix="/evaluations", tags=["Evaluations"])
app.include_router(user_router, prefix='/user', tags=["User"])
app.include_router(auth_router, prefix='/auth', tags=["Auth"])
app.include_router(school_router, prefix="/schools", tags=["Schools"])
app.include_router(school_teacher_router, prefix="/schools/teacher", tags=["School > Teacher"])
app.include_router(teacher_router, prefix="/teacher", tags=["Teacher"])
app.include_router(book_author_router, prefix="/book/author", tags=["Book Author"])
app.include_router(school_student_router, prefix="/school/student", tags=["School > Student"])
app.include_router(school_academic_session_router, prefix='/school/academic-session', tags=["School > Academic Session"])
app.include_router(question_router, prefix="/questions", tags=["Questions"])
app.include_router(school_student_router, prefix="/school/student", tags=["School > Student"])
app.include_router(assessment_router, prefix='/assessment', tags=["Assessment"])

@app.get("/")
def root():
    return {"message": "API is running!"}

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)