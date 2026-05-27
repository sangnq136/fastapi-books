from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    rating = Column(Integer)
    description = Column(String)
    published_year = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))

class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    born_year = Column(Integer)
