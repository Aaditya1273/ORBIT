"""
ORBIT Database Configuration
SQLAlchemy database setup and session management
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import structlog

from ..core.config import settings

logger = structlog.get_logger(__name__)

# Create database engine
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # PostgreSQL configuration for production
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database with tables and initial data
    """
    from .models import Base, create_tables
    
    logger.info("Initializing database")
    create_tables(engine)
    logger.info("Database initialized successfully")


# Database event listeners for logging
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance"""
    if settings.DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=1000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()


@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log SQL queries in debug mode"""
    if settings.DEBUG and settings.LOG_LEVEL == "DEBUG":
        logger.debug("SQL Query", statement=statement, parameters=parameters)


# Database health check
async def check_database_health() -> dict:
    """
    Check database connectivity and performance
    """
    try:
        db = SessionLocal()
        
        # Simple query to test connectivity
        result = db.execute("SELECT 1").fetchone()
        
        if result and result[0] == 1:
            db.close()
            return {
                "status": "healthy",
                "message": "Database connection successful"
            }
        else:
            db.close()
            return {
                "status": "unhealthy",
                "message": "Database query failed"
            }
            
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "message": f"Database error: {str(e)}"
        }