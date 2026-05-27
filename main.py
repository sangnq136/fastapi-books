from fastapi import FastAPI
from database import engine
from routers import auth, admin, users, books, authors
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(authors.router)
