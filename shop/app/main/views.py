import json
from functools import wraps
from random import randint

from flask import render_template, make_response, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from db import db
from . import main_blueprint
from .tasks import synchronize_orders
from ..models import Book, Author, Order, books_orders_table
from ..utils.extensions import cache, csrf



# def is_owner(func):
#     @wraps(func)
#     def wrapper(id):
#         if Order.query.filter(Order.id == id).first().user_id == current_user.id:
#             func()
#         else:
#             abort(403)
#     return wrapper

def get_basket(r, additional=None):
    if r.cookies.get('basket'):
        basket = json.loads(r.cookies.get('basket'))
    else:
        basket = []
    if additional:
        basket.append(additional)
    books = Book.query.filter(Book.id.in_(basket), Book.count != 0).all()
    return books


def get_basket_rm(r, rm):
    basket = json.loads(r.cookies.get('basket'))
    basket.remove(rm)
    books = Book.query.filter(Book.id.in_(basket), Book.count != 0).all()
    return books


@main_blueprint.route('/')
def index():  # put application's code here
    page = request.args.get('page', 1, type=int)
    books_paginated = Book.query.filter(Book.count != 0).order_by(Book.id.desc()).paginate(page=page, per_page=9)
    carved_books, last_books_ids = [], []
    books = Book.query.filter(Book.count != 0).order_by(Book.id.desc()).all()

    if len(Book.query.filter(Book.count > 0).all()) >= 10:
        while len(carved_books) < 3 or len(carved_books) != len(books):
            book = books[randint(0, len(Book.query.all()) - 1)]
            if book not in carved_books:
                carved_books.append(book)

    if cache.get('last_books_ids'):
        last_books_ids = cache.get('last_books_ids')
    else:
        if len(books) % 3 == 1 or len(books) % 3 == 2:
            if len(books) % 3 == 1:
                last_books_ids.append(books[-1].id)
            else:
                last_books_ids.append(books[-1].id)
                last_books_ids.append(books[-2].id)

    return render_template('main/book_list.html',
                           books=books_paginated,
                           carved_books=carved_books,
                           last_books_ids=last_books_ids,
                           basket=get_basket(request))


@main_blueprint.route('/authors')
def authors_list():
    # cache.set("authors", Author.query.all())
    page = request.args.get('page', 1, type=int)
    authors = Author.query.filter().order_by(Author.id.desc()).paginate(page=page, per_page=10)
    return render_template('main/author_list.html', authors=authors, basket=get_basket(request))


@main_blueprint.route('/<string:isbn>')
def book_detail(isbn):
    return render_template('main/book_detail.html',
                           book=Book.query.filter(Book.isbn == isbn).first(),
                           basket=get_basket(request))


@main_blueprint.route('/author/<string:author_name>')
def author_detail(author_name):
    if '_' in author_name:
        return render_template(
            'main/author_detail.html',
            author=Author.query.filter(
                Author.first_name == author_name[:author_name.rfind('_')],
                Author.last_name == author_name[author_name.rfind('_') + 1:]).first(),
            basket=get_basket(request))
    else:
        return render_template(
            'main/author_detail.html',
            author=Author.query.filter(
                Author.first_name == author_name).first(),
            basket=get_basket(request))


@main_blueprint.route('/add_to_basket', methods=['post'])
@csrf.exempt
@login_required
def add_to_basket():
    data = dict()
    item = int(request.form.get("item"))
    basket = []
    if request.cookies.get('basket'):
        basket = json.loads(request.cookies.get('basket'))
        if item not in basket:
            basket.append(item)
        cookie = json.dumps(basket)
    else:
        cookie = json.dumps([item])
    if len(basket) > 1:
        cookie.replace(',', '\054')
    price = 0
    if request.cookies.get('basket'):
        books_cookie = json.loads(request.cookies.get('basket'))
        books_cookie.append(item)
    else:
        books_cookie = [item]
    order_books = Book.query.filter(Book.id.in_(books_cookie)).all()
    for book in order_books:
        price += book.price
    data['updated_basket'] = cookie
    data['html_basket_button'] = render_template('markup_components/basket.html', basket=get_basket(request, item))
    data['html_basket_form'] = render_template('main/forms/basket_form.html', basket=get_basket(request, item), price=round(price, 2))
    return data


@main_blueprint.route('/delete_book_basket', methods=['post'])
@csrf.exempt
@login_required
def delete_book_basket():
    data = dict()
    item = int(request.args.get("item"))
    basket = json.loads(request.cookies.get('basket'))
    if item in basket:
        basket.remove(item)
    cookie = json.dumps(basket)
    if len(basket) > 1:
        cookie.replace(',', '\054')
    price = 0
    books_cookie = json.loads(request.cookies.get('basket'))
    if books_cookie:
        order_books = Book.query.filter(Book.id.in_(books_cookie)).all()
        for book in order_books:
            price += book.price
    data['updated_basket'] = cookie
    data['html_basket_button'] = render_template('markup_components/basket.html', basket=get_basket_rm(request, item))
    data['html_basket_form'] = render_template('main/forms/basket_form.html', basket=get_basket_rm(request, item),
                                               price=round(price, 2))
    return data


@main_blueprint.route('/pay_order', methods=['get', 'post'])
@csrf.exempt
@login_required
def pay_order():
    data = dict()
    books_cookie = json.loads(request.cookies.get('basket'))
    order_books = Book.query.filter(Book.id.in_(books_cookie)).all()

    if request.method == "POST":
        form = request.form.to_dict()
        order = Order(
            price=request.form.get('price'),
            paid=True,
            user_id=current_user.id)

        try:
            db.session.add(order)
            db.session.commit()
            flash(f'Successfully payed order:{order.id}', 'success')
        except:
            flash('Error on order payment', 'danger')

        for key, value in form.items():
            if key != 'price' and int(value) != 0:
                book_order = books_orders_table.insert().values(**{
                    "book_id": int(key),
                    "order_id": int(order.id),
                    "count": int(value)
                })
                book = Book.query.filter(Book.id == key).first()
                book.count -= int(value)
                try:
                    db.session.execute(book_order)
                    db.session.commit()
                    print(f"book_id: {key}, order_id: {order.id}, count: {value} -> INSERT SUCCESS")
                except:
                    print(f"book_id: {key}, order_id: {order.id}, count: {value} -> INSERT ERROR")
        resp = make_response(redirect(url_for('main.index')))
        resp.delete_cookie("basket")
        return resp

    else:
        price = 0
        for book in order_books:
            price += book.price
        data['html_form'] = render_template('main/forms/basket_form.html', basket=get_basket(request), price=round(price, 2))
        return data


@main_blueprint.route('/order_detail/<int:id>')
@login_required
def order_detail(id):
    return {'hrml_order': render_template('main/components/order_detail_block.html', order=Order.query.filter(Order.id == id).first())}


@main_blueprint.route('/filter')
def books_filter():
    data = dict()
    books = Book.query.filter(Book.title.ilike(f"%{request.args.get('sub_string')}%")).all()
    # data['test'] = '' if not request.args.get('sub_string') else books[0].title
    max = len(books) if len(books) < 5 else 5
    data['html_filtered_books'] = render_template('main/components/filtered_books_block.html', books=books[:max])
    return data
