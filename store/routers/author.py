from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from repository import author
import db, schemas

router = APIRouter(
    prefix='/author',
    tags=['Author'],

)


@router.get('/', response_model=List[schemas.ShowAuthor])
def get_all(db: Session = Depends(db.get_db)):
    return author.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowAuthor)
def get_author(id: int, db: Session = Depends(db.get_db)):
    return author.get_author(id, db)


@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.AuthorEdit, db: Session = Depends(db.get_db)):
    return author.create(request, db)


@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update(id: int, request: schemas.AuthorEdit, db: Session = Depends(db.get_db)):
    return author.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(db.get_db)):
    return author.delete(id, db)