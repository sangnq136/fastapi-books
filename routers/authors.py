from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path

from database import SessionLocal
from schemas.author_schema import AuthorsRequest
from services.author_service import *
from .auth import get_current_user


def get_current_active_user(
        user: Annotated[dict, Depends(get_current_user)]
):
    if not user:
        raise HTTPException(401, "Access Denied")
    return user


router = APIRouter(
    prefix='/authors',
    tags=['authors'],
    dependencies=[Depends(get_current_active_user)]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_active_user)]


@router.get("", status_code=status.HTTP_200_OK)
async def read_all(
        db: db_dependency,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1)
):
    return read_all_authors_service(db, page, size)


@router.get("/{author_id}", status_code=status.HTTP_200_OK)
async def get_detail(
        db: db_dependency,
        author_id: int = Path(gt=0)
):
    return get_author_detail_service(db, author_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(
        db: db_dependency,
        request: AuthorsRequest
):
    return create_author_service(db, request)


@router.put("/{author_id}", status_code=status.HTTP_200_OK)
async def update_author(
        db: db_dependency,
        request: AuthorsRequest,
        author_id: int = Path(gt=0)
):
    return update_author_service(db, request, author_id)


@router.delete("/{author_id}", status_code=status.HTTP_200_OK)
async def delete_author(
        db: db_dependency,
        author_id: int = Path(gt=0)
):
    return delete_author_service(db, author_id)
