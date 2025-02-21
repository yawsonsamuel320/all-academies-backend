from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from models.user import User, InviteStatus
from models.school.school import School
from schemas.user import UserType, InviteTeacherRequest, AcceptInviteRequest, CompleteSignupRequest
from core.dependencies import get_current_school_admin
from core.security import create_access_token, verify_access_token
from utils.email import send_invite_email
from core.config import FRONTEND_URL
from bson import ObjectId

router = APIRouter()

@router.post("/{school_id}/invite-teacher")
async def invite_teacher(
    school_id: str, 
    request: InviteTeacherRequest, 
    background_tasks: BackgroundTasks, 
    admin: User = Depends(get_current_school_admin)
):
    """Only school admins can invite teachers"""

    email = request.email
    subjects_taught = request.subjects_taught

    # Get school_name
    school = await School.find_one(School.id == ObjectId(school_id))
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    # Check if the user already exists
    existing_user = await User.find_one(User.email == email)


    if existing_user:
        if existing_user.user_type != UserType.teacher:
            raise HTTPException(status_code=400, detail="User is not registered as a teacher")
        
        # If the teacher already belongs to a school
        if existing_user.school:
            if (existing_user.school['school_id'] == school_id) and (existing_user.school.get("status") in [InviteStatus.accepted, InviteStatus.registered]):
                raise HTTPException(status_code=400, detail="Teacher is already linked to a school")

        # Update invite status and notify them
        existing_user.school = {"school_id": school_id, "status": InviteStatus.pending}

        invite_token = create_access_token(
            {"email": email, 
             "school_id": school_id, 
             "subjects_taught": [subject.model_dump() for subject in existing_user.subjects_taught] + [subject.model_dump() for subject in subjects_taught]})
        invite_link = f"{FRONTEND_URL}/accept-invite?token={invite_token}"

        await existing_user.save()

        # Send email and app notification
        background_tasks.add_task(send_invite_email, 
                                  email=email, 
                                  school_name=school.name, 
                                  invite_link=invite_link,  
                                  first_name=request.first_name, 
                                  role="teacher", 
                                  subjects_taught=subjects_taught,)
        

        return {"message": "Invitation sent to existing user. Awaiting teacher confirmation.", "token": invite_token}

    invite_token = create_access_token({"email": email, "school_id": school_id, "subjects_taught": [subject.model_dump() for subject in subjects_taught]})
    invite_link = f"{FRONTEND_URL}/accept-invite?token={invite_token}"
    
    # User does not exist → Create entry with `pending` invite status
    new_teacher = User(
        first_name=request.first_name or "",
        last_name=request.last_name or "",
        email=email,
        password_hash="",  # They will set their password later
        is_active=False,
        is_superuser=False,
        user_type=UserType.teacher,
        subjects_taught=subjects_taught,
        school={"school_id": school_id, "status": InviteStatus.pending}
    )
    await new_teacher.insert()

    # Send email and app notification
    background_tasks.add_task(send_invite_email, 
                                email=email, 
                                school_name=school.name, 
                                invite_link=invite_link,  
                                first_name=request.first_name, 
                                role="teacher", 
                                subjects_taught=subjects_taught,)


    return {"message": "Invitation sent successfully. Awaiting teacher confirmation."}
    

@router.post("/auth/accept-invite")
async def accept_invite(request: AcceptInviteRequest):
    token_data = verify_access_token(request.token)  # Decodes token
    email = token_data.get("email")
    school_id = token_data.get("school_id")
    subjects_taught = token_data.get("subjects_taught")

    # Fetch user from the database
    teacher = await User.find_one(User.email == email)

    if not teacher or teacher.school["school_id"] != school_id:
        raise HTTPException(status_code=400, detail="Invalid or expired invite")

    if teacher.school["status"] == InviteStatus.accepted:
        raise HTTPException(status_code=400, detail="Invite already accepted")

    # Update the teacher's invite status to accepted
    teacher.school["status"] = InviteStatus.accepted

    # Update the subjects taught
    teacher.subjects_taught = subjects_taught
    await teacher.save()

    # Allow teacher to proceed to set up their account
    return teacher.model_dump()


@router.delete("/{school_id}/delete-teacher/{teacher_id}")
async def delete_teacher(
    school_id: str, 
    teacher_id: str, 
    admin: User = Depends(get_current_school_admin)
):
    """Only school admins can delete teachers"""

    # Ensure the requester is a school admin
    if admin.user_type != UserType.school_admin and admin.school.school_id == school_id:
        raise HTTPException(status_code=403, detail="Only school admins can delete teachers")

    # Fetch the teacher from the database
    teacher = await User.find_one({"_id": ObjectId(teacher_id), "school.school_id": school_id})

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Delete the teacher
    await teacher.delete()

    return {"message": "Teacher deleted successfully"}

@router.put("/{school_id}/update-teacher/{teacher_id}")
async def update_teacher(
    school_id: str, 
    teacher_id: str, 
    request: CompleteSignupRequest, 
    admin: User = Depends(get_current_school_admin)
):
    """Only school admins can update teacher details"""

    # Ensure the requester is a school admin
    if admin.user_type != UserType.school_admin and admin.school.school_id == school_id:
        raise HTTPException(status_code=403, detail="Only school admins can update teacher details")

    # Fetch the teacher from the database
    teacher = await User.find_one({"_id": ObjectId(teacher_id), "school.school_id": school_id})

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Update teacher details
    teacher.first_name = request.first_name
    teacher.last_name = request.last_name