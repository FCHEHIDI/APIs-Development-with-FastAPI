"""
Security utilities for authentication and authorization.
"""
from datetime import datetime, timedelta
from typing import Optional, Union, Any
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityManager:
    """Handles authentication and security operations."""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate password hash.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def create_password_reset_token(email: str) -> str:
        """
        Create password reset token.
        
        Args:
            email: User email
            
        Returns:
            Password reset token
        """
        delta = timedelta(hours=1)  # Reset token expires in 1 hour
        data = {"sub": email, "type": "password_reset"}
        return SecurityManager.create_access_token(data, expires_delta=delta)
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[str]:
        """
        Verify password reset token.
        
        Args:
            token: Password reset token
            
        Returns:
            Email if token is valid, None otherwise
        """
        payload = SecurityManager.verify_token(token)
        if payload and payload.get("type") == "password_reset":
            return payload.get("sub")
        return None


# Global security manager instance
security = SecurityManager()
