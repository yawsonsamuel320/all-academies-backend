from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.school.school import School
from models.user import User, InviteStatus
from core.dependencies import get_current_school_admin
from schemas.school.school import SchoolCreate, SchoolUpdate, SchoolResponse
from beanie import PydanticObjectId
from datetime import datetime, timezone

router = APIRouter()

# Create a new school
@router.post("/", response_model=SchoolResponse)
async def create_school(school_data: SchoolCreate, admin: User = Depends(get_current_school_admin)):
    existing_school = await School.find_one(School.email == school_data.email)
    if existing_school:
        raise HTTPException(status_code=400, detail="A school with this email already exists.")

    school = School(**school_data.model_dump(), admin_id=str(admin.id), created_at=datetime.now(timezone.utc), updated_at=datetime.utcnow())
    await school.insert()
    if not admin.school:
        admin.school = {"school_id": str(school.id), "status": InviteStatus.accepted}
        await admin.save()
    return school
    

# Get a school by ID
@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(school_id: PydanticObjectId):
    school = await School.get(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

# Update a school
@router.put("/{school_id}", response_model=SchoolResponse)
async def update_school(school_id: PydanticObjectId, school_data: SchoolUpdate):
    school = await School.get(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    update_data = school_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(school, key, value)
    
    school.updated_at = datetime.utcnow()
    await school.save()
    return school

# Delete a school
@router.delete("/{school_id}", response_model=dict)
async def delete_school(school_id: PydanticObjectId):
    school = await School.get(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    await school.delete()
    return {"message": "School deleted successfully"}
