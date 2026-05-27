from starlette import status

from routers.books import get_db, get_current_user
from utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_books):
    response = client.get("/books")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["page"] == 1
    assert data["size"] == 10
    assert data["total"] == 1

    assert len(data["items"]) == 1

    book = data["items"][0]

    assert book["title"] == "Book Title 1"
    assert book["description"] == "Description 1"
    assert book["author_id"] == 1
    assert book["rating"] == 5
    assert book["owner_id"] == 1
    assert book["published_year"] == 2000


def test_read_one_authenticated(test_books):
    response = client.get("/books/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Book Title 1"
    assert data["description"] == "Description 1"
    assert data["rating"] == 5
    assert data["owner_id"] == 1
    assert data["published_year"] == 2000

    assert "author" in data

    author = data["author"]

    assert author["id"] == 1


def test_read_one_authenticated_not_found(test_books):
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Book not found.'}


def test_create_book(test_books):
    request_data = {
        'title': 'New Book',
        'description': 'Need book description',
        'author_id': 1,
        'rating': 4,
        'published_year': 2024
    }

    response = client.post("/books", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Books).filter(Books.id == 2).first()

    assert model is not None
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.rating == request_data['rating']
    assert model.published_year == request_data['published_year']

    assert model.owner_id == 1


def test_create_book_missing_author(test_books):
    request_data = {
        "title": "No Author",
        "description": "Desc",
        "rating": 5,
        "published_year": 2022
    }

    response = client.post("/books", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_book_author_name_missing_born_year(test_books):
    request_data = {
        "title": "Invalid Author",
        "description": "Desc",
        "author_name": "New Author",
        "rating": 5,
        "published_year": 2022
    }

    response = client.post("/books", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_book_unauthorized():
    # override user = None
    app.dependency_overrides[get_current_user] = lambda: None

    request_data = {
        "title": "Unauthorized",
        "description": "Desc",
        "author_id": 1,
        "rating": 5,
        "published_year": 2022
    }

    response = client.post("/books", json=request_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # restore override
    app.dependency_overrides[get_current_user] = override_get_current_user


def test_update_book(test_books):
    request_data = {
        'title': 'Updated Book Title',
        'description': 'Updated Description',
        'author_id': 1,
        'rating': 4,
        'published_year': 2025
    }

    response = client.put('/books/1', json=request_data)

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Book updated successfully"
    assert data["book_id"] == 1

    db = TestingSessionLocal()
    model = db.query(Books).filter(Books.id == 1).first()

    assert model is not None
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.author_id == request_data['author_id']
    assert model.rating == request_data['rating']
    assert model.published_year == request_data['published_year']


def test_create_book_with_both_author_fields(test_books):
    request_data = {
        "title": "Conflict Author",
        "description": "Desc",
        "author_id": 1,
        "author_name": "Conflict",
        "rating": 5,
        "published_year": 2022
    }

    response = client.post("/books", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_book_not_found(test_books):
    request_data = {
        'title': 'Updated Book Title',
        'description': 'Updated Description',
        'author_id': 2,
        'rating': 4,
        'published_year': 2025
    }

    response = client.put('/books/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}


def test_delete_book(test_books):
    response = client.delete('/books/1')
    assert response.status_code == status.HTTP_200_OK
    db = TestingSessionLocal()
    model = db.query(Books).filter(Books.id == 1).first()
    assert model is None


def test_delete_book_not_found(test_books):
    response = client.delete('/books/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}
