"""Orders API routes - placeholder."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_orders():
    """List orders endpoint - placeholder."""
    return {"message": "Orders endpoint"}
