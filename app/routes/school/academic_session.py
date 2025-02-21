from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.school.academic_session import AcademicSession
from models.user import User
from schemas.school.academic_session import AcademicSessionCreate, AcademicSessionUpdate
from core.dependencies import get_current_school_admin

router = APIRouter()


# Create an Academic Session
@router.post("/", response_model=AcademicSession)
async def create_academic_session(
    session_data: AcademicSessionCreate, current_admin: User = Depends(get_current_school_admin)
):
    # Ensure the admin is from the correct school
    if session_data.school_id != current_admin.school["school_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to create session for this school.")

    # Check if there's already an ongoing session
    existing_session = await AcademicSession.find_one({"school_id": session_data.school_id, "status": "ongoing"})
    if existing_session:
        raise HTTPException(status_code=400, detail="An ongoing session already exists for this school.")

    # Check if end date is smaller than start date
    if session_data.end_date < session_data.start_date:
        raise HTTPException(status_code=400, detail="End date cannot be earlier than start date.")

    # Create a new session
    new_session = AcademicSession(**session_data.model_dump())
    await new_session.insert()
    return new_session

# Get all academic sessions for a school
@router.get("/{school_id}", response_model=List[AcademicSession])
async def get_academic_sessions(school_id: str):
    sessions = await AcademicSession.find({"school_id": school_id}).to_list()
    return sessions

# Update session details
@router.put("/{session_id}", response_model=AcademicSession)
async def update_academic_session(session_id: str, update_data: AcademicSessionUpdate):
    session = await AcademicSession.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Academic session not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(session, key, value)
    await session.set(update_data.model_dump())
    print(update_data)
    return session
