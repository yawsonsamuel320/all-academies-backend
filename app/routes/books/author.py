from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from services.book_service import save_book
from core.dependencies import get_current_author
from typing import Optional
from models.book import Book
from models.user import User
from typing import List
from beanie import PydanticObjectId

router = APIRouter()

@router.post("/upload/")
async def upload_book(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    file: UploadFile = File(...),
    author = Depends(get_current_author),
):
    return await save_book(title, description, subject, file, author)

@router.get("/books", response_model=List[Book])
async def list_books():
    books = await Book.find_all().to_list()
    return books

@router.get("/authors/me/books", response_model=List[Book])
async def get_author_books(author: User = Depends(get_current_author)):
    books = await Book.find({"author_id": str(author.id)}).to_list()
    return books

@router.put("/books/{book_id}", response_model=Book)
async def update_book(
    book_id: PydanticObjectId,
    title: str,
    description: str,
    author: User = Depends(get_current_author),
):
    book = await Book.get(book_id)
    if not book or book.author_id != author.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this book")

    book.title = title
    book.description = description
    await book.save()

    return book

@router.delete("/books/{book_id}")
async def delete_book(book_id: PydanticObjectId, author: User = Depends(get_current_author)):
    book = await Book.get(book_id)
    if not book or book.author_id != author.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this book")

    await book.delete()
    return {"message": "Book deleted successfully"}
