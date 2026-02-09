"""Webhooks API routes - placeholder."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/shopify")
async def shopify_webhook():
    """Shopify webhook endpoint - placeholder."""
    return {"message": "Shopify webhook received"}


@router.post("/woocommerce")
async def woocommerce_webhook():
    """WooCommerce webhook endpoint - placeholder."""
    return {"message": "WooCommerce webhook received"}
