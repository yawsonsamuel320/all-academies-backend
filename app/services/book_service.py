import os
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from models.book import Book

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_book(title, description, subject, file: UploadFile, author):
    # Validate file type
    allowed_extensions = {"pdf", "epub", "mobi"}
    ext = file.filename.split(".")[-1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PDF, EPUB, or MOBI files are allowed")

    # Generate unique filename
    book_id = str(uuid4())
    filename = f"{book_id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file locally
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Create and save book in MongoDB
    book = Book(
        title=title,
        description=description,
        subject=subject,
        author_id=str(author.id),
        author_name=f'{author.first_name} {author.last_name}',
        file_url=file_path
    )
    await book.insert()  # Save to MongoDB

    return {"message": "Book uploaded successfully", "book": book.dict()}
