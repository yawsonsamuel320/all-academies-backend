from fastapi import APIRouter, HTTPException, Depends, status
from schemas.question import QuestionType
from schemas.question_collection import QuestionCollection
from core.dependencies import get_current_contributor
from models.user import User
from typing import List
from models.question import Question
from models.question_collection import QuestionCollection
from beanie import PydanticObjectId

from datetime import datetime, timezone

router = APIRouter()

# Create a new question collection
@router.post("/", response_model=QuestionCollection, status_code=status.HTTP_201_CREATED)
async def create_collection(collection: QuestionCollection):
    collection.created_at = datetime.now(timezone.utc)
    collection.updated_at = datetime.now(timezone.utc)
    await collection.insert()
    return collection

# Get all question collections
@router.get("/", response_model=List[QuestionCollection])
async def get_all_collections():
    collections = await QuestionCollection.find_all().to_list()
    return collections

# Get a single question collection by ID
@router.get("/{collection_id}", response_model=QuestionCollection)
async def get_collection(collection_id: PydanticObjectId):
    collection = await QuestionCollection.get(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

# Update a question collection
@router.put("/{collection_id}", response_model=QuestionCollection)
async def update_collection(collection_id: PydanticObjectId, updated_data: QuestionCollection):
    collection = await QuestionCollection.get(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    updated_data.updated_at = datetime.now(timezone.utc)  # Update timestamp
    await collection.set(updated_data.dict(exclude_unset=True))
    return collection

# Delete a question collection
@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: PydanticObjectId):
    collection = await QuestionCollection.get(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    await collection.delete()
    return {"message": "Collection deleted successfully"}
