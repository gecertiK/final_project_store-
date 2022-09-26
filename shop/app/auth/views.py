import base64
import io
import json
import os
from functools import wraps

from flask_security.utils import hash_password
from werkzeug.utils import secure_filename

from . import auth_blueprint
from flask import request, flash, render_template, redirect, url_for, make_response, abort, send_file, current_app

from .forms import SignUpForm, SingInForm, UserForm, ChangePasswordCheckForm, ChangePasswordForm, ChangeEmailForm

from flask_security import current_user, login_required, logout_user, login_user, password_reset
from db import db
from app.models import User, Role, Author, Book, Genre, Order, books_orders_table
from app import csrf
from ..utils.security import user_datastore



# def is_owner(func):
#     @wraps(func)
#     def wrapper(route):
#         if current_user.username in route and route[(route.rfind(route)) - 1] == '/':
#             func()
#         else:
#             abort(403)
#     return wrapper

def get_basket(r):
    books = []
    if r.cookies.get('basket'):
        basket = json.loads(request.cookies.get('basket'))
        books = Book.query.filter(Book.id.in_(basket), Book.count != 0).all()
    return books


@auth_blueprint.route('/registration', methods=['post', 'get'])
@csrf.exempt
def registration():
    data = dict()
    form = SignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        data['form_is_valid'] = True
        user_datastore.create_user(
            username=form.username.data,
            email=form.email.data,
            password=hash_password(form.password.data))
        try:
            db.session.commit()
            user = User.query.filter(User.username == form.username.data).first()
            login_user(user)
            data['html_header'] = render_template('markup_components/header.html', current_user=current_user, home=True)
            flash('Successfully created new User', 'success')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            return data
        except:
            data['form_is_valid'] = False
            data['html_form'] = render_template('auth/forms/registration_form.html', form=form)
            flash('Error on User registration', 'danger')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            return data
    elif request.method == "POST":
        data['html_form'] = render_template('auth/forms/registration_form.html', form=form, validated=True)
        return data
    else:
        data['html_form'] = render_template('auth/forms/registration_form.html', form=form)
        return data

@auth_blueprint.route('/login', methods=['post', 'get'])
@csrf.exempt
def login():
    data = dict()
    form = SingInForm()
    if request.method == "POST" and form.validate_on_submit():
        data['form_is_valid'] = True
        user = User.query.filter(User.email == form.email.data).first()
        try:
            login_user(user, remember=form.remember.data)
            login_user(user)
            data['html_header'] = render_template('markup_components/header.html', current_user=current_user, home=True)
            flash('Successfully logged in', 'success')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            return data
        except:
            data['form_is_valid'] = False
            data['html_form'] = render_template('auth/forms/login_form.html', form=form)
            flash('Error on User authentication', 'danger')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            return data
    else:
        data['html_form'] = render_template('auth/forms/login_form.html', form=form)
        return data


@auth_blueprint.route('/logout')
@csrf.exempt
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'warning')
    return redirect(url_for('main.index'), 302)


@auth_blueprint.route('/change_password_check', methods=['post', 'get'])
@csrf.exempt
@login_required
def change_password_check():
    data = dict()
    form = ChangePasswordCheckForm()
    print('here1')
    if request.method == "POST" and form.validate_on_submit():
        print('here3')
        form = ChangePasswordForm()
        data['html_form'] = render_template('auth/forms/change_password_form.html', form=form)
        return data
    else:
        print('here2')
        data['html_form'] = render_template('auth/forms/change_password_check_form.html', form=form)
        return data


@auth_blueprint.route('/change_password', methods=['post', 'get'])
@csrf.exempt
@login_required
def change_password():
    data = dict()
    user = User.query.get_or_404(current_user.id)
    form = ChangePasswordForm()

    if request.method == "POST" and form.validate():
        data['form_is_valid'] = True
        user.password = hash_password(form.password.data)
        try:
            db.session.commit()
            flash('Successfully updated password data', 'success')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            return data
        except:
            data['form_is_valid'] = False
            flash('Error on password update', 'danger')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            return data
    else:
        data['html_form'] = render_template('auth/forms/change_password_form.html', form=form)
        return data


@auth_blueprint.route('/change_email', methods=['post', 'get'])
@csrf.exempt
@login_required
def change_email():
    data = dict()
    user = User.query.get_or_404(current_user.id)
    form = ChangeEmailForm()

    if request.method == "POST" and form.validate():
        data['form_is_valid'] = True
        user.email = form.email.data
        try:
            db.session.commit()
            flash('Successfully updated email data', 'success')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            data['html_profile_block'] = render_template('auth/markup_components/profile_block.html')
            return data
        except:
            data['form_is_valid'] = False
            flash('Error on email update', 'danger')
            data['html_messages_block'] = render_template('markup_components/flash_messages.html')
            return data
    else:
        data['html_form'] = render_template('auth/forms/change_email_form.html', form=form)
        return data


@auth_blueprint.route('/profile')
@login_required
def profile():

    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter(Order.user_id == current_user.id).order_by(
        Order.order_date.desc()).paginate(page=page, per_page=10)
    orders_books = db.session.query(Order, books_orders_table).filter(Order.user_id == current_user.id).join(
        books_orders_table, Order.id == books_orders_table.c.order_id).with_entities(
        books_orders_table.c.order_id, books_orders_table.c.book_id, books_orders_table.c.count).all()
    orders_books_dict = dict()
    for order, book, count in orders_books:
        if order in orders_books_dict.keys():
            orders_books_dict[order].update({book: count})
        else:
            orders_books_dict.update({order: {book: count}})
    return render_template(
        'auth/profile.html',
        user=current_user,
        orders=orders,
        user_page=True,
        basket=get_basket(request),
        orders_books=orders_books_dict
    )

# @auth_blueprint.route('/test')
# def test():
#     # f
#     orders_books = db.session.query(Order, books_orders_table).filter(Order.user_id == current_user.id).join(books_orders_table,
#                                                                                                Order.id == books_orders_table.c.order_id).all()
#     orders_books_dict = dict()
#     for ob in orders_books:
#         if ob[2] in orders_books_dict.keys():
#             orders_books_dict[ob[2]].update({ob[1]: ob[3]})
#         else:
#             orders_books_dict.update({ob[2]: {ob[1]: ob[3]}})
#     return orders_books_dict[5][11]
