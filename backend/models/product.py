"""Product model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class Product(Base):
    """Product model for storing migrated products."""
    
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    migration_job_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Source identifiers
    shopify_id = Column(String, nullable=True, index=True)
    woocommerce_id = Column(Integer, nullable=True, index=True)
    
    # Product data
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    sku = Column(String, nullable=True, index=True)
    barcode = Column(String, nullable=True)
    
    # Pricing
    price = Column(Float, nullable=True)
    compare_at_price = Column(Float, nullable=True)
    cost = Column(Float, nullable=True)
    
    # Inventory
    quantity = Column(Integer, default=0)
    track_inventory = Column(Boolean, default=True)
    
    # Product type and categorization
    product_type = Column(String, nullable=True)
    vendor = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    categories = Column(JSON, nullable=True)  # List of categories
    
    # SEO
    seo_title = Column(String, nullable=True)
    seo_description = Column(Text, nullable=True)
    slug = Column(String, nullable=True)
    
    # Images
    images = Column(JSON, nullable=True)  # List of image URLs
    
    # Variants
    has_variants = Column(Boolean, default=False)
    variants = Column(JSON, nullable=True)  # Product variants data
    
    # Additional data
    metadata = Column(JSON, nullable=True)
    
    # Migration status
    migration_status = Column(String, default="pending")
    migration_error = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product {self.title}>"
