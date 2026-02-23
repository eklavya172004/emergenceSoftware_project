"""
Database Migration Guide
Easily switch between SQLite and PostgreSQL
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def migrate_sqlite_to_postgresql(source_db: str, target_connection_string: str):
    """
    Migrate data from SQLite to PostgreSQL
    
    Args:
        source_db: Path to SQLite database file (e.g., "portfolio.db")
        target_connection_string: PostgreSQL connection string
    """
    from sqlalchemy import create_engine, inspect, text
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Create engines
        source_engine = create_engine(f"sqlite:///{source_db}")
        target_engine = create_engine(target_connection_string)
        
        logger.info(f"Connecting to source SQLite: {source_db}")
        logger.info(f"Connecting to target PostgreSQL: {target_connection_string}")
        
        # Get source metadata
        source_inspector = inspect(source_engine)
        source_tables = source_inspector.get_table_names()
        
        logger.info(f"Found {len(source_tables)} tables to migrate: {source_tables}")
        
        # Migrate each table
        with source_engine.connect() as source_conn:
            with target_engine.connect() as target_conn:
                for table_name in source_tables:
                    logger.info(f"Migrating table: {table_name}")
                    
                    # Copy table structure and data
                    source_data = source_conn.execute(text(f"SELECT * FROM {table_name}"))
                    
                    rows = source_data.fetchall()
                    if rows:
                        columns = [col[0] for col in source_data.keys()]
                        
                        for row in rows:
                            placeholders = ','.join([f"${i+1}" for i in range(len(columns))])
                            insert_sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
                            target_conn.execute(text(insert_sql), dict(zip(columns, row)))
                        
                        target_conn.commit()
                        logger.info(f"✅ Migrated {len(rows)} rows from {table_name}")
                    else:
                        logger.info(f"Table {table_name} is empty, skipping data migration")
        
        logger.info("✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        return False


def setup_postgresql_docker():
    """
    Quick setup for PostgreSQL using Docker
    """
    setup_script = """
# Quick PostgreSQL setup with Docker

# 1. Install Docker (https://www.docker.com/products/docker-desktop)

# 2. Run PostgreSQL container
docker run --name portfolio_db \\
  -e POSTGRES_USER=portfolio_user \\
  -e POSTGRES_PASSWORD=portfolio_pass \\
  -e POSTGRES_DB=portfolio \\
  -p 5432:5432 \\
  -d postgres:15

# 3. Update .env
DATABASE_URL=postgresql://portfolio_user:portfolio_pass@localhost:5432/portfolio

# 4. Install Python driver
pip install psycopg2-binary

# 5. Initialize database
python init_db.py

# To stop the container:
docker stop portfolio_db

# To start again:
docker start portfolio_db

# To remove container:
docker rm portfolio_db
    """
    return setup_script


def verify_migration():
    """
    Verify that migration was successful
    """
    verification_script = """
# Verification script

from sqlalchemy import create_engine, text
import os

# Check source database
source_db = "sqlite:///./portfolio.db"
source_engine = create_engine(source_db)

# Check target database
target_db = os.getenv("DATABASE_URL", "sqlite:///./portfolio.db")
target_engine = create_engine(target_db)

def count_records(engine, table_name):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        return result.scalar()

tables = ["conversations", "messages", "resume_data"]

print("\\n=== Migration Verification ===\\n")

for table in tables:
    try:
        source_count = count_records(source_engine, table)
        target_count = count_records(target_engine, table)
        
        status = "✅" if source_count == target_count else "❌"
        print(f"{status} {table:20} | Source: {source_count:5} | Target: {target_count:5}")
    except Exception as e:
        print(f"❌ {table:20} | Error: {str(e)}")

print("\\n" + "="*60)
    """
    return verification_script


def backup_sqlite():
    """
    Create backup of SQLite database
    """
    import shutil
    from datetime import datetime
    
    source = "portfolio.db"
    if os.path.exists(source):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"portfolio_backup_{timestamp}.db"
        shutil.copy2(source, backup_name)
        print(f"✅ Database backed up to: {backup_name}")
        return backup_name
    else:
        print(f"❌ Database file not found: {source}")
        return None


# Configuration guide
SWITCH_GUIDE = """
# How to Switch Between SQLite and PostgreSQL

## Option 1: Fresh Start (Easy)
If you haven't saved important conversations yet:

1. Delete old database:
   rm portfolio.db

2. Update .env:
   DATABASE_URL=postgresql://user:pass@localhost:5432/portfolio

3. Run setup:
   python init_db.py

TIP: Best for development environments

---

## Option 2: Migrate Data (Recommended)
If you have important conversations to keep:

1. Backup SQLite:
   python -c "from migrate import backup_sqlite; backup_sqlite()"

2. Setup PostgreSQL (see setup_postgresql_docker())

3. Update .env:
   DATABASE_URL=postgresql://user:pass@localhost:5432/portfolio

4. Install PostgreSQL driver:
   pip install psycopg2-binary

5. Run migration:
   python -c "from migrate import migrate_sqlite_to_postgresql; \
   migrate_sqlite_to_postgresql('portfolio.db', 'postgresql://...')"

6. Verify:
   python -c "from migrate import verify_migration; verify_migration()"

TIP: Safe, keeps all data

---

## Production Switch Checklist

- [ ] Backup SQLite database
- [ ] Setup PostgreSQL (local or cloud)
- [ ] Test migration in staging
- [ ] Update .env in production
- [ ] Run migration
- [ ] Verify data integrity
- [ ] Test application
- [ ] Monitor for issues
- [ ] Keep backup for rollback
"""

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration tools")
    parser.add_argument("--backup", action="store_true", help="Backup SQLite database")
    parser.add_argument("--migrate", action="store_true", help="Show migration instructions")
    parser.add_argument("--docker", action="store_true", help="Show Docker setup")
    parser.add_argument("--verify", action="store_true", help="Show verification script")
    
    args = parser.parse_args()
    
    if args.backup:
        backup_sqlite()
    elif args.migrate:
        print(SWITCH_GUIDE)
    elif args.docker:
        print(setup_postgresql_docker())
    elif args.verify:
        print(verify_migration())
    else:
        print(SWITCH_GUIDE)
