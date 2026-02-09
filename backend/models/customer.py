"""Customer model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class Customer(Base):
    """Customer model for storing migrated customers."""
    
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    migration_job_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Source identifiers
    shopify_id = Column(String, nullable=True, index=True)
    woocommerce_id = Column(Integer, nullable=True, index=True)
    
    # Customer information
    email = Column(String, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # Status
    accepts_marketing = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Addresses
    default_address = Column(JSON, nullable=True)
    addresses = Column(JSON, nullable=True)  # List of addresses
    
    # Customer groups/tags
    tags = Column(JSON, nullable=True)
    groups = Column(JSON, nullable=True)
    
    # Statistics
    total_orders = Column(Integer, default=0)
    total_spent = Column(String, nullable=True)
    
    # Loyalty points (if applicable)
    loyalty_points = Column(Integer, default=0)
    
    # Additional data
    notes = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Migration status
    migration_status = Column(String, default="pending")
    migration_error = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Customer {self.email}>"
    
    @property
    def full_name(self):
        """Get customer's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or "Unknown"
