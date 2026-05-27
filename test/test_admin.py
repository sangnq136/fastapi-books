from fastapi import status

from utils import *
from routers.admin import get_db, get_current_user
from models import Books

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_books):
    response = client.get('/admin/books')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1

    book = data[0]

    assert book["title"] == "Book Title 1"
    assert book["description"] == "Description 1"
    assert book["author_id"] == 1
    assert book["rating"] == 5
    assert book["owner_id"] == 1
    assert book["published_year"] == 2000

def test_admin_delete_book(test_books):
    response = client.delete(f'/admin/books/1')
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    model = db.query(Books).filter(Books.id == 1).first()
    assert model is None

def test_admin_delete_book_not_found():
    response = client.delete(f'/admin/books/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}