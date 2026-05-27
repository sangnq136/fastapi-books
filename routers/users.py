from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Query

from database import SessionLocal
from schemas.user_schema import ChangePasswordRequest, ChangePhoneRequest
from services.user_service import *
from .auth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)]  # inject auth toàn router
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return read_all_users_service(db)


@router.get("/detail", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    return get_current_user_service(db, user)


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
        user: user_dependency,
        db: db_dependency,
        request: ChangePasswordRequest
):
    return change_password_service(db, user, request)


@router.put("/change_phone", status_code=status.HTTP_200_OK)
async def change_phone(
        user: user_dependency,
        db: db_dependency,
        phone_number: str = Query(None),
):
    return change_phone_service(db, user, phone_number)
