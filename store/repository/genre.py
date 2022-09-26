from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import schemas
from models import Genre


def get_all(db: Session):
    genres = db.query(Genre).all()
    return genres


def get_genre(id: int, db: Session):
    genre = db.query(Genre).filter(Genre.id == id).first()
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Genre with id {id} not available"})
    return genre


def create(request: schemas.GenreEdit, db: Session):
    genre = Genre(**request.dict())
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


def update(id: int, request: schemas.GenreEdit, db: Session):
    genre = db.query(Genre).filter(Genre.id == id)
    if not genre.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Genre with id {id} not found"})
    genre.update(request.dict())
    db.commit()
    return genre.first()


def delete(id: int, db: Session):
    genre = db.query(Genre).filter(Genre.id == id)
    if not genre.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"detail": f"Genre with id {id} not found"})
    genre.delete(synchronize_session=False)
    db.commit()
    return f"Genre with id {id} successfully deleted"
