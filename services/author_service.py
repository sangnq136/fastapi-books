from repositories.author_repository import *
from fastapi import HTTPException, status
from models import Authors


def read_all_authors_service(db, page: int, size: int):
    query = get_authors(db)

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total
    }


def create_author_service(db, request):
    try:
        author = Authors(
            name=request.name,
            description=request.description,
            born_year=request.born_year
        )

        create_author(db, author)

        db.commit()
        db.refresh(author)

        return author

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


def get_author_detail_service(db, author_id: int):
    author = get_author_by_id(db, author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found."
        )

    return author


def update_author_service(db, request, author_id: int):
    try:
        author = get_author_by_id(db, author_id)

        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found."
            )

        author.name = request.name
        author.description = request.description
        author.born_year = request.born_year

        update_author(db, author)

        db.commit()
        db.refresh(author)

        return {
            "message": "Author updated successfully",
            "author_id": author.id
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(500, "Internal Server Error")


def delete_author_service(db, author_id: int):
    try:
        author = get_author_by_id(db, author_id)

        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found."
            )

        delete_author(db, author_id)

        db.commit()

        return {
            "message": "Author deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(500, "Internal Server Error")
