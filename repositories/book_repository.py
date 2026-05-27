from models import Books, Authors


def get_books(db, user_id):
    return db.query(Books).filter(Books.owner_id == user_id)


def get_book_by_id(db, book_id, user_id):
    return db.query(Books) \
        .filter(Books.id == book_id) \
        .filter(Books.owner_id == user_id) \
        .first()


def get_author_by_id(db, author_id):
    return db.query(Authors).filter(Authors.id == author_id).first()


def get_author_by_name(db, name):
    return db.query(Authors).filter(Authors.name == name).first()


def create_author(db, name, born_year):
    author = Authors(
        name=name,
        description="Auto created author",
        born_year=born_year
    )
    db.add(author)
    db.flush()
    return author


def create_book(db, book_model):
    db.add(book_model)


def delete_book(db, book_id, user_id):
    db.query(Books)\
        .filter(Books.id == book_id)\
        .filter(Books.owner_id == user_id)\
        .delete()
