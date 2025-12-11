from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import database

# Create tables in database
models.Base.metadata.create_all(bind=database.engine)

# Initialize the FastAPI application
app = FastAPI(
    title="Book Collection API",
    description="API to manage your book collection",
    version="1.0.0"
)


# Function-dependent to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/", tags=["Root"])
def read_root():
    """
    Root Endpoint - API information
    """
    return {
        "message": "WELCOME Book Collection API!",
    }



@app.post(
    "/books/",
    response_model=schemas.BookOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
    summary="Add new book"
)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    """
    Add new book to collection

    - **title**: Book title (required)
    - **author**: Author of the book (required)
    - **year**: Year of publication (optional)
    """
    # Create a book object from data
    db_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year
    )

    # Add to DB
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book



@app.get(
    "/books/",
    response_model=List[schemas.BookOut],
    tags=["Books"],
    summary="Get all books"
)
def get_books(
        skip: int = Query(0, ge=0, description="Skip N entries"),
        limit: int = Query(100, ge=1, le=100, description="Record limit"),
        db: Session = Depends(get_db)
):
    """
    Get a list of all books in the collection

    Supports inclusion:
    - **skip**: How many entries to skip
    - **limit**: Maximum number of entries (1-100)
    """
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books



@app.get(
    "/books/{book_id}",
    response_model=schemas.BookOut,
    tags=["Books"],
    summary="Get the book by ID"
)
def get_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    """
    Get information about a specific book by its ID
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id}  not found"
        )

    return book



@app.put(
    "/books/{book_id}",
    response_model=schemas.BookOut,
    tags=["Books"],
    summary="Update information about the book"
)
def update_book(
        book_id: int,
        book_update: schemas.BookUpdate,
        db: Session = Depends(get_db)
):
    """
    Update information about the book

    You can update any field (title, author, year)
    """
    # Find book
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id}  not found"
        )


    update_data = book_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return book



@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="Delete book"
)
def delete_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    """
    Remove book from collection by ID
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id}  not found"
        )

    db.delete(book)
    db.commit()

    return None  # 204 No Content


@app.get(
    "/books/search/",
    response_model=List[schemas.BookOut],
    tags=["Search"],
    summary="Search book"
)
def search_books(
        title: Optional[str] = Query(None, description="Book title (partial match)"),
        author: Optional[str] = Query(None, description="Author of the book (partial match)"),
        year: Optional[int] = Query(None, description="Year of publication (exact match)"),
        db: Session = Depends(get_db)
):
    """
    Search books by title, author or year

    - **title**: Search by part of the name
    - **author**: Search by part of the author name
    - **year**: Search by exact year of publication
    """
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))

    if year is not None:
        query = query.filter(models.Book.year == year)

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Books by given criteria not found"
        )

    return results



@app.get("/health", tags=["Health"])
def health_check():
    """
    API Health Check
    """
    return {
        "status": "healthy",
        "service": "Book Collection API",
        "timestamp": "Error"
    }