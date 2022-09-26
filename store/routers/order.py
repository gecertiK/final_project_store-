from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from repository import order
import db, schemas

router = APIRouter(
    prefix='/order',
    tags=['Order'],

)


@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
def synchronize_orders(request: schemas.OrderUpdate, db: Session = Depends(db.get_db)):
    return order.synchronize_orders(request, db)
