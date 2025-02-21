from fastapi import APIRouter, HTTPException, Path, Depends, BackgroundTasks
from beanie import PydanticObjectId
from models.user import User, InviteStatus
from schemas.user import UserType, AcceptInviteRequest, UserUpdate
from typing import List, Optional
from core.config import FRONTEND_URL

from core.dependencies import get_current_school_admin
from core.security import create_access_token, verify_access_token

from pydantic import BaseModel, EmailStr
from bson import ObjectId
from utils.email import send_invite_email
from models.school.school import School

router = APIRouter()

class InviteStudentRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    school_id: str
    class_level: str

@router.post("/invite-student")
async def invite_student(request: InviteStudentRequest, background_tasks: BackgroundTasks, admin: User = Depends(get_current_school_admin)
):
    """Invite a student via email."""
    # Get school_name
    school = await School.find_one(School.id == ObjectId(request.school_id))
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Check if the user already exists
    existing_user = await User.find_one(User.email == request.email)

    if existing_user:
        if existing_user.user_type != UserType.student:
            raise HTTPException(status_code=400, detail="User is not registered as a student")
        
        # If the teacher already belongs to a school
        if existing_user.school:
            if (existing_user.school['school_id'] == request.school_id) and (existing_user.school.get("status") in [InviteStatus.accepted, InviteStatus.registered]):
                raise HTTPException(status_code=400, detail="Student is already linked to a school")

        # Update invite status and notify them
        existing_user.school = {"school_id": request.school_id, "status": InviteStatus.pending}

        invite_token = create_access_token({"email": request.email, 
                                            "first_name": request.first_name,
                                            "last_name": request.last_name,
                                            "school_id": request.school_id, "class_level": request.class_level})

        invite_link = f"{FRONTEND_URL}/accept-invite?token={invite_token}"
        
        await existing_user.save()

        # Send email 
        background_tasks.add_task(
            send_invite_email,
            email=request.email,
            school_name=school.name,
            invite_link=invite_link,
            first_name=request.first_name,
            role="student",
            class_level=request.class_level
        )
        
        # TODO: Send app notification

        return {"message": "Invitation sent to existing user. Awaiting teacher confirmation.", "token": invite_token}
    else:
    
        invite_token = create_access_token({"email": request.email, "school_id": request.school_id, "class_level": request.class_level})

        invite_link = f"{FRONTEND_URL}/accept-invite?token={invite_token}"
        
        # Create a student record in the database
        student = User(
            first_name=request.first_name or "",
            last_name=request.last_name or "",
            email=request.email,
            password_hash="",
            is_active=False,
            is_superuser=False,
            user_type=UserType.student,
            school={"school_id": request.school_id, "status": InviteStatus.pending},
            invite_status=InviteStatus.pending,
            class_level=request.class_level
        )
        await student.insert()

        # Send email
        background_tasks.add_task(
            send_invite_email,
            email=request.email,
            school_name=school.name,
            invite_link=invite_link,
            first_name=request.first_name,
            role="student",
            class_level=request.class_level
        )

        return {"message": "Student invitation sent successfully"}

@router.post("/auth/accept-invite")
async def accept_invite(request: AcceptInviteRequest):
    token_data = verify_access_token(request.token)  # Decodes token
    email = token_data.get("email")
    school_id = token_data.get("school_id")
    class_level = token_data.get("class_level")

    # Fetch user from the database
    student = await User.find_one(User.email == email)

    if not student or student.school["school_id"] != school_id:
        raise HTTPException(status_code=400, detail="Invalid or expired invite")

    if student.school["status"] == InviteStatus.accepted:
        raise HTTPException(status_code=400, detail="Invite already accepted")

    # Update the teacher's invite status to accepted
    student.school["status"] = InviteStatus.accepted

    # Update the class_level
    student.class_level = class_level
    await student.save()

    # Allow teacher to proceed to set up their account
    return student.model_dump()

@router.get("/school/{school_id}/students", response_model=List[User])
async def get_students_by_school(school_id: str = Path(...), school_admin: User = Depends(get_current_school_admin)):
    if str(school_admin.school['school_id']) != school_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this school's students")
    try:
        school_id = PydanticObjectId(school_id)  # Convert manually
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid school_id format")

    students = await User.find({"school.school_id": str(school_id), "user_type": "student"}).to_list()
    
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    
    return students


@router.delete("/school/{school_id}/students/{student_id}")
async def delete_student(school_id: str, student_id: str, school_admin: User = Depends(get_current_school_admin)):
    if str(school_admin.school['school_id']) != school_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this student")

    student = await User.find_one(User.id == ObjectId(student_id), User.user_type == UserType.student)
    if not student or str(student.school['school_id']) != school_id:
        raise HTTPException(status_code=404, detail="Student not found")

    await student.delete()
    return {"message": "Student deleted successfully"}




@router.put("/school/{school_id}/students/{student_id}")
async def update_student(school_id: str, student_id: str, request: UserUpdate, school_admin: User = Depends(get_current_school_admin)):
    if str(school_admin.school['school_id']) != school_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this student")

    student = await User.find_one(User.id == ObjectId(student_id), User.user_type == UserType.student)
    if not student or str(student.school['school_id']) != school_id:
        raise HTTPException(status_code=404, detail="Student not found")

    if request.first_name is not None:
        student.first_name = request.first_name
    if request.last_name is not None:
        student.last_name = request.last_name
    if request.class_level is not None:
        student.class_level = request.class_level

    await student.save()
    return {"message": "Student updated successfully", "student": student.model_dump()}