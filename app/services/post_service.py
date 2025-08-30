"""
Post service layer for business logic.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Post, User
from app.schemas import PostCreate, PostUpdate


class PostService:
    """Service class for post operations."""
    
    @staticmethod
    def get_post(db: Session, post_id: int) -> Optional[Post]:
        """Get post by ID."""
        return db.query(Post).filter(Post.id == post_id).first()
    
    @staticmethod
    def get_posts(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        owner_id: Optional[int] = None,
        published_only: bool = False
    ) -> List[Post]:
        """Get posts with filtering and pagination."""
        query = db.query(Post)
        
        if owner_id:
            query = query.filter(Post.owner_id == owner_id)
        
        if published_only:
            query = query.filter(Post.is_published == True)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create_post(db: Session, post: PostCreate, owner_id: int) -> Post:
        """Create a new post."""
        db_post = Post(**post.dict(), owner_id=owner_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    
    @staticmethod
    def update_post(
        db: Session, 
        post_id: int, 
        post_update: PostUpdate,
        owner_id: Optional[int] = None
    ) -> Optional[Post]:
        """Update a post."""
        query = db.query(Post).filter(Post.id == post_id)
        
        # If owner_id is provided, ensure only the owner can update
        if owner_id:
            query = query.filter(Post.owner_id == owner_id)
        
        post = query.first()
        if not post:
            return None
        
        update_data = post_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post, field, value)
        
        db.commit()
        db.refresh(post)
        return post
    
    @staticmethod
    def delete_post(
        db: Session, 
        post_id: int,
        owner_id: Optional[int] = None
    ) -> bool:
        """Delete a post."""
        query = db.query(Post).filter(Post.id == post_id)
        
        # If owner_id is provided, ensure only the owner can delete
        if owner_id:
            query = query.filter(Post.owner_id == owner_id)
        
        post = query.first()
        if not post:
            return False
        
        db.delete(post)
        db.commit()
        return True
    
    @staticmethod
    def get_posts_count(
        db: Session,
        owner_id: Optional[int] = None,
        published_only: bool = False
    ) -> int:
        """Get total count of posts."""
        query = db.query(Post)
        
        if owner_id:
            query = query.filter(Post.owner_id == owner_id)
        
        if published_only:
            query = query.filter(Post.is_published == True)
        
        return query.count()
