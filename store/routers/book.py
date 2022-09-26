from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from repository import book
import db, schemas

router = APIRouter(
    prefix='/book',
    tags=['Book'],

)


@router.get('/', response_model=List[schemas.ShowBook])
def get_all(db: Session = Depends(db.get_db)):
    return book.get_all(db)


@router.get('/{isbn}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBook)
def get_book(isbn: str, db: Session = Depends(db.get_db)):
    return book.get_book(isbn, db)


@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.BookEdit, db: Session = Depends(db.get_db)):
    return book.create(request, db)


@router.put('/{isbn}', status_code=status.HTTP_204_NO_CONTENT)
def update(isbn: str, request: schemas.BookEdit, db: Session = Depends(db.get_db)):
    return book.update(isbn, request, db)


@router.delete('/{isbn}', status_code=status.HTTP_204_NO_CONTENT)
def delete(isbn: str, db: Session = Depends(db.get_db)):
    return book.delete(isbn, db)