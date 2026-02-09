"""Migration job model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
from core.database import Base


class MigrationStatus(str, enum.Enum):
    """Migration job status."""
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MigrationDirection(str, enum.Enum):
    """Migration direction."""
    SHOPIFY_TO_WOOCOMMERCE = "shopify_to_woocommerce"
    WOOCOMMERCE_TO_SHOPIFY = "woocommerce_to_shopify"


class MigrationMode(str, enum.Enum):
    """Migration mode."""
    FULL = "full"
    INCREMENTAL = "incremental"
    TEST = "test"
    BATCH = "batch"


class MigrationJob(Base):
    """Migration job model."""
    
    __tablename__ = "migration_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Migration configuration
    direction = Column(SQLEnum(MigrationDirection), nullable=False)
    mode = Column(SQLEnum(MigrationMode), nullable=False)
    entities = Column(JSON, nullable=False)  # List of entities to migrate
    
    # Status and progress
    status = Column(SQLEnum(MigrationStatus), default=MigrationStatus.PENDING)
    progress = Column(Integer, default=0)  # Percentage 0-100
    
    # Counts
    total_items = Column(Integer, default=0)
    migrated_items = Column(Integer, default=0)
    failed_items = Column(Integer, default=0)
    skipped_items = Column(Integer, default=0)
    
    # Configuration options
    config = Column(JSON, nullable=True)  # Additional config options
    
    # Results and errors
    results = Column(JSON, nullable=True)  # Migration results
    errors = Column(JSON, nullable=True)  # List of errors
    error_message = Column(Text, nullable=True)  # Main error message
    
    # Celery task ID
    celery_task_id = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MigrationJob {self.id} - {self.status}>"
    
    @property
    def duration(self):
        """Calculate job duration."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (datetime.utcnow() - self.started_at).total_seconds()
        return 0
