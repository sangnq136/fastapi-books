from fastapi import HTTPException, status
from repositories.book_repository import *


def build_book_response(book, author):
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
        "rating": book.rating,
        "published_year": book.published_year,
        "owner_id": book.owner_id,
        "author": {
            "id": author.id,
            "name": author.name,
            "born_year": author.born_year,
        }
    }


def create_book_service(db, user, request):
    try:
        # ✅ resolve author
        if request.author_id:
            author = get_author_by_id(db, request.author_id)
            if not author:
                raise HTTPException(404, "Author not found")

        else:
            author = get_author_by_name(db, request.author_name)

            if not author:
                author = create_author(
                    db,
                    request.author_name,
                    request.author_born_year
                )

        # ✅ create book
        book = Books(
            title=request.title,
            author_id=author.id,
            description=request.description,
            rating=request.rating,
            published_year=request.published_year,
            owner_id=user['id']
        )

        create_book(db, book)

        db.commit()
        db.refresh(book)

        return build_book_response(book, author)

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


def read_detail_service(db, user, book_id: int):
    book = get_book_by_id(db, book_id, user["id"])

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found."
        )

    author = get_author_by_id(db, book.author_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
        "rating": book.rating,
        "published_year": book.published_year,
        "owner_id": book.owner_id,
        "author": {
            "id": author.id,
            "name": author.name,
            "born_year": author.born_year,
            "description": author.description,
        }
    }


def delete_book_service(db, user, book_id: int):
    try:
        book = get_book_by_id(db, book_id, user["id"])

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found."
            )

        delete_book(db, book_id, user["id"])

        db.commit()

        return {
            "message": "Book deleted successfully"
        }

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


def update_book_service(db, user, request, book_id: int):
    try:
        book = get_book_by_id(db, book_id, user["id"])

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found."
            )

        # ✅ resolve author logic (reuse create logic)
        if request.author_id:
            author = get_author_by_id(db, request.author_id)
            if not author:
                raise HTTPException(404, "Author not found")

        elif request.author_name:
            author = get_author_by_name(db, request.author_name)

            if not author:
                author = create_author(
                    db,
                    request.author_name,
                    request.author_born_year
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either author_id or author_name must be provided"
            )

        # ✅ update fields
        book.title = request.title
        book.description = request.description
        book.rating = request.rating
        book.author_id = author.id
        book.published_year = request.published_year

        db.add(book)
        db.commit()
        db.refresh(book)

        return {
            "message": "Book updated successfully",
            "book_id": book.id
        }

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
