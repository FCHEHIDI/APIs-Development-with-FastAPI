"""
Advanced health check routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.health_checks import check_database_health, check_system_resources, get_application_info
from typing import Dict, Any
import time

router = APIRouter()


@router.get("/health", tags=["Health"])
async def basic_health_check():
    """
    Basic health check - always returns healthy if app is running.
    Used by load balancers and container orchestrators.
    """
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


@router.get("/health/detailed", tags=["Health"])
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check with system monitoring.
    
    Returns:
        Detailed health status including database and system resources
    """
    # Check all components
    app_info = get_application_info()
    db_health = await check_database_health(db)
    system_health = check_system_resources()
    
    # Determine overall health
    overall_status = "healthy"
    if db_health["status"] != "healthy":
        overall_status = "unhealthy"
    elif system_health["status"] == "warning":
        overall_status = "warning"
    elif system_health["status"] == "unhealthy":
        overall_status = "unhealthy"
    
    health_data = {
        "status": overall_status,
        "timestamp": time.time(),
        "application": app_info,
        "database": db_health,
        "system": system_health,
        "checks_performed": [
            "application_info",
            "database_connectivity", 
            "system_resources"
        ]
    }
    
    # Return appropriate HTTP status
    if overall_status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_data
        )
    
    return health_data


@router.get("/health/ready", tags=["Health"])
async def readiness_check(db: Session = Depends(get_db)):
    """
    Kubernetes-style readiness check.
    Returns 200 if ready to serve traffic, 503 if not.
    """
    try:
        # Quick database connectivity check
        db_health = await check_database_health(db)
        
        if db_health["status"] == "healthy":
            return {"status": "ready"}
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={"status": "not_ready", "reason": "database_unavailable"}
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "reason": str(e)}
        )


@router.get("/health/live", tags=["Health"])
async def liveness_check():
    """
    Kubernetes-style liveness check.
    Returns 200 if application is alive (basic functionality).
    """
    return {"status": "alive", "timestamp": time.time()}
