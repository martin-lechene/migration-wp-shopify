"""Log model for tracking migration activities."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
from core.database import Base


class LogLevel(str, enum.Enum):
    """Log level enumeration."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Log(Base):
    """Log model for storing migration logs and events."""
    
    __tablename__ = "logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    migration_job_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Log data
    level = Column(SQLEnum(LogLevel), default=LogLevel.INFO, nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String, nullable=True)  # e.g., 'product_migration', 'api_error'
    
    # Context
    entity_type = Column(String, nullable=True)  # product, customer, order
    entity_id = Column(String, nullable=True)
    
    # Additional details
    details = Column(JSON, nullable=True)
    stack_trace = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<Log {self.level} - {self.message[:50]}>"
