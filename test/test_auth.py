from starlette import status

from utils import *
from routers.auth import get_db, authenticate_user, create_access_token, get_current_user
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db


def test_authenticated_user(test_users):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(db, test_users.username, 'testpassword')
    assert authenticated_user is not None
    assert test_users.username == authenticated_user.username

    non_existent_user = authenticate_user(db, 'WrongUserName', 'testpassword')
    assert non_existent_user is None

    wrong_password_user = authenticate_user(db, test_users.username, 'wrongpassword')
    assert wrong_password_user is None


def test_create_access_token(monkeypatch):
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("ALGORITHM", "HS256")
    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, "testsecret", algorithms="HS256", options={'verify_signature': False})
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("ALGORITHM", "HS256")

    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, "testsecret", algorithm="HS256")

    user = await get_current_user(token=token)

    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


#
@pytest.mark.asyncio
async def test_get_current_user_missing_payload(monkeypatch):
    # ✅ mock env
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("ALGORITHM", "HS256")

    encode = {'role': 'user'}  # ❌ thiếu sub + id
    token = jwt.encode(encode, "testsecret", algorithm="HS256")

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate user'


@pytest.mark.parametrize("email", [
    "plainaddress",
    "missingatsign.com",
    "user@.com",
    "@domain.com",
    "user@domain"
])
def test_create_user_invalid_email_cases(email):
    request_data = {
        "username": "testuser",
        "email": email,
        "first_name": "test",
        "last_name": "user",
        "role": "user",
        "password": "testpassword",
        "phone_number": "123456789"
    }

    response = client.post("/auth", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
