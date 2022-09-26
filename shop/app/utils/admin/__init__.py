from .views import AdminHomeView, RoleModelAdmin, UserModelAdmin, AuthorModelAdmin, BookModelAdmin, GenreModelAdmin, \
    OrderModelAdmin
from app.models import Role, User, Author, Book, Genre, Order
from app.utils.extensions import admin
from db import db


def init_admin(app):
    admin.init_app(app, index_view=AdminHomeView())

    # # if U received troubles with blueprints naming, just comment this block
    admin.add_view(RoleModelAdmin(Role, db.session))
    admin.add_view(UserModelAdmin(User, db.session))
    admin.add_view(AuthorModelAdmin(Author, db.session))
    admin.add_view(BookModelAdmin(Book, db.session))
    admin.add_view(GenreModelAdmin(Genre, db.session))
    admin.add_view(OrderModelAdmin(Order, db.session))
