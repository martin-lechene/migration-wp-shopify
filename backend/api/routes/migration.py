"""Migration API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from datetime import datetime
import structlog

from core.database import get_db
from core.dependencies import get_current_user
from models.user import User
from models.migration import MigrationJob, MigrationStatus, MigrationDirection, MigrationMode
from services.product_migration_service import ProductMigrationService

logger = structlog.get_logger()

router = APIRouter()


class MigrationConfig(BaseModel):
    """Migration configuration model."""
    direction: str
    mode: str
    entities: List[str]
    batch_size: Optional[int] = 50
    optimize_images: Optional[bool] = True
    generate_redirects: Optional[bool] = False


class MigrationResponse(BaseModel):
    """Migration response model."""
    job_id: str
    status: str
    created_at: datetime
    message: str


class MigrationJobResponse(BaseModel):
    """Migration job detail response."""
    id: str
    direction: str
    mode: str
    status: str
    progress: int
    total_items: int
    migrated_items: int
    failed_items: int
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


@router.post("/start", response_model=MigrationResponse)
async def start_migration(
    config: MigrationConfig,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start a new migration job.
    
    Args:
        config: Migration configuration
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        MigrationResponse: Migration job details
    """
    # Validate direction and mode
    try:
        direction = MigrationDirection(config.direction)
        mode = MigrationMode(config.mode)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid direction or mode")
    
    # Create migration job
    job = MigrationJob(
        user_id=str(current_user.id),
        direction=direction,
        mode=mode,
        entities=config.entities,
        status=MigrationStatus.QUEUED,
        config={
            'batch_size': config.batch_size,
            'optimize_images': config.optimize_images,
            'generate_redirects': config.generate_redirects
        }
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Add migration to background tasks
    # background_tasks.add_task(run_migration_task, str(job.id))
    
    logger.info(
        "Migration job created",
        job_id=str(job.id),
        direction=config.direction,
        mode=config.mode,
        user_id=str(current_user.id)
    )
    
    return MigrationResponse(
        job_id=str(job.id),
        status=job.status.value,
        created_at=job.created_at,
        message="Migration job created successfully"
    )


@router.get("/jobs", response_model=List[MigrationJobResponse])
async def list_migration_jobs(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List migration jobs for current user.
    
    Args:
        skip: Number of jobs to skip
        limit: Maximum number of jobs to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[MigrationJobResponse]: List of migration jobs
    """
    jobs = db.query(MigrationJob).filter(
        MigrationJob.user_id == str(current_user.id)
    ).order_by(MigrationJob.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        MigrationJobResponse(
            id=str(job.id),
            direction=job.direction.value,
            mode=job.mode.value,
            status=job.status.value,
            progress=job.progress,
            total_items=job.total_items,
            migrated_items=job.migrated_items,
            failed_items=job.failed_items,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at
        )
        for job in jobs
    ]


@router.get("/jobs/{job_id}", response_model=MigrationJobResponse)
async def get_migration_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get migration job details.
    
    Args:
        job_id: Migration job ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        MigrationJobResponse: Migration job details
    """
    job = db.query(MigrationJob).filter(
        MigrationJob.id == job_id,
        MigrationJob.user_id == str(current_user.id)
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Migration job not found")
    
    return MigrationJobResponse(
        id=str(job.id),
        direction=job.direction.value,
        mode=job.mode.value,
        status=job.status.value,
        progress=job.progress,
        total_items=job.total_items,
        migrated_items=job.migrated_items,
        failed_items=job.failed_items,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at
    )


@router.post("/jobs/{job_id}/cancel")
async def cancel_migration_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a migration job.
    
    Args:
        job_id: Migration job ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict: Cancellation status
    """
    job = db.query(MigrationJob).filter(
        MigrationJob.id == job_id,
        MigrationJob.user_id == str(current_user.id)
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Migration job not found")
    
    if job.status in [MigrationStatus.COMPLETED, MigrationStatus.CANCELLED]:
        raise HTTPException(status_code=400, detail="Job is already completed or cancelled")
    
    job.status = MigrationStatus.CANCELLED
    job.completed_at = datetime.utcnow()
    db.commit()
    
    logger.info("Migration job cancelled", job_id=str(job.id))
    
    return {"message": "Migration job cancelled successfully"}
