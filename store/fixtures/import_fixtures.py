import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book, Author, books_authors_table, Genre, genres_books_table

color = lambda x, y, z: ";".join([str(x), str(y), str(z)])

red = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 31, 40), x)
green = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 32, 40), x)
yellow = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 33, 40), x)
blue = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 34, 40), x)
purple = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 35, 40), x)
cyan = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 36, 40), x)

selected_color = lambda x, y: '\x1b[%sm%s\x1b[0m' % (y, x)

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@db_store:5432/db_store'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

session = SessionLocal()



def import_data():
    with open('fixtures/test_data.json', 'r') as file:
        data = json.load(file)
        a, b = False, False
        for key, value in data.items():
            book = session.query(Book).filter(Book.isbn == key).first()
            if book:
                book.title = value['title']
                book.price = value['price']
                book.count = value['count']
                book.summary = value['summary']
                b = True
            else:
                book = Book(
                    isbn=key,
                    title=value['title'],
                    price=value['price'],
                    count=value['count'],
                    summary=value['summary'],
                )
                try:
                    session.add(book)
                    session.commit()
                    if b:
                        print(blue(f"Successfully updated {book}"))
                    else:
                        print(cyan(f"Successfully added {book}"))
                except:
                    print(red(f"Error on book addition-> {value['title']}"))
            for el in value['authors']:
                if el['last_name']:
                    author = session.query(Author).filter(
                        Author.first_name == el['first_name'], Author.last_name == el['last_name']).first()
                    a = True
                else:
                    author = session.query(Author).filter(Author.first_name == el['first_name']).first()
                    a = True

                if not author:
                    if not el['last_name']:
                        del el['last_name']
                    if not el['date_of_death']:
                        del el['date_of_death']
                    author = Author(**el)
                    try:
                        session.add(author)
                        session.commit()
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
                    session.execute(book_author)
                    session.commit()
                except:
                    print(red(f"Error on book({book.title}) -> author("
                              f"{author.first_name}{' ' + author.last_name if author.last_name else ''}"
                              f") adding"))
            for el in value['genres']:
                genre = session.query(Genre).filter(Genre.name == el['name']).first()
                if not genre:
                    genre = Genre(**el)
                    try:
                        session.add(genre)
                        session.commit()
                        print(green(f"Successfully added {genre}"))
                    except:
                        print(red(f"Error on genre({genre.name}) adding"))
                book_genre = genres_books_table.insert().values(**{
                    "book_id": int(book.id),
                    "genre_id": int(genre.id),
                })
                try:
                    session.execute(book_genre)
                    session.commit()
                except:
                    print(red(f"Error on book({book.title}) -> genre({genre.name}) adding"))
            try:
                session.commit()
            except:
                print(red('Error on database update'))
            a, b = False, False
        print(green('Successfully updated database'))
    session.close()