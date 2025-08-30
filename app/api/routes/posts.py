"""
Post management routes.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import PostCreate, PostUpdate, PostResponse, MessageResponse
from app.services.post_service import PostService
from app.api.dependencies.auth import get_current_active_user, get_optional_current_user
from app.models import User

router = APIRouter()


@router.get("/", response_model=List[PostResponse])
async def read_posts(
    skip: int = Query(0, ge=0, description="Number of posts to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of posts to return"),
    published_only: bool = Query(True, description="Only return published posts"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get all posts with pagination.
    
    Args:
        skip: Number of posts to skip
        limit: Maximum number of posts to return
        published_only: Only return published posts
        db: Database session
        current_user: Optional current user (for accessing unpublished posts)
        
    Returns:
        List of posts
    """
    # If user is authenticated, they can see their own unpublished posts
    if current_user and not published_only:
        published_only = False
    
    posts = PostService.get_posts(
        db=db, 
        skip=skip, 
        limit=limit, 
        published_only=published_only
    )
    return posts


@router.get("/my-posts", response_model=List[PostResponse])
async def read_my_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's posts.
    
    Args:
        skip: Number of posts to skip
        limit: Maximum number of posts to return
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of user's posts
    """
    posts = PostService.get_posts(
        db=db, 
        skip=skip, 
        limit=limit, 
        owner_id=current_user.id,
        published_only=False
    )
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def read_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get post by ID.
    
    Args:
        post_id: Post ID to retrieve
        db: Database session
        current_user: Optional current user
        
    Returns:
        Post information
        
    Raises:
        HTTPException: If post not found or not accessible
    """
    db_post = PostService.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check if post is published or user is the owner
    if not db_post.is_published:
        if not current_user or current_user.id != db_post.owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
    
    return db_post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new post.
    
    Args:
        post: Post creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created post information
    """
    return PostService.create_post(db=db, post=post, owner_id=current_user.id)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a post (owner only).
    
    Args:
        post_id: Post ID to update
        post_update: Post update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated post information
        
    Raises:
        HTTPException: If post not found or user not authorized
    """
    updated_post = PostService.update_post(
        db=db, 
        post_id=post_id, 
        post_update=post_update,
        owner_id=current_user.id
    )
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to update it"
        )
    return updated_post


@router.delete("/{post_id}", response_model=MessageResponse)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a post (owner only).
    
    Args:
        post_id: Post ID to delete
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If post not found or user not authorized
    """
    success = PostService.delete_post(
        db=db, 
        post_id=post_id,
        owner_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to delete it"
        )
    return MessageResponse(message="Post deleted successfully")
