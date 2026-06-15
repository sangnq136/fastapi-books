"""Audit logging middleware for tracking API requests."""
import logging
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure audit logger
audit_logger = logging.getLogger("audit")
audit_handler = logging.FileHandler("audit.log")
audit_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
audit_handler.setFormatter(audit_formatter)
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all API requests for audit trail."""
    
    async def dispatch(self, request: Request, call_next):
        # Log request details
        user_id = None
        if hasattr(request.state, "user"):
            user_id = request.state.user.get("id")
        
        audit_logger.info(
            f"REQUEST: {request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'Unknown'} - "
            f"User: {user_id or 'Anonymous'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        audit_logger.info(
            f"RESPONSE: {request.method} {request.url.path} - "
            f"Status: {response.status_code}"
        )
        
        return response
