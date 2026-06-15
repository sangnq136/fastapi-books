from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from database import engine
from routers import auth, admin, users, books, authors
from models import Base
from core.config import settings
from core.middleware import AuditLoggingMiddleware
from core.rate_limiter import rate_limit_middleware
from core.database_utils import create_indexes

app = FastAPI(
    title="Books API",
    description="REST API for managing books, authors, and users",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create database indexes
create_indexes(engine)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add audit logging middleware
app.add_middleware(AuditLoggingMiddleware)

# Add rate limiting middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

# Include routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(authors.router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
