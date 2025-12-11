# schemas.py
from pydantic import BaseModel
from typing import Optional


# How to create a book
class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None


# Scheme for updating the book
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


# Book return scheme (with ID)
class BookOut(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None

    class Config:
        from_attributes = True  # For working with SQLAlchemy models
