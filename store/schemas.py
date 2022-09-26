from datetime import date
from typing import List, Text, Optional

from fastapi import Query
from pydantic import BaseModel, validator, Field, constr


class AuthorBase(BaseModel):
    first_name: str = Field(..., max_length=40)
    last_name: Optional[constr(max_length=40)]
    date_of_birth: date = ...
    date_of_death: Optional[date]

    class Config:
        orm_mode = True

    @validator('date_of_birth', 'date_of_death')
    def date_in_future(cls, v):
        if v and type(v) != 'NoneType':
            if v > date.today():
                raise ValueError('Data can\'t be in future')
        return v

    @validator('date_of_death')
    def death_to_birth(cls, v, values, **kwargs):
        if v and type(v) != 'NoneType':
            if 'date_of_birth' in values and v > values['date_of_birth']:
                raise ValueError('Date of death cant be earlier than date of birth')
        return v


class BookBase(BaseModel):
    isbn: str = Field(..., min_length=13, max_length=13)
    title: str = Field(..., max_length=70)
    summary: str = ...
    price: float = ...
    count: int = 0

    class Config:
        orm_mode = True


class GenreBase(BaseModel):
    name: str = Field(..., max_length=40)

    class Config:
        orm_mode = True


class ShowAuthor(AuthorBase):
    books: List[BookBase] = []


class ShowBook(BookBase):
    authors: List[AuthorBase] = []
    genres: List[GenreBase] = []


class ShowGenre(GenreBase):
    books: List[BookBase] = []


class AuthorEdit(AuthorBase):
    pass


class GenreEdit(GenreBase):
    pass


class BookEdit(BookBase):
    pass


class OrderBase(BaseModel):
    isbn: str = Field(..., min_length=13, max_length=13)
    count: int = ...


class OrderUpdate(BaseModel):
    orders: List[OrderBase]
