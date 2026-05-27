import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app
from models import Books, Users, Authors
from routers.auth import bcrypt_context

#  Test DB (SQLite in-memory-like with StaticPool)
SQLALCHEMY_DATABASE_URI = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


#  Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#  Override user (authentication)
def override_get_current_user():
    return {'username': 'shelbytest', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    db = TestingSessionLocal()

    # cleanup trước mỗi test
    db.query(Books).delete()
    db.query(Authors).delete()
    db.query(Users).delete()
    db.commit()

    yield

    # cleanup sau mỗi test
    db.query(Books).delete()
    db.query(Authors).delete()
    db.query(Users).delete()
    db.commit()

    db.close()


@pytest.fixture
def test_users():
    db = TestingSessionLocal()

    user = Users(
        username="shelbytest",
        email="shelbytest@email.com",
        first_name="Shelby",
        last_name="Test",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="+1 555 555 555",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    db.close()


@pytest.fixture
def test_author():
    db = TestingSessionLocal()

    author = Authors(
        name="Author Test",
        description="Desc",
        born_year=1990
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    yield author

    db.close()


@pytest.fixture
def test_books():
    db = TestingSessionLocal()

    author = Authors(
        name="Author Test",
        description="Desc",
        born_year=1990
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    book = Books(
        title="Book Title 1",
        author_id=author.id,
        description="Description 1",
        rating=5,
        owner_id=1,
        published_year=2000
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    yield book

    db.close()
