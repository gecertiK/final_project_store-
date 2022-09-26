from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import schemas
from models import Book


def synchronize_orders(request: schemas.OrderUpdate, db: Session):
    for order in request.orders:
        book = db.query(Book).filter(Book.isbn == order.isbn)
        if book.first():
            book.update({"count": book.first().count - order.count})
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={"detail": f"Book with isbn {order.isbn} not available"})
    return True
