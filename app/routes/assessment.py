from fastapi import APIRouter, HTTPException, Depends, status
from models.assessment import Section, SectionUpdate, Assessment
from models.user import User
from typing import List, Optional
from schemas.assessment import AssessmentCreate
from core.dependencies import get_current_contributor
from datetime import datetime, timezone

router = APIRouter()

async def create_section_instances(sections: Optional[List[Section]]):
    """Helper function to convert schema sections to model instances."""
    return [Section(**section.model_dump()) for section in sections] if sections else []

@router.post("/assessments/", response_model=Assessment)
async def create_assessment_route(
    assessment: AssessmentCreate,  # The schema for creating an assessment
    current_user: User = Depends(get_current_contributor)
):
    try:
        # Unwrap parameters from the assessment input
        section_instances = await create_section_instances(assessment.sections)

        # Create the assessment model instance
        new_assessment = Assessment(
            title=assessment.title,
            description=assessment.description,
            type=assessment.type,
            sections=section_instances,  # Pass unwrapped sections
            total_marks=assessment.total_marks,
            exam_format=assessment.exam_format,
            scheduled_at=assessment.scheduled_at,
            creator_id=str(current_user.id),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        # Insert the new assessment into the database
        await new_assessment.insert()

        return new_assessment

    except Exception as e:
        print(f"Error creating assessment: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.post("/assessments/{assessment_id}/sections", response_model=Section)
async def create_section_route(
    assessment_id: str, 
    section: Section, 
    current_user: User = Depends(get_current_contributor)
):
    try:
        # Fetch the assessment by ID
        assessment = await Assessment.get(assessment_id)
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # Create a new Section instance from the input data
        new_section = Section(**section.dict())  # This uses Pydantic's dictionary conversion

        # Append the new section to the assessment's sections list
        if assessment.sections is None:
            assessment.sections = []
        
        assessment.sections.append(new_section.dict())  # Save section as a dictionary
        
        # Save the updated assessment with the new section
        await assessment.save()

        return new_section

    except Exception as e:
        print(f"Error creating section: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")



@router.put("/assessments/{assessment_id}/sections/{section_title}", response_model=Section)
async def update_section_route(
    assessment_id: str, section_title: str, section: SectionUpdate, current_user: User = Depends(get_current_contributor)
):
    try:
        # Fetch the assessment and section from the database
        assessment = await Assessment.get(assessment_id)
        print(assessment.sections)

        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        section_to_update = next((s for s in assessment.sections if s.title == section_title), None)
        
        if not section_to_update:
            raise HTTPException(status_code=404, detail="Section not found")
        
        # Update section details
        if section.title is not None:
            section_to_update.title = section.title
        if section.description is not None:
            section_to_update.description = section.description
        if section.question_ids is not None:
            section_to_update.question_ids = section.question_ids
        assessment.updated_at = datetime.now(timezone.utc)
        await assessment.save()

        return section_to_update
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/assessments/{assessment_id}/sections/{section_id}", response_model=dict)
async def delete_section_route(
    assessment_id: str, section_id: str, current_user: User = Depends(get_current_contributor)
):
    try:
        # Fetch the assessment and remove the section by ID
        assessment = await Assessment.get(assessment_id)
        assessment.sections = [s for s in assessment.sections if s.id != section_id]

        await assessment.save()

        return {"message": "Section deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/assessments/{assessment_id}", response_model=Assessment)
async def get_assessment_route(assessment_id: str, current_user: User = Depends(get_current_contributor)):
    try:
        # Fetch the assessment by ID
        assessment = await Assessment.get(assessment_id)
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        return assessment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/assessments/{assessment_id}/sections/{section_id}", response_model=Section)
async def get_section_route(
    assessment_id: str, section_id: str, current_user: User = Depends(get_current_contributor)
):
    try:
        # Fetch the assessment and section
        assessment = await Assessment.get(assessment_id)
        section = next((s for s in assessment.sections if s.id == section_id), None)
        
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        return section
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

