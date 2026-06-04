from fastapi import HTTPException, status
from repositories.admin_repository import *


# ✅ check admin role
def _check_admin(user):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied"
        )


# ✅ get all books (admin)
def admin_get_all_books_service(db, user):
    _check_admin(user)
    return get_all_books(db)


# ✅ delete book (admin)
def admin_delete_book_service(db, user, book_id: int):
    try:
        _check_admin(user)

        book = get_book_by_id(db, book_id)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found."
            )

        delete_book(db, book_id)
        db.commit()

        return {
            "message": "Book deleted successfully"
        }

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(500, "Internal Server Error")
