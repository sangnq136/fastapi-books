from models import Authors


def get_authors(db):
    return db.query(Authors)


def get_author_by_id(db, author_id: int):
    return db.query(Authors).filter(Authors.id == author_id).first()


def create_author(db, author_model):
    db.add(author_model)


def update_author(db, author):
    db.add(author)


def delete_author(db, author_id: int):
    db.query(Authors).filter(Authors.id == author_id).delete()
