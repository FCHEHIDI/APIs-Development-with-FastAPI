"""
API router configuration.
"""
from fastapi import APIRouter
from app.api.routes import auth, users, posts, admin, health

api_router = APIRouter()

# Include route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
