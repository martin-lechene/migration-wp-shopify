"""Application settings and configuration."""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Application
    APP_NAME: str = "Shopify-WordPress Migrator"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = Field(default="change-me-in-production-please-very-secret-key")
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api"
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/migrator_db"
    )
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Celery
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0")
    CELERY_WORKER_CONCURRENCY: int = 4
    
    # Shopify
    SHOPIFY_SHOP_NAME: Optional[str] = None
    SHOPIFY_API_KEY: Optional[str] = None
    SHOPIFY_API_SECRET: Optional[str] = None
    SHOPIFY_ACCESS_TOKEN: Optional[str] = None
    SHOPIFY_API_VERSION: str = "2024-01"
    
    # WooCommerce
    WOOCOMMERCE_URL: Optional[str] = None
    WOOCOMMERCE_CONSUMER_KEY: Optional[str] = None
    WOOCOMMERCE_CONSUMER_SECRET: Optional[str] = None
    WOOCOMMERCE_API_VERSION: str = "wc/v3"
    
    # WordPress
    WORDPRESS_URL: Optional[str] = None
    WORDPRESS_USERNAME: Optional[str] = None
    WORDPRESS_PASSWORD: Optional[str] = None
    
    # Migration Settings
    BATCH_SIZE_PRODUCTS: int = 50
    BATCH_SIZE_CUSTOMERS: int = 100
    BATCH_SIZE_ORDERS: int = 50
    MAX_CONCURRENT_TASKS: int = 10
    RATE_LIMIT_WINDOW: int = 60
    RATE_LIMIT_CALLS: int = 40
    
    # Image Settings
    ENABLE_IMAGE_OPTIMIZATION: bool = True
    IMAGE_MAX_WIDTH: int = 2048
    IMAGE_MAX_HEIGHT: int = 2048
    IMAGE_QUALITY: int = 85
    IMAGE_FORMAT: str = "JPEG"
    IMAGE_STORAGE_PATH: str = "./tmp/images"
    
    # Backup Settings
    ENABLE_AUTO_BACKUP: bool = True
    BACKUP_PATH: str = "./backups"
    BACKUP_RETENTION_DAYS: int = 30
    
    # Email Notifications
    ENABLE_EMAIL_NOTIFICATIONS: bool = False
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    # Features
    FEATURE_SYNC_REAL_TIME: bool = False
    FEATURE_MULTI_CURRENCY: bool = True
    FEATURE_WEBHOOKS: bool = True
    FEATURE_ADVANCED_MAPPING: bool = True
    FEATURE_DIGITAL_PRODUCTS: bool = True
    FEATURE_LOYALTY_POINTS: bool = True
    FEATURE_BLOG_MIGRATION: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "./logs/app.log"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    SENTRY_DSN: Optional[str] = None
    
    # JWT
    JWT_SECRET_KEY: str = Field(default="jwt-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


# Create settings instance
settings = Settings()
