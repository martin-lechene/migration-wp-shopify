"""Backup API routes - placeholder."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/create")
async def create_backup():
    """Create backup endpoint - placeholder."""
    return {"message": "Backup created"}


@router.get("/list")
async def list_backups():
    """List backups endpoint - placeholder."""
    return {"backups": []}
