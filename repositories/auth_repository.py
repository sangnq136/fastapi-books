from models import Users


def get_user_by_username(db, username: str):
    return db.query(Users).filter(Users.username == username).first()


def get_user_by_email(db, email: str):
    return db.query(Users).filter(Users.email == email).first()


def create_user(db, user_model):
    db.add(user_model)
