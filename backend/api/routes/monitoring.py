"""Monitoring API routes - placeholder."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user
from models.user import User
from models.migration import MigrationJob

router = APIRouter()


@router.get("/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get migration statistics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict: Migration statistics
    """
    total_jobs = db.query(MigrationJob).filter(
        MigrationJob.user_id == str(current_user.id)
    ).count()
    
    return {
        "total_jobs": total_jobs,
        "active_jobs": 0,
        "completed_jobs": 0,
        "failed_jobs": 0
    }
