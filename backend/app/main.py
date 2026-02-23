"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .config import settings
from .api import chat, database
from .database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Could not initialize database: {e}")
    
    app = FastAPI(
        title="Portfolio API",
        description="AI-powered portfolio with chat functionality",
        version="1.0.0",
    )
    
    # Configure CORS with sensible defaults
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
    app.include_router(database.router, prefix="/api/v1/conversations", tags=["conversations"])
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": "1.0.0",
            "message": "Portfolio API is running",
            "database_type": "sqlite" if "sqlite" in settings.database_url else "postgresql"
        }
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Welcome to Portfolio API",
            "docs": "/docs",
            "health": "/health",
            "chat": "/api/v1/chat",
            "conversations": "/api/v1/conversations"
        }
    
    logger.info("FastAPI application created successfully")
    return app


# Create the app instance
app = create_app()
