"""Product migration service - core migration logic for products."""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import structlog

from services.shopify_service import ShopifyService
from services.woocommerce_service import WooCommerceService
from services.image_service import ImageService
from models.product import Product
from models.migration import MigrationJob, MigrationDirection
from core.exceptions import MigrationError

logger = structlog.get_logger()


class ProductMigrationService:
    """Service for migrating products between platforms."""
    
    def __init__(self, db: Session):
        """
        Initialize product migration service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.shopify = ShopifyService()
        self.woocommerce = WooCommerceService()
        self.image_service = ImageService()
    
    def map_shopify_to_woocommerce(
        self,
        shopify_product: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Map Shopify product data to WooCommerce format.
        
        Args:
            shopify_product: Shopify product data
            
        Returns:
            Dict: WooCommerce product data
        """
        # Extract main variant (first variant)
        variants = shopify_product.get('variants', [])
        main_variant = variants[0] if variants else {}
        
        # Map basic fields
        wc_product = {
            'name': shopify_product.get('title', ''),
            'description': shopify_product.get('body_html', ''),
            'short_description': shopify_product.get('body_html', '')[:200] if shopify_product.get('body_html') else '',
            'sku': main_variant.get('sku', ''),
            'regular_price': str(main_variant.get('price', '0')),
            'sale_price': str(main_variant.get('compare_at_price', '')) if main_variant.get('compare_at_price') else '',
            'manage_stock': True,
            'stock_quantity': main_variant.get('inventory_quantity', 0),
            'type': 'simple' if len(variants) == 1 else 'variable',
            'status': 'publish' if shopify_product.get('status') == 'active' else 'draft',
        }
        
        # Map images
        images = []
        for img in shopify_product.get('images', []):
            images.append({'src': img.get('src', '')})
        wc_product['images'] = images
        
        # Map categories
        product_type = shopify_product.get('product_type', '')
        if product_type:
            wc_product['categories'] = [{'name': product_type}]
        
        # Map tags
        tags = shopify_product.get('tags', '').split(',')
        if tags:
            wc_product['tags'] = [{'name': tag.strip()} for tag in tags if tag.strip()]
        
        # SEO meta
        wc_product['meta_data'] = [
            {'key': '_yoast_wpseo_title', 'value': shopify_product.get('title', '')},
            {'key': '_shopify_product_id', 'value': str(shopify_product.get('id', ''))}
        ]
        
        return wc_product
    
    def map_woocommerce_to_shopify(
        self,
        wc_product: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Map WooCommerce product data to Shopify format.
        
        Args:
            wc_product: WooCommerce product data
            
        Returns:
            Dict: Shopify product data
        """
        shopify_product = {
            'title': wc_product.get('name', ''),
            'body_html': wc_product.get('description', ''),
            'product_type': '',
            'vendor': '',
            'tags': '',
            'status': 'active' if wc_product.get('status') == 'publish' else 'draft',
        }
        
        # Map categories to product type
        categories = wc_product.get('categories', [])
        if categories:
            shopify_product['product_type'] = categories[0].get('name', '')
        
        # Map tags
        tags = wc_product.get('tags', [])
        if tags:
            shopify_product['tags'] = ', '.join([tag.get('name', '') for tag in tags])
        
        # Map variant
        variant = {
            'sku': wc_product.get('sku', ''),
            'price': wc_product.get('regular_price', '0'),
            'inventory_quantity': wc_product.get('stock_quantity', 0),
            'inventory_management': 'shopify' if wc_product.get('manage_stock') else None,
        }
        
        if wc_product.get('sale_price'):
            variant['compare_at_price'] = wc_product.get('regular_price', '0')
            variant['price'] = wc_product.get('sale_price', '0')
        
        shopify_product['variants'] = [variant]
        
        # Map images
        images = []
        for img in wc_product.get('images', []):
            images.append({'src': img.get('src', '')})
        shopify_product['images'] = images
        
        return shopify_product
    
    async def migrate_product_shopify_to_woocommerce(
        self,
        shopify_product: Dict[str, Any],
        job_id: str
    ) -> Dict[str, Any]:
        """
        Migrate a single product from Shopify to WooCommerce.
        
        Args:
            shopify_product: Shopify product data
            job_id: Migration job ID
            
        Returns:
            Dict: Migration result
        """
        try:
            # Map product data
            wc_product_data = self.map_shopify_to_woocommerce(shopify_product)
            
            # Create product in WooCommerce
            wc_product = await self.woocommerce.create_product(wc_product_data)
            
            # Store in database
            product = Product(
                migration_job_id=job_id,
                shopify_id=str(shopify_product.get('id', '')),
                woocommerce_id=wc_product.get('id'),
                title=shopify_product.get('title', ''),
                sku=shopify_product.get('variants', [{}])[0].get('sku', ''),
                migration_status='completed'
            )
            self.db.add(product)
            self.db.commit()
            
            logger.info(
                "Product migrated successfully",
                shopify_id=shopify_product.get('id'),
                woocommerce_id=wc_product.get('id'),
                title=shopify_product.get('title')
            )
            
            return {
                'success': True,
                'shopify_id': shopify_product.get('id'),
                'woocommerce_id': wc_product.get('id')
            }
            
        except Exception as e:
            logger.error(
                "Product migration failed",
                shopify_id=shopify_product.get('id'),
                error=str(e)
            )
            
            # Store error in database
            product = Product(
                migration_job_id=job_id,
                shopify_id=str(shopify_product.get('id', '')),
                title=shopify_product.get('title', ''),
                migration_status='failed',
                migration_error=str(e)
            )
            self.db.add(product)
            self.db.commit()
            
            return {
                'success': False,
                'shopify_id': shopify_product.get('id'),
                'error': str(e)
            }
    
    async def migrate_products(
        self,
        job_id: str,
        direction: MigrationDirection,
        batch_size: int = 50,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Migrate products in batch.
        
        Args:
            job_id: Migration job ID
            direction: Migration direction
            batch_size: Number of products per batch
            limit: Maximum number of products to migrate
            
        Returns:
            Dict: Migration results
        """
        results = {
            'total': 0,
            'migrated': 0,
            'failed': 0,
            'errors': []
        }
        
        try:
            if direction == MigrationDirection.SHOPIFY_TO_WOOCOMMERCE:
                # Get products from Shopify
                products = await self.shopify.get_products(limit=batch_size)
                results['total'] = len(products)
                
                # Migrate each product
                for product in products:
                    result = await self.migrate_product_shopify_to_woocommerce(
                        product,
                        job_id
                    )
                    
                    if result['success']:
                        results['migrated'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append(result.get('error'))
                    
                    # Check limit
                    if limit and results['migrated'] >= limit:
                        break
            
            else:
                # WooCommerce to Shopify migration
                # Similar logic but reversed
                pass
            
        except Exception as e:
            logger.error("Batch migration failed", error=str(e))
            raise MigrationError(f"Batch migration failed: {str(e)}")
        
        return results
