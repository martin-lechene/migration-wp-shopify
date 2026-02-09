"""Shopify API service client."""
from typing import List, Dict, Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

from config.settings import settings
from core.exceptions import APIConnectionError, RateLimitError

logger = structlog.get_logger()


class ShopifyService:
    """Service for interacting with Shopify API."""
    
    def __init__(self):
        """Initialize Shopify service."""
        self.shop_name = settings.SHOPIFY_SHOP_NAME
        self.access_token = settings.SHOPIFY_ACCESS_TOKEN
        self.api_version = settings.SHOPIFY_API_VERSION
        
        if not self.shop_name or not self.access_token:
            logger.warning("Shopify credentials not configured")
        
        self.base_url = f"https://{self.shop_name}/admin/api/{self.api_version}"
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Shopify API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            Dict: API response data
            
        Raises:
            APIConnectionError: If API request fails
            RateLimitError: If rate limit is exceeded
        """
        url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=data,
                    timeout=30.0
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After", 2)
                    raise RateLimitError(
                        "Shopify rate limit exceeded",
                        details={"retry_after": retry_after}
                    )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(
                    "Shopify API error",
                    status_code=e.response.status_code,
                    response_text=e.response.text
                )
                raise APIConnectionError(
                    f"Shopify API error: {e.response.status_code}",
                    details={"response": e.response.text}
                )
            except httpx.RequestError as e:
                logger.error("Shopify connection error", error=str(e))
                raise APIConnectionError(
                    "Failed to connect to Shopify API",
                    details={"error": str(e)}
                )
    
    async def test_connection(self) -> bool:
        """
        Test Shopify API connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            await self._make_request("GET", "shop.json")
            logger.info("Shopify connection test successful")
            return True
        except Exception as e:
            logger.error("Shopify connection test failed", error=str(e))
            return False
    
    async def get_products(
        self,
        limit: int = 50,
        since_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get products from Shopify.
        
        Args:
            limit: Number of products to fetch
            since_id: Get products after this ID
            
        Returns:
            List[Dict]: List of products
        """
        params = {"limit": limit}
        if since_id:
            params["since_id"] = since_id
        
        response = await self._make_request("GET", "products.json", params=params)
        return response.get("products", [])
    
    async def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        Get single product by ID.
        
        Args:
            product_id: Shopify product ID
            
        Returns:
            Dict: Product data
        """
        response = await self._make_request("GET", f"products/{product_id}.json")
        return response.get("product", {})
    
    async def get_product_count(self) -> int:
        """
        Get total count of products.
        
        Returns:
            int: Number of products
        """
        response = await self._make_request("GET", "products/count.json")
        return response.get("count", 0)
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product in Shopify.
        
        Args:
            product_data: Product data
            
        Returns:
            Dict: Created product data
        """
        response = await self._make_request(
            "POST",
            "products.json",
            data={"product": product_data}
        )
        return response.get("product", {})
    
    async def update_product(
        self,
        product_id: int,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing product.
        
        Args:
            product_id: Shopify product ID
            product_data: Updated product data
            
        Returns:
            Dict: Updated product data
        """
        response = await self._make_request(
            "PUT",
            f"products/{product_id}.json",
            data={"product": product_data}
        )
        return response.get("product", {})
    
    async def get_customers(
        self,
        limit: int = 50,
        since_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get customers from Shopify.
        
        Args:
            limit: Number of customers to fetch
            since_id: Get customers after this ID
            
        Returns:
            List[Dict]: List of customers
        """
        params = {"limit": limit}
        if since_id:
            params["since_id"] = since_id
        
        response = await self._make_request("GET", "customers.json", params=params)
        return response.get("customers", [])
    
    async def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """
        Get single customer by ID.
        
        Args:
            customer_id: Shopify customer ID
            
        Returns:
            Dict: Customer data
        """
        response = await self._make_request("GET", f"customers/{customer_id}.json")
        return response.get("customer", {})
    
    async def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new customer in Shopify.
        
        Args:
            customer_data: Customer data
            
        Returns:
            Dict: Created customer data
        """
        response = await self._make_request(
            "POST",
            "customers.json",
            data={"customer": customer_data}
        )
        return response.get("customer", {})
    
    async def get_orders(
        self,
        limit: int = 50,
        since_id: Optional[int] = None,
        status: str = "any"
    ) -> List[Dict[str, Any]]:
        """
        Get orders from Shopify.
        
        Args:
            limit: Number of orders to fetch
            since_id: Get orders after this ID
            status: Order status filter
            
        Returns:
            List[Dict]: List of orders
        """
        params = {"limit": limit, "status": status}
        if since_id:
            params["since_id"] = since_id
        
        response = await self._make_request("GET", "orders.json", params=params)
        return response.get("orders", [])
    
    async def get_order(self, order_id: int) -> Dict[str, Any]:
        """
        Get single order by ID.
        
        Args:
            order_id: Shopify order ID
            
        Returns:
            Dict: Order data
        """
        response = await self._make_request("GET", f"orders/{order_id}.json")
        return response.get("order", {})
    
    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order in Shopify.
        
        Args:
            order_data: Order data
            
        Returns:
            Dict: Created order data
        """
        response = await self._make_request(
            "POST",
            "orders.json",
            data={"order": order_data}
        )
        return response.get("order", {})
