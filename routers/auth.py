from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import SessionLocal
from schemas.auth_schema import *
from services.auth_service import *

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]


# ✅ wrap dependency để dùng toàn project
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    return get_current_user_service(token)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        request: CreateUserRequest
):
    return create_user_service(db, request)


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Failed to authenticate")

    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=20)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
