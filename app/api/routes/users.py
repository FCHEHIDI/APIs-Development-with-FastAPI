"""
User management routes.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import UserResponse, UserUpdate, MessageResponse, PaginatedResponse
from app.services.user_service import UserService
from app.api.dependencies.auth import get_current_active_user, get_current_superuser
from app.models import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get all users (superuser only).
    
    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        List of users
    """
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user information
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get user by ID (superuser only).
    
    Args:
        user_id: User ID to retrieve
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found
    """
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user information.
    
    Args:
        user_update: User update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated user information
    """
    updated_user = UserService.update_user(
        db=db, user_id=current_user.id, user_update=user_update
    )
    return updated_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Update user by ID (superuser only).
    
    Args:
        user_id: User ID to update
        user_update: User update data
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        Updated user information
        
    Raises:
        HTTPException: If user not found
    """
    updated_user = UserService.update_user(
        db=db, user_id=user_id, user_update=user_update
    )
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Delete user by ID (superuser only).
    
    Args:
        user_id: User ID to delete
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If user not found
    """
    success = UserService.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return MessageResponse(message="User deleted successfully")
