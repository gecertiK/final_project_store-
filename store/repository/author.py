from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import schemas
from models import Author


def get_all(db: Session):
    authors = db.query(Author).all()
    return authors


def get_author(id: int, db: Session):
    author = db.query(Author).filter(Author.id == id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Author with id {id} not available"})
    return author


def create(request: schemas.AuthorEdit, db: Session):
    author = Author(**request.dict())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update(id: int, request: schemas.AuthorEdit, db: Session):
    author = db.query(Author).filter(Author.id == id)
    if not author.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Author with id {id} not found"})
    author.update(request.dict())
    db.commit()
    return author.first()


def delete(id: int, db: Session):
    author = db.query(Author).filter(Author.id == id)
    if not author.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Author with id {id} not found"})
    author.delete(synchronize_session=False)
    db.commit()
    return f"Author with id {id} successfully deleted"
