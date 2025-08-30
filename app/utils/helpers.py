"""
Utility functions and helpers.
"""
import re
from typing import Any, Dict, Optional
from datetime import datetime
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        True if username is valid, False otherwise
    """
    # Username: 3-30 characters, alphanumeric and underscores only
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    return re.match(pattern, username) is not None


def sanitize_string(text: str, max_length: int = 255) -> str:
    """
    Sanitize and truncate string input.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potential harmful characters
    sanitized = re.sub(r'[<>"\']', '', text.strip())
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def create_response_metadata(
    total_items: int,
    page: int,
    size: int,
    additional_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create standardized response metadata for pagination.
    
    Args:
        total_items: Total number of items
        page: Current page number
        size: Page size
        additional_data: Additional metadata to include
        
    Returns:
        Response metadata dictionary
    """
    total_pages = (total_items + size - 1) // size if size > 0 else 0
    
    metadata = {
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if additional_data:
        metadata.update(additional_data)
    
    return metadata


class APILogger:
    """Structured logging utility for API operations."""
    
    @staticmethod
    def log_request(method: str, path: str, user_id: Optional[int] = None):
        """Log API request."""
        logger.info(
            "API request",
            method=method,
            path=path,
            user_id=user_id,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_response(status_code: int, execution_time: float):
        """Log API response."""
        logger.info(
            "API response",
            status_code=status_code,
            execution_time=execution_time,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_error(error: str, details: Optional[Dict[str, Any]] = None):
        """Log API error."""
        logger.error(
            "API error",
            error=error,
            details=details,
            timestamp=datetime.utcnow().isoformat()
        )
