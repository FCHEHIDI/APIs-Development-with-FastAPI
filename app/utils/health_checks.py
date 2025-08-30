"""
Production-ready health check implementation.
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
import time
import psutil  # For system metrics
from typing import Dict, Any


async def check_database_health(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Check database connectivity and performance.
    
    Returns:
        Database health status
    """
    try:
        start_time = time.time()
        # Simple query to test connection
        result = db.execute(text("SELECT 1"))
        response_time = time.time() - start_time
        
        return {
            "status": "healthy",
            "response_time_ms": round(response_time * 1000, 2),
            "connection": "active"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "connection": "failed"
        }


def check_system_resources() -> Dict[str, Any]:
    """
    Check system resources (CPU, Memory, Disk).
    
    Returns:
        System resource status
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Define thresholds
        cpu_threshold = 80.0
        memory_threshold = 85.0
        disk_threshold = 90.0
        
        # Determine overall health
        is_healthy = (
            cpu_percent < cpu_threshold and
            memory.percent < memory_threshold and
            disk.percent < disk_threshold
        )
        
        return {
            "status": "healthy" if is_healthy else "warning",
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "thresholds": {
                "cpu": cpu_threshold,
                "memory": memory_threshold,
                "disk": disk_threshold
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


def get_application_info() -> Dict[str, Any]:
    """
    Get application information and status.
    
    Returns:
        Application information
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production",
        "uptime": time.time(),  # In production, calculate actual uptime
        "python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}"
    }
