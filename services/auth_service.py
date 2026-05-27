from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext

from core.config import settings
from repositories.auth_repository import *

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Authenticate user
def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)

    if not user:
        return None

    if not bcrypt_context.verify(password, user.hashed_password):
        return None

    return user


# ✅ Create JWT token
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    to_encode = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.now() + expires_delta
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ✅ Get current user
def get_current_user_service(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        username = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")

        if not username or not user_id:
            raise HTTPException(status_code=401, detail="Could not validate user")

        return {
            "username": username,
            "id": user_id,
            "user_role": role
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate user")


# ✅ Create user
def create_user_service(db, request):
    try:
        if get_user_by_username(db, request.username) or get_user_by_email(db, request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username / Email already exists"
            )

        from models import Users

        user = Users(
            email=request.email,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            role=request.role,
            hashed_password=bcrypt_context.hash(request.password),
            phone_number=request.phone_number,
            is_active=True,
        )

        create_user(db, user)

        db.commit()

        return {"message": "User created successfully"}

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(500, "Internal Server Error")
