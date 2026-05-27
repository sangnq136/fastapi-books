from fastapi import HTTPException, status
from passlib.context import CryptContext
from repositories.user_repository import *

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#   READ ALL USERS
def read_all_users_service(db):
    return get_all_users(db)


#   GET CURRENT USER
def get_current_user_service(db, user):
    user_model = get_user_by_id(db, user["id"])

    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )

    return user_model


#   CHANGE PASSWORD
def change_password_service(db, user, request):
    try:
        user_model = get_user_by_id(db, user["id"])

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )

        if not bcrypt_context.verify(request.password, user_model.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Old Password"
            )

        user_model.hashed_password = bcrypt_context.hash(request.new_password)

        update_user(db, user_model)
        db.commit()

        return {
            "message": "Password updated successfully"
        }

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(500, "Internal Server Error")


#   CHANGE PHONE
def change_phone_service(db, user, phone_number):
    try:
        user_model = get_user_by_id(db, user["id"])

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )

        user_model.phone_number = phone_number

        update_user(db, user_model)
        db.commit()

        return {
            "message": "Phone number updated successfully"
        }

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(500, "Internal Server Error")
