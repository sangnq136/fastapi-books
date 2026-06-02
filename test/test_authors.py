from starlette import status
from utils import *
from routers.authors import get_db
from routers.auth import get_current_user
from models import Authors

# ✅ override dependency
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all_authors(test_author):
    response = client.get("/authors")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["page"] == 1
    assert data["size"] == 10
    assert data["total"] == 1
    assert len(data["items"]) == 1

    author = data["items"][0]

    assert author["name"] == "Author Test"
    assert author["description"] == "Desc"
    assert author["born_year"] == 1990


def test_get_author_detail(test_author):
    response = client.get(f"/authors/{test_author.id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == test_author.id
    assert data["name"] == "Author Test"
    assert data["description"] == "Desc"
    assert data["born_year"] == 1990


def test_get_author_not_found(test_author):
    response = client.get("/authors/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found."}


def test_create_author(test_author):
    request_data = {
        "name": "New Author",
        "description": "New Desc",
        "born_year": 2000
    }

    response = client.post("/authors", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    author = db.query(Authors).filter(Authors.id == 2).first()

    assert author is not None
    assert author.name == request_data["name"]
    assert author.description == request_data["description"]
    assert author.born_year == request_data["born_year"]


def test_update_author(test_author):
    request_data = {
        "name": "Updated Author",
        "description": "Updated Desc",
        "born_year": 2001
    }

    response = client.put(f"/authors/{test_author.id}", json=request_data)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["message"] == "Author updated successfully"

    db = TestingSessionLocal()
    updated = db.query(Authors).filter(Authors.id == test_author.id).first()

    assert updated.name == request_data["name"]
    assert updated.description == request_data["description"]
    assert updated.born_year == request_data["born_year"]


def test_update_author_not_found():
    request_data = {
        "name": "Updated Author",
        "description": "Updated Desc",
        "born_year": 2001
    }

    response = client.put("/authors/999", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found."}


def test_delete_author(test_author):
    response = client.delete(f"/authors/{test_author.id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["message"] == "Author deleted successfully"

    db = TestingSessionLocal()
    author = db.query(Authors).filter(Authors.id == test_author.id).first()

    assert author is None


def test_delete_author_not_found():
    response = client.delete("/authors/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found."}
