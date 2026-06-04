# 📘 Books API (FastAPI)

A FastAPI project providing authentication and book management with author auto-creation, pagination, and full test coverage.

## 🚀 Quick Start

### 1. Install dependencies

pip install -r requirements.txt

---

### 2. Initialize database

python

from database import engine
from models import Base
Base.metadata.create_all(bind=engine)

---

### 3. Run application

uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs

---

### ✅ Run tests

pytest

---

## 🔐 Environment Variables

Create `.env` file:

- SECRET_KEY=your_secret_key
- ALGORITHM=HS256

---

## 📦 Core Features

- JWT Authentication
- CRUD Books (with ownership)
- Auto-create Author if not provided
- Pagination support
- Input validation via Pydantic
- Unit tests with pytest

---

## 📚 API Endpoints

### Auth

- POST /auth → Create user
- POST /auth/token → Login (JWT)

### Books

- GET /books → List books (pagination) by owner created
- GET /books/{book_id} → Book detail by owner created
- POST /books → Create book
- PUT /books/{book_id} → Update book by owner created
- DELETE /books/{book_id} → Delete book by owner created

### Authors

- GET /authors → List authors  (pagination)
- GET /authors/{author_id} → Author detail
- POST /authors → Create author
- PUT /authors/{author_id} → Update author
- DELETE /authors/{author_id} → Delete author


### Admins

- GET /books → List books (pagination) by admin 
- DELETE /books/{book_id} → Delete book by admin 

---

## ⚙️ Create Book Logic

- Provide author_id → use existing author  
- Provide author_name → reuse or auto-create  
- Missing both → validation error (422)

---

## 📬 Postman (quick test flow)

Requests:

1. Create User → POST /auth  
2. Login → POST /auth/token  
3. Create Book → POST /books  
4. Get Book → GET /books/{id}  
5. Update → PUT /books/{id}  
6. Delete → DELETE /books/{id}  
7. List → GET /books?page=1&size=10

---

## ⏱ Evaluation Flow

- pip install -r requirements.txt
- pytest
- uvicorn main:app --reload

- Test via Swagger (http://127.0.0.1:8000/docs) or Postman with the 6 core requests.

---

## ✅ Checklist

- App runs
- Auth works
- CRUD Books works
- Author auto-create works
- Pagination works
- Tests pass

---

## 👤 Author

Nguyen Quang Sang (Shelby)
