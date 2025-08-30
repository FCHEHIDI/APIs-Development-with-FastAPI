"""
Admin dashboard routes for system management.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import User, Post
from app.api.dependencies.auth import get_current_superuser
from app.services.user_service import UserService
from app.services.post_service import PostService

router = APIRouter()


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_stats(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics (superuser only).
    
    Args:
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        Dashboard statistics
    """
    # User statistics
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    superusers = db.query(User).filter(User.is_superuser == True).count()
    
    # Post statistics
    total_posts = db.query(Post).count()
    published_posts = db.query(Post).filter(Post.is_published == True).count()
    draft_posts = total_posts - published_posts
    
    # Recent activity
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    recent_posts = db.query(Post).order_by(Post.created_at.desc()).limit(5).all()
    
    # Posts per user
    posts_per_user = db.query(
        User.username,
        func.count(Post.id).label('post_count')
    ).outerjoin(Post).group_by(User.id, User.username).all()
    
    return {
        "summary": {
            "total_users": total_users,
            "active_users": active_users,
            "superusers": superusers,
            "total_posts": total_posts,
            "published_posts": published_posts,
            "draft_posts": draft_posts
        },
        "recent_activity": {
            "recent_users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at.isoformat()
                }
                for user in recent_users
            ],
            "recent_posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "is_published": post.is_published,
                    "created_at": post.created_at.isoformat()
                }
                for post in recent_posts
            ]
        },
        "analytics": {
            "posts_per_user": [
                {"username": username, "post_count": count}
                for username, count in posts_per_user
            ]
        }
    }


@router.get("/users/stats", response_model=Dict[str, Any])
async def get_user_statistics(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get detailed user statistics (superuser only).
    
    Args:
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        User statistics
    """
    # User counts by status
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = total_users - active_users
    
    # Registration trends (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_registrations = db.query(User).filter(
        User.created_at >= thirty_days_ago
    ).count()
    
    return {
        "user_counts": {
            "total": total_users,
            "active": active_users,
            "inactive": inactive_users,
            "superusers": db.query(User).filter(User.is_superuser == True).count()
        },
        "trends": {
            "recent_registrations_30d": recent_registrations,
            "average_daily_registrations": round(recent_registrations / 30, 2)
        }
    }


@router.get("/posts/stats", response_model=Dict[str, Any])
async def get_post_statistics(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get detailed post statistics (superuser only).
    
    Args:
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        Post statistics
    """
    # Post counts by status
    total_posts = db.query(Post).count()
    published_posts = db.query(Post).filter(Post.is_published == True).count()
    draft_posts = total_posts - published_posts
    
    # Top authors
    top_authors = db.query(
        User.username,
        User.full_name,
        func.count(Post.id).label('post_count')
    ).join(Post).group_by(User.id, User.username, User.full_name)\
     .order_by(func.count(Post.id).desc()).limit(10).all()
    
    return {
        "post_counts": {
            "total": total_posts,
            "published": published_posts,
            "drafts": draft_posts,
            "publication_rate": round((published_posts / total_posts * 100), 2) if total_posts > 0 else 0
        },
        "top_authors": [
            {
                "username": username,
                "full_name": full_name,
                "post_count": count
            }
            for username, full_name, count in top_authors
        ]
    }
