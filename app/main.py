"""
FastAPI Professional API Application

A production-ready FastAPI application demonstrating best practices for:
- Project structure and organization
- Authentication and authorization
- Database integration with SQLAlchemy
- Input validation with Pydantic
- Error handling and logging
- API documentation
- Security features
- Testing setup

Author: Backend Developer Portfolio
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import time
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import api_router
from app.utils.helpers import APILogger


# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    """
    # Startup
    APILogger.log_request("STARTUP", "/", None)
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    APILogger.log_request("SHUTDOWN", "/", None)


# FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## Professional FastAPI Application

    This is a comprehensive REST API built with FastAPI, showcasing professional backend development practices.

    ### Features:
    - 🔐 **JWT Authentication**: Secure user authentication and authorization
    - 📊 **Database Integration**: SQLAlchemy ORM with PostgreSQL/SQLite support
    - 📝 **CRUD Operations**: Complete Create, Read, Update, Delete functionality
    - 🛡️ **Security**: Password hashing, input validation, and security headers
    - 📖 **Documentation**: Auto-generated interactive API docs
    - 🧪 **Testing**: Comprehensive unit and integration tests
    - 📁 **Clean Architecture**: Well-organized code structure
    - 🔍 **Logging**: Structured logging for monitoring and debugging
    - 🚀 **Production Ready**: Error handling, middleware, and best practices

    ### Tech Stack:
    - **Framework**: FastAPI
    - **Database**: SQLAlchemy with PostgreSQL/SQLite
    - **Authentication**: JWT with python-jose
    - **Validation**: Pydantic models
    - **Security**: Passlib for password hashing
    - **Testing**: Pytest with async support
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Security Middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.allowed_hosts
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add process time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log request/response
    APILogger.log_response(response.status_code, process_time)
    
    return response


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    APILogger.log_error("Validation error", {"errors": exc.errors()})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    APILogger.log_error("Database error", {"error": str(exc)})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred",
            "error_code": "DATABASE_ERROR"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    APILogger.log_error("HTTP error", {
        "status_code": exc.status_code,
        "detail": exc.detail
    })
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Application health status
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "timestamp": time.time()
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API welcome message and links
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_check": "/health"
    }


# Include API routes
app.include_router(api_router, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
