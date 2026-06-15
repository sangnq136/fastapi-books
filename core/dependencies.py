"""Centralized dependency injection setup."""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from database import SessionLocal
from routers.auth import get_current_user

def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_active_user(
        user: Annotated[dict, Depends(get_current_user)]
):
    """Ensure user is authenticated and active."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied"
        )
    return user

# Type aliases for consistency
db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_active_user)]
