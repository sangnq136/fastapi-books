from typing import Annotated

from fastapi import Depends, Path, APIRouter
from fastapi import Query

from database import SessionLocal
from schemas.book_schema import BooksRequest
from services.book_service import *
from .auth import get_current_user

router = APIRouter(
    prefix='/books',
    tags=['books']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_active_user(
        user: Annotated[dict, Depends(get_current_user)]
):
    if not user:
        raise HTTPException(401, "Authentication Failed")
    return user


# dependency inject
db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_active_user)]


### Endpoint ###
@router.get(path="", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency, page: int = Query(1), size: int = Query(10)):
    query = get_books(db, user['id'])

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total
    }


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def read_detail(
        user: user_dependency,
        db: db_dependency,
        book_id: int = Path(gt=0)
):
    return read_detail_service(db, user, book_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(user: user_dependency, db: db_dependency, request: BooksRequest):
    return create_book_service(db, user, request)


@router.put("/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(
        user: user_dependency,
        db: db_dependency,
        request: BooksRequest,
        book_id: int = Path(gt=0)
):
    return update_book_service(db, user, request, book_id)


#
#
@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(
        user: user_dependency,
        db: db_dependency,
        book_id: int = Path(gt=0)
):
    return delete_book_service(db, user, book_id)
