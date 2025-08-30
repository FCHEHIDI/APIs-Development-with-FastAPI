"""
User service layer for business logic.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.core.security import security


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(
            or_(User.email == user.email, User.username == user.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user.email:
                raise ValueError("Email already registered")
            if existing_user.username == user.username:
                raise ValueError("Username already taken")
        
        # Create new user
        hashed_password = security.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username/email and password."""
        # Allow login with either username or email
        user = db.query(User).filter(
            or_(User.username == username, User.email == username)
        ).first()
        
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True
