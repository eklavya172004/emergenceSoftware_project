"""Initialize the database with tables."""
import logging
from app.database import init_db, drop_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Initialize the database."""
    logger.info("Initializing database...")
    
    try:
        init_db()
        logger.info("✅ Database initialized successfully!")
        logger.info("Database file: portfolio.db")
        logger.info("Tables created: conversations, messages, resume_data")
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        raise


if __name__ == "__main__":
    main()
