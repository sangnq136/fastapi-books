from models import Books


def get_all_books(db):
    return db.query(Books).all()


def get_book_by_id(db, book_id: int):
    return db.query(Books).filter(Books.id == book_id).first()


def delete_book(db, book_id: int):
    db.query(Books).filter(Books.id == book_id).delete()
