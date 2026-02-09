"""Custom exceptions and exception handlers."""
from typing import Any
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import structlog

logger = structlog.get_logger()


class MigratorException(Exception):
    """Base exception for migrator application."""
    
    def __init__(self, message: str, status_code: int = 500, details: Any = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class AuthenticationError(MigratorException):
    """Authentication failed."""
    
    def __init__(self, message: str = "Authentication failed", details: Any = None):
        super().__init__(message, status_code=401, details=details)


class AuthorizationError(MigratorException):
    """User not authorized."""
    
    def __init__(self, message: str = "Not authorized", details: Any = None):
        super().__init__(message, status_code=403, details=details)


class NotFoundError(MigratorException):
    """Resource not found."""
    
    def __init__(self, message: str = "Resource not found", details: Any = None):
        super().__init__(message, status_code=404, details=details)


class ValidationError(MigratorException):
    """Data validation error."""
    
    def __init__(self, message: str = "Validation error", details: Any = None):
        super().__init__(message, status_code=422, details=details)


class MigrationError(MigratorException):
    """Migration process error."""
    
    def __init__(self, message: str = "Migration failed", details: Any = None):
        super().__init__(message, status_code=500, details=details)


class APIConnectionError(MigratorException):
    """External API connection error."""
    
    def __init__(self, message: str = "API connection failed", details: Any = None):
        super().__init__(message, status_code=503, details=details)


class RateLimitError(MigratorException):
    """Rate limit exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Any = None):
        super().__init__(message, status_code=429, details=details)


def handle_exceptions(app: FastAPI) -> FastAPI:
    """
    Add exception handlers to FastAPI application.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        FastAPI: Application with exception handlers
    """
    
    @app.exception_handler(MigratorException)
    async def migrator_exception_handler(request: Request, exc: MigratorException):
        """Handle custom migrator exceptions."""
        logger.error(
            "Migrator exception",
            path=request.url.path,
            method=request.method,
            error=exc.message,
            status_code=exc.status_code,
            details=exc.details
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "details": exc.details,
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions."""
        logger.warning(
            "HTTP exception",
            path=request.url.path,
            method=request.method,
            status_code=exc.status_code,
            detail=exc.detail
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        logger.warning(
            "Validation error",
            path=request.url.path,
            method=request.method,
            errors=exc.errors()
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation error",
                "details": exc.errors(),
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(
            "Unexpected error",
            path=request.url.path,
            method=request.method,
            error=str(exc),
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": str(exc),
                "path": str(request.url.path)
            }
        )
    
    return app
