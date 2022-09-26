from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import schemas
from models import Book


def get_all(db: Session):
    books = db.query(Book).all()
    return books


def get_book(isbn: str, db: Session):
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Book with isbn {isbn} not available"})
    return book


def create(request: schemas.BookEdit, db: Session):
    book = db.query(Book).filter(Book.isbn == request.isbn).first()
    if book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Book with isbn {request.isbn} exists"})
    book = Book(**request.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update(isbn: str, request: schemas.BookEdit, db: Session):
    book = db.query(Book).filter(Book.isbn == isbn)
    if not book.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Book with isbn {isbn} not found"})
    book.update(request.dict())
    db.commit()
    return book.first()


def delete(isbn: str, db: Session):
    book = db.query(Book).filter(Book.isbn == isbn)
    if not book.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Book with isbn {isbn} not found"})
    book.delete(synchronize_session=False)
    db.commit()
    return f"Book with isbn {isbn} successfully deleted"
