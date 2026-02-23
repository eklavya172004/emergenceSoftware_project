"""Database configuration and session management."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment or use SQLite default
# Priority: 1) DATABASE_URL env 2) database_url env 3) SQLite default
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("database_url") or "sqlite:///./portfolio.db"

# Ensure we have a valid URL
if not DATABASE_URL or DATABASE_URL.strip() == "":
    logger.warning("DATABASE_URL is empty, using SQLite default")
    DATABASE_URL = "sqlite:///./portfolio.db"

# SQLite engine configuration
try:
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        logger.info(f"Using SQLite database")
    else:
        # PostgreSQL or MySQL
        engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
        logger.info(f"Using remote database (PostgreSQL/MySQL)")
except Exception as e:
    logger.error(f"Failed to create database engine with URL: {DATABASE_URL[:50]}...")
    logger.warning("Falling back to SQLite database")
    DATABASE_URL = "sqlite:///./portfolio.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency to get database session.
    Usage: def route(db: Session = Depends(get_db)):
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables."""
    try:
        from .models.db.models import Base  # Import after models are defined
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        logger.warning("Database initialization failed, but continuing...")


def drop_db():
    """Drop all tables (use with caution!)."""
    try:
        from .models.db.models import Base
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
    except Exception as e:
        logger.error(f"Error dropping database: {e}")
