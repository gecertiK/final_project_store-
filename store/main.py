from fastapi import FastAPI

import models, routers
from routers import author, book, genre, order

from config import settings



app = FastAPI()

app.include_router(author.router)
app.include_router(book.router)
app.include_router(genre.router)
app.include_router(order.router)
