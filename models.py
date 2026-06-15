"""Models for Users, Books, and Authors using SQLAlchemy."""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship

from database import Base

class Users(Base):
    """Models for Users"""
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
    
    books = relationship("Books", back_populates="owner")
    
    __table_args__ = (
        Index('ix_users_email', 'email'),
        Index('ix_users_username', 'username'),
    )

class Authors(Base):
    """Models for Authors"""
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    born_year = Column(Integer)
    
    books = relationship("Books", back_populates="author", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_authors_name', 'name'),
    )

class Books(Base):
    """Models for Books"""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'))
    rating = Column(Integer)
    description = Column(String)
    published_year = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    
    author = relationship("Authors", back_populates="books")
    owner = relationship("Users", back_populates="books")
    
    __table_args__ = (
        Index('ix_books_author_id', 'author_id'),
        Index('ix_books_owner_id', 'owner_id'),
        Index('ix_books_title', 'title'),
    )
