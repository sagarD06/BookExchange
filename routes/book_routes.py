from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from auth import verify_api_key
from database import get_session
from models.book_model import Book, BookCreate, BookRead

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookRead])
def get_books(
    session: Annotated[Session, Depends(get_session)],
    title: str | None = Query(None, description="Filter books by title"),
    author: str | None = Query(None, description="Filter books by author"),
    price_min: float | None = Query(
        None, description="Filter books with price greater than or equal to this value"
    ),
    price_max: float | None = Query(
        None, description="Filter books with price less than or equal to this value"
    ),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(
        10, description="Maximum number of records to return for pagination"
    ),
):
    """Retrieve all books from the database."""
    query = select(Book).where(
        Book.is_sold == False
    )  # Default filter to only show unsold books

    if title:
        query = query.where(Book.title == title)

    if author:
        query = query.where(Book.author == author)

    if price_min is not None:
        query = query.where(Book.price >= price_min)

    if price_max is not None:
        query = query.where(Book.price <= price_max)

    query = query.offset(skip).limit(limit)

    books = session.exec(query).all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found")

    return books


@router.post("/", response_model=BookRead)
def create_book(
    book: BookCreate,
    session: Annotated[Session, Depends(get_session)],
    api_key: str = Depends(verify_api_key),
):
    """Create a new book in the database."""
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    book_update: BookCreate,
    session: Annotated[Session, Depends(get_session)],
    api_key: str = Depends(verify_api_key),
):
    """Update an existing book in the database."""
    db_book = session.get(Book, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    book = book_update.model_dump(exclude_unset=True)

    for key, value in book.items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.patch("/{book_id}/mark_sold", response_model=BookRead)
def mark_book_as_sold(
    book_id: int,
    session: Annotated[Session, Depends(get_session)],
    api_key: str = Depends(verify_api_key),
):
    """Mark a book as sold in the database."""
    db_book = session.get(Book, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.is_sold = True
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.delete("/{book_id}", response_model=dict)
def delete_book(
    book_id: int,
    session: Annotated[Session, Depends(get_session)],
    api_key: str = Depends(verify_api_key),
):
    """Delete a book from the database."""
    db_book = session.get(Book, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(db_book)
    session.commit()
    return {"message": "Book deleted successfully"}
