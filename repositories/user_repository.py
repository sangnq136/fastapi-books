from models import Users


def get_all_users(db):
    return db.query(Users).all()


def get_user_by_id(db, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


def update_user(db, user):
    db.add(user)
