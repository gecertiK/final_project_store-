from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from repository import genre
import db, schemas

router = APIRouter(
    prefix='/genre',
    tags=['Genre'],

)


@router.get('/', response_model=List[schemas.ShowGenre])
def get_all(db: Session = Depends(db.get_db)):
    return genre.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowGenre)
def get_genre(id: int, db: Session = Depends(db.get_db)):
    return genre.get_genre(id, db)


@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.GenreEdit, db: Session = Depends(db.get_db)):
    return genre.create(request, db)


@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update(id: int, request: schemas.GenreEdit, db: Session = Depends(db.get_db)):
    return genre.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(db.get_db)):
    return genre.delete(id, db)