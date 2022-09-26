from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Text, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

from db import Base

genres_books_table = Table('genres_books', Base.metadata,
                           Column('book_id', ForeignKey('book.id')),
                           Column('genre_id', ForeignKey('genre.id')))

books_authors_table = Table('books_authors', Base.metadata,
                            Column('book_id', ForeignKey('book.id')),
                            Column('author_id', ForeignKey('author.id')))


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)

    def __str__(self):
        return self.name


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    date_of_birth = Column(Date, nullable=False)
    date_of_death = Column(Date, nullable=True)

    books = relationship('Book', secondary=books_authors_table, backref='authors', lazy=True)

    def __repr__(self):
        return "<{}:{} {}>".format(self.id, self.first_name, self.last_name)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(70), nullable=False)
    isbn = Column(String(14), unique=True, nullable=False)
    summary = Column(Text)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=True)

    genres = relationship('Genre', secondary=genres_books_table, backref='books', lazy=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)

    def __str__(self):
        return f"{self.title}"
