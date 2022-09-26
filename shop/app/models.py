from datetime import datetime
from random import randint

from flask import url_for
from flask_security.models.fsqla_v2 import FsRoleMixin, FsUserMixin
from flask_security.utils import hash_password, verify_password

from db import db

def format_date(date):
    if date.day == datetime.now().day:
        return f"{date.strftime('%H:%M:%S')}"
    if date.day == datetime.now().day - 1:
        return f"tomorrow at {date.strftime('%H:%M:%S')}"
    if date.day - datetime.now().day - 1 <= 7:
        return f"{date.day - datetime.now().day}" \
               f" days ago at {date.strftime('%H:%M:%S')}"[1:]
    else:
        return f"{date.strftime('%Y-%m-%d %H:%M:%S')}"

roles_users_table = db.Table('roles_users',
                             db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                             db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, FsRoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, FsUserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users_table,
                            backref='users', lazy=True)

    orders = db.relationship('Order', backref='user', passive_deletes=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(password, self.password)


genres_books_table = db.Table('genres_books',
                              db.Column('book_id', db.Integer(), db.ForeignKey('book.id')),
                              db.Column('genre_id', db.Integer(), db.ForeignKey('genre.id')))

books_authors_table = db.Table('books_authors',
                               db.Column('book_id', db.Integer(), db.ForeignKey('book.id')),
                               db.Column('author_id', db.Integer(), db.ForeignKey('author.id')))

books_orders_table = db.Table('books_orders',
                              db.Column('book_id', db.Integer(), db.ForeignKey('book.id')),
                              db.Column('order_id', db.Integer(), db.ForeignKey('order.id')),
                              db.Column('count', db.Integer))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)

    def __str__(self):
        return self.name


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    date_of_birth = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    # image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    # file_path = db.Column(db.Text, nullable=True, default='images/default.png')

    books = db.relationship('Book', secondary=books_authors_table,
                            backref='authors', lazy=True)

    def __repr__(self):
        return "<{}:{} {}>".format(self.id, self.first_name, self.last_name)

    def __str__(self):
        return self.first_name if not self.last_name else f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        url = f'{self.first_name}_{self.last_name}' if self.last_name else self.first_name
        return url_for('main.author_detail', author_name=url)

    def colored_name(self):
        color = ('primary', 'warning', 'info')
        return color[randint(0, 2)]


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    isbn = db.Column(db.String(14), unique=True, nullable=False)
    summary = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=True)

    # image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    # file_path = db.Column(db.Text, nullable=True, default='images/default.png')

    genres = db.relationship('Genre', secondary=genres_books_table, backref='books', lazy=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return url_for('main.book_detail', isbn=self.isbn)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime(), default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    synchronized = db.Column(db.Boolean, default=False)

    books = db.relationship('Book', secondary=books_orders_table, backref='orders', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

    def __repr__(self):
        return "<{}>".format(self.id)

    def __str__(self):
        return "<{}>".format(self.id)

    def get_ordered_books_profile(self):
        return self.books if len(self.books) in range(1, 3) else self.books[:3]

    def get_formatted_date(self):
        return format_date(self.order_date)

