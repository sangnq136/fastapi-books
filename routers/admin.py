from typing import Annotated

from fastapi import APIRouter, Depends, Path

from database import SessionLocal
from services.admin_service import *
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_user)]  # ✅ inject auth global
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books(
    user: user_dependency,
    db: db_dependency
):
    return admin_get_all_books_service(db, user)

@router.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book_admin(
    user: user_dependency,
    db: db_dependency,
    book_id: int = Path(gt=0)
):
    return admin_delete_book_service(db, user, book_id)
