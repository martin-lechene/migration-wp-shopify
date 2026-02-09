"""WooCommerce API service client."""
from typing import List, Dict, Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

from config.settings import settings
from core.exceptions import APIConnectionError, RateLimitError

logger = structlog.get_logger()


class WooCommerceService:
    """Service for interacting with WooCommerce API."""
    
    def __init__(self):
        """Initialize WooCommerce service."""
        self.url = settings.WOOCOMMERCE_URL
        self.consumer_key = settings.WOOCOMMERCE_CONSUMER_KEY
        self.consumer_secret = settings.WOOCOMMERCE_CONSUMER_SECRET
        self.api_version = settings.WOOCOMMERCE_API_VERSION
        
        if not self.url or not self.consumer_key or not self.consumer_secret:
            logger.warning("WooCommerce credentials not configured")
        
        self.base_url = f"{self.url}/wp-json/{self.api_version}"
        self.auth = (self.consumer_key, self.consumer_secret)
    
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
    ) -> Any:
        """
        Make HTTP request to WooCommerce API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            Response data (Dict or List)
            
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
                    auth=self.auth,
                    params=params,
                    json=data,
                    timeout=30.0
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    raise RateLimitError(
                        "WooCommerce rate limit exceeded",
                        details={"status_code": 429}
                    )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(
                    "WooCommerce API error",
                    status_code=e.response.status_code,
                    response_text=e.response.text
                )
                raise APIConnectionError(
                    f"WooCommerce API error: {e.response.status_code}",
                    details={"response": e.response.text}
                )
            except httpx.RequestError as e:
                logger.error("WooCommerce connection error", error=str(e))
                raise APIConnectionError(
                    "Failed to connect to WooCommerce API",
                    details={"error": str(e)}
                )
    
    async def test_connection(self) -> bool:
        """
        Test WooCommerce API connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            # Try to fetch system status
            await self._make_request("GET", "system_status")
            logger.info("WooCommerce connection test successful")
            return True
        except Exception as e:
            logger.error("WooCommerce connection test failed", error=str(e))
            return False
    
    async def get_products(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get products from WooCommerce.
        
        Args:
            page: Page number
            per_page: Number of products per page
            
        Returns:
            List[Dict]: List of products
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        response = await self._make_request("GET", "products", params=params)
        return response if isinstance(response, list) else []
    
    async def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        Get single product by ID.
        
        Args:
            product_id: WooCommerce product ID
            
        Returns:
            Dict: Product data
        """
        response = await self._make_request("GET", f"products/{product_id}")
        return response
    
    async def get_product_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        """
        Get product by SKU.
        
        Args:
            sku: Product SKU
            
        Returns:
            Optional[Dict]: Product data or None
        """
        params = {"sku": sku}
        response = await self._make_request("GET", "products", params=params)
        
        if isinstance(response, list) and len(response) > 0:
            return response[0]
        return None
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product in WooCommerce.
        
        Args:
            product_data: Product data
            
        Returns:
            Dict: Created product data
        """
        response = await self._make_request("POST", "products", data=product_data)
        return response
    
    async def update_product(
        self,
        product_id: int,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing product.
        
        Args:
            product_id: WooCommerce product ID
            product_data: Updated product data
            
        Returns:
            Dict: Updated product data
        """
        response = await self._make_request(
            "PUT",
            f"products/{product_id}",
            data=product_data
        )
        return response
    
    async def batch_create_products(
        self,
        products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Batch create products.
        
        Args:
            products: List of product data
            
        Returns:
            Dict: Batch operation results
        """
        response = await self._make_request(
            "POST",
            "products/batch",
            data={"create": products}
        )
        return response
    
    async def get_customers(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get customers from WooCommerce.
        
        Args:
            page: Page number
            per_page: Number of customers per page
            
        Returns:
            List[Dict]: List of customers
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        response = await self._make_request("GET", "customers", params=params)
        return response if isinstance(response, list) else []
    
    async def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """
        Get single customer by ID.
        
        Args:
            customer_id: WooCommerce customer ID
            
        Returns:
            Dict: Customer data
        """
        response = await self._make_request("GET", f"customers/{customer_id}")
        return response
    
    async def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new customer in WooCommerce.
        
        Args:
            customer_data: Customer data
            
        Returns:
            Dict: Created customer data
        """
        response = await self._make_request("POST", "customers", data=customer_data)
        return response
    
    async def get_orders(
        self,
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get orders from WooCommerce.
        
        Args:
            page: Page number
            per_page: Number of orders per page
            status: Order status filter
            
        Returns:
            List[Dict]: List of orders
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        if status:
            params["status"] = status
        
        response = await self._make_request("GET", "orders", params=params)
        return response if isinstance(response, list) else []
    
    async def get_order(self, order_id: int) -> Dict[str, Any]:
        """
        Get single order by ID.
        
        Args:
            order_id: WooCommerce order ID
            
        Returns:
            Dict: Order data
        """
        response = await self._make_request("GET", f"orders/{order_id}")
        return response
    
    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order in WooCommerce.
        
        Args:
            order_data: Order data
            
        Returns:
            Dict: Created order data
        """
        response = await self._make_request("POST", "orders", data=order_data)
        return response
    
    async def get_product_categories(self) -> List[Dict[str, Any]]:
        """
        Get product categories.
        
        Returns:
            List[Dict]: List of categories
        """
        response = await self._make_request("GET", "products/categories", params={"per_page": 100})
        return response if isinstance(response, list) else []
    
    async def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a product category.
        
        Args:
            category_data: Category data
            
        Returns:
            Dict: Created category data
        """
        response = await self._make_request("POST", "products/categories", data=category_data)
        return response
