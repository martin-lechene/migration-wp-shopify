"""Products API routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import structlog

from core.database import get_db
from core.dependencies import get_current_user
from models.user import User
from services.shopify_service import ShopifyService
from services.woocommerce_service import WooCommerceService

logger = structlog.get_logger()

router = APIRouter()


@router.get("/test-connection")
async def test_api_connections(
    current_user: User = Depends(get_current_user)
):
    """
    Test API connections to Shopify and WooCommerce.
    
    Args:
        current_user: Current authenticated user
        
    Returns:        Dict: Connection status for each platform
    """
    shopify = ShopifyService()
    woocommerce = WooCommerceService()
    
    shopify_status = await shopify.test_connection()
    woocommerce_status = await woocommerce.test_connection()
    
    return {
        "shopify": {
            "connected": shopify_status,
            "configured": bool(shopify.shop_name and shopify.access_token)
        },
        "woocommerce": {
            "connected": woocommerce_status,
            "configured": bool(woocommerce.url and woocommerce.consumer_key)
        }
    }
