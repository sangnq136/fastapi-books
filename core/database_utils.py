"""Database utilities for migrations and indexing."""
from sqlalchemy import Index
from models import Books, Authors, Users

def create_indexes(engine):
    """Create indexes on foreign keys and frequently queried columns."""
    
    # Create indexes if they don't exist
    indexes = [
        Index('ix_books_author_id', Books.author_id),
        Index('ix_books_owner_id', Books.owner_id),
        Index('ix_books_title', Books.title),
        Index('ix_users_email', Users.email),
        Index('ix_users_username', Users.username),
        Index('ix_authors_name', Authors.name),
    ]
    
    for index in indexes:
        index.create(engine, checkfirst=True)
