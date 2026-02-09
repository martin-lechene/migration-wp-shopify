"""Customers API routes - placeholder."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_customers():
    """List customers endpoint - placeholder."""
    return {"message": "Customers endpoint"}
