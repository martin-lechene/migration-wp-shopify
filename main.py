"""
Shopify to WordPress/WooCommerce Migration Tool
Main FastAPI Application
"""
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app
import structlog

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from api.routes import (
    auth,
    migration,
    products,
    customers,
    orders,
    monitoring,
    webhooks,
    backup
)
from core.database import engine, Base
from core.logging import setup_logging
from core.exceptions import handle_exceptions

# Setup structured logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Shopify-WordPress Migrator API", version=settings.APP_VERSION)
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-grade migration tool for Shopify to WordPress/WooCommerce",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add exception handling
app = handle_exceptions(app)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Compression Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Prometheus metrics endpoint
if settings.ENABLE_METRICS:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(migration.router, prefix="/api/migration", tags=["Migration"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(backup.router, prefix="/api/backup", tags=["Backup"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/info")
async def api_info():
    """API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "features": {
            "real_time_sync": settings.FEATURE_SYNC_REAL_TIME,
            "multi_currency": settings.FEATURE_MULTI_CURRENCY,
            "webhooks": settings.FEATURE_WEBHOOKS,
            "advanced_mapping": settings.FEATURE_ADVANCED_MAPPING,
            "digital_products": settings.FEATURE_DIGITAL_PRODUCTS,
            "loyalty_points": settings.FEATURE_LOYALTY_POINTS,
            "blog_migration": settings.FEATURE_BLOG_MIGRATION
        },
        "supported_platforms": {
            "source": ["Shopify", "WooCommerce"],
            "destination": ["WooCommerce", "Shopify"]
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
