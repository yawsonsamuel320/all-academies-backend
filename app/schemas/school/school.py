from pydantic import BaseModel, EmailStr, BeforeValidator, Field, HttpUrl
from typing import Optional, Annotated
from datetime import datetime
from bson import ObjectId

# Custom type to handle MongoDB ObjectId conversion
PyObjectId = Annotated[str, BeforeValidator(str)]

class SchoolBase(BaseModel):
    name: str
    location: str
    country: str
    email: EmailStr
    logo: Optional[HttpUrl] = None
    phone: Optional[str] = None
    status: Optional[str] = "active"  # active, pending, disabled

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    email: Optional[EmailStr] = None
    logo: Optional[HttpUrl] = None
    phone: Optional[str] = None
    status: Optional[str] = None

class SchoolResponse(SchoolBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    admin_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # To allow conversion from ORM models
        populate_by_name = True  # Ensures `_id` is recognized as `id`
        json_encoders = {ObjectId: str}  # Converts ObjectId to string