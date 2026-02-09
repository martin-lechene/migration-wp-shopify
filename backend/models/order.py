"""Order model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class Order(Base):
    """Order model for storing migrated orders."""
    
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    migration_job_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Source identifiers
    shopify_id = Column(String, nullable=True, index=True)
    woocommerce_id = Column(Integer, nullable=True, index=True)
    
    # Order information
    order_number = Column(String, nullable=False, index=True)
    customer_email = Column(String, nullable=True)
    customer_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Financial
    total_price = Column(Float, nullable=False)
    subtotal_price = Column(Float, nullable=True)
    total_tax = Column(Float, nullable=True)
    total_shipping = Column(Float, nullable=True)
    total_discounts = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    
    # Status
    financial_status = Column(String, nullable=True)  # paid, pending, refunded, etc.
    fulfillment_status = Column(String, nullable=True)  # fulfilled, partial, unfulfilled
    
    # Line items
    line_items = Column(JSON, nullable=True)  # Order products
    
    # Addresses
    billing_address = Column(JSON, nullable=True)
    shipping_address = Column(JSON, nullable=True)
    
    # Shipping
    shipping_lines = Column(JSON, nullable=True)
    
    # Discounts
    discount_codes = Column(JSON, nullable=True)
    
    # Payment
    payment_method = Column(String, nullable=True)
    
    # Additional data
    notes = Column(Text, nullable=True)
    customer_note = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Migration status
    migration_status = Column(String, default="pending")
    migration_error = Column(Text, nullable=True)
    
    # Timestamps
    order_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Order {self.order_number}>"
