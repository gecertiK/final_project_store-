import json

import requests
from celery import shared_task
from sqlalchemy import func

from app.models import books_authors_table, genres_books_table, books_orders_table, Author, Book, Genre, Order
from app.utils.extensions import celery
from db import db


color = lambda x, y, z: ";".join([str(x), str(y), str(z)])

red = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 31, 40), x)
green = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 32, 40), x)
yellow = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 33, 40), x)
blue = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 34, 40), x)
purple = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 35, 40), x)
cyan = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 36, 40), x)

selected_color = lambda x, y: '\x1b[%sm%s\x1b[0m' % (y, x)


@celery.task(name='shop.synchronize_orders')
def synchronize_orders(isbn=0, count=0):
    # scheduled
    data = dict({"orders": []})
    isbn_count = db.session.query(Book.isbn, func.sum(books_orders_table.c.count)
                     ).join(Order, Order.id == books_orders_table.c.order_id
                            ).join(Book, Book.id == books_orders_table.c.book_id
                                   ).group_by(Book.isbn).filter(Order.synchronized == False).all()
    if not isbn_count:
        return True

    for isbn, count in isbn_count:
        data["orders"].append({"isbn": isbn, "count": count})

    # # apply_async
    # data = {"orders": [{"isbn": isbn, "count": count}]}

    requests.put('http://store:5002/order/', json=data)
    db.session.query(Order).filter(Order.synchronized == False).update({"synchronized":True})
    db.session.commit()
    return True


@shared_task(name='synchronize_db')
def synchronize_db():
    books = Book.query.filter(Book.count > 0).all()
    if books:
        for book in books:
            book.count = 0
        db.session.commit()

    # updated data receiving
    r = requests.get('http://store:5002/book/')
    if r.status_code == 200:
        data = r.json()
    else:
        return f"Error: Request status code -> {r.status_code}"
    a, b = False, False
    for el in data:
        book = Book.query.filter(Book.isbn == el['isbn']).first()
        if book:
            book.title = el['title']
            book.price = el['price']
            book.count = el['count']
            book.summary = el['summary']
            b = True
        else:
            book = Book(
                isbn=el['isbn'],
                title=el['title'],
                price=el['price'],
                count=el['count'],
                summary=el['summary'],
            )
            try:
                db.session.add(book)
                db.session.commit()
                if b:
                    print(blue(f"Successfully updated {book}"))
                else:
                    print(cyan(f"Successfully added {book}"))
            except:
                print(red(f"Error on book addition-> {el['title']}"))
        for el_author in el['authors']:
            if el_author['last_name']:
                author = Author.query.filter(
                    Author.first_name == el_author['first_name'], Author.last_name == el_author['last_name']).first()
                a = True
            else:
                author = Author.query.filter(Author.first_name == el_author['first_name']).first()
                a = True

            if not author:
                if not el_author['last_name']:
                    del el_author['last_name']
                if not el_author['date_of_death']:
                    del el_author['date_of_death']
                author = Author(**el_author)
                try:
                    db.session.add(author)
                    db.session.commit()
                    if a:
                        print(blue(f"Successfully updated {author}"))
                    else:
                        print(cyan(f"Successfully added {author}"))
                except:
                    print(red(f"Error on author("
                              f"{author.first_name}{' ' + author.last_name if author.last_name else ''}"
                              f") adding"))
            book_author = books_authors_table.insert().values(**{
                "book_id": int(book.id),
                "author_id": int(author.id),
            })
            try:
                db.session.execute(book_author)
                db.session.commit()
            except:
                print(red(f"Error on book({book.title}) -> author("
                          f"{author.first_name}{' ' + author.last_name if author.last_name else ''}"
                          f") adding"))
        for el_genre in el['genres']:
            genre = Genre.query.filter(Genre.name == el_genre['name']).first()
            if not genre:
                genre = Genre(**el_genre)
                try:
                    db.session.add(genre)
                    db.session.commit()
                    print(green(f"Successfully added {genre}"))
                except:
                    print(red(f"Error on genre({genre.name}) adding"))
            book_genre = genres_books_table.insert().values(**{
                "book_id": int(book.id),
                "genre_id": int(genre.id),
            })
            try:
                db.session.execute(book_genre)
                db.session.commit()
            except:
                print(red(f"Error on book({book.title}) -> genre({genre.name}) adding"))
        try:
            db.session.commit()
        except:
            print(red('Error on database update'))
        a, b = False, False
    print(green('Successfully updated database'))
    return True
