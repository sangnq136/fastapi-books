"""Rate limiting utilities."""
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from collections import defaultdict

# In-memory rate limit store (use Redis in production)
request_counts = defaultdict(list)
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_SECONDS = 60


def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit."""
    now = datetime.now()
    window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS)
    
    # Clean old requests
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip]
        if req_time > window_start
    ]
    
    # Check limit
    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    
    # Record request
    request_counts[client_ip].append(now)
    return True


async def rate_limit_middleware(request, call_next):
    """Middleware to enforce rate limiting."""
    client_ip = request.client.host if request.client else "unknown"
    
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 100 requests per minute."
        )
    
    return await call_next(request)
