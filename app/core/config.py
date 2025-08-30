"""
Configuration management for the FastAPI application.
"""
import os
from typing import Optional, List
from decouple import config
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    # Application
    app_name: str = "FastAPI Professional API"
    app_version: str = "1.0.0"
    debug: bool = config("DEBUG", default=False, cast=bool)
    
    # Server
    host: str = config("HOST", default="0.0.0.0")
    port: int = config("PORT", default=8000, cast=int)
    
    # Database
    database_url: Optional[str] = config("DATABASE_URL", default=None)
    database_echo: bool = config("DATABASE_ECHO", default=False, cast=bool)
    
    # Security
    secret_key: str = config("SECRET_KEY", default="your-super-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # CORS
    allowed_hosts: List[str] = ["*"]
    cors_origins: List[str] = ["*"]
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Rate Limiting
    rate_limit_requests: int = config("RATE_LIMIT_REQUESTS", default=100, cast=int)
    rate_limit_window: int = config("RATE_LIMIT_WINDOW", default=60, cast=int)
    
    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> str:
        if v is None:
            # Default SQLite for development
            return "sqlite:///./app.db"
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
