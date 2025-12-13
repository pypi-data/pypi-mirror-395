from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session
from ..core_lib_config.settings import DBSettings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# CRITICAL FIX (2025-10-28): Singleton engine pattern to prevent connection leaks
#
# PROBLEM: Previous implementation created a new engine for EVERY call to get_db_session(),
# causing connection pool exhaustion. Each engine creates its own connection pool that never
# gets cleaned up, leading to "server closed the connection unexpectedly" errors.
#
# ROOT CAUSE:
# - Workers called get_db_session() once in __init__ and reused the same session forever
# - If PostgreSQL closed the connection (idle timeout), the session became stale
# - Creating new engines on every call leaked connection pools
#
# SOLUTION:
# - Single global engine with proper connection pool configuration
# - Pre-ping connections before use (detects stale connections)
# - Pool recycle to prevent long-lived stale connections
# - Proper pool size limits to prevent exhaustion
# - Sessions are properly scoped and should be closed after use
#
# CONFIGURATION:
# - pool_size=5: Max persistent connections per worker
# - max_overflow=10: Additional connections under load (total 15 max)
# - pool_pre_ping=True: Test connection before use (auto-reconnect if stale)
# - pool_recycle=3600: Recycle connections after 1 hour (prevent PostgreSQL idle timeout)
# - echo_pool=False: Disable connection pool debug logging in production

_engine: Optional[any] = None
_SessionLocal: Optional[sessionmaker] = None

def get_engine(db_settings: DBSettings):
    """
    Get or create the singleton SQLAlchemy engine with proper connection pool configuration.
    
    This ensures only ONE engine (and thus ONE connection pool) exists per worker process.
    """
    global _engine
    
    if _engine is None:
        logger.info("Creating SQLAlchemy engine with connection pool configuration...")
        logger.info(f"Database URL: {db_settings.database_url.split('@')[1] if '@' in db_settings.database_url else 'configured'}")
        
        _engine = create_engine(
            db_settings.database_url,
            # Connection pool configuration
            poolclass=pool.QueuePool,  # Default pool, suitable for multi-threaded apps
            pool_size=5,                # Core pool size: 5 persistent connections
            max_overflow=10,            # Allow 10 additional connections under load (15 total max)
            pool_timeout=30,            # Wait 30s for available connection before raising error
            pool_recycle=3600,          # Recycle connections after 1 hour (prevent stale)
            pool_pre_ping=True,         # Test connection liveness before use (auto-reconnect if dead)
            echo_pool=False,            # Set to True for pool debug logging
            
            # Connection behavior
            connect_args={
                "connect_timeout": 10,           # Connection establishment timeout
                "keepalives": 1,                 # Enable TCP keepalives
                "keepalives_idle": 30,           # Start keepalives after 30s idle
                "keepalives_interval": 10,       # Send keepalive every 10s
                "keepalives_count": 5,           # Drop connection after 5 failed keepalives
            },
        )
        
        # Log connection pool events for debugging
        @event.listens_for(_engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            logger.debug("Database connection established")
        
        @event.listens_for(_engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            logger.debug("Connection checked out from pool")
        
        @event.listens_for(_engine, "checkin")
        def receive_checkin(dbapi_conn, connection_record):
            logger.debug("Connection returned to pool")
        
        logger.info("✓ SQLAlchemy engine created with connection pool (size=5, max_overflow=10, pool_recycle=3600s)")
    
    return _engine

def get_session_factory(db_settings: DBSettings):
    """
    Get or create the singleton session factory.
    
    Sessions created from this factory share the same connection pool.
    """
    global _SessionLocal
    
    if _SessionLocal is None:
        engine = get_engine(db_settings)
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False,  # Prevent lazy-load errors after commit
        )
        logger.info("✓ Session factory created")
    
    return _SessionLocal

def get_db_session(db_settings: DBSettings) -> Session:
    """
    Creates a new database session from the singleton session factory.
    
    IMPORTANT: The caller MUST close the session after use:
        session = get_db_session(db_settings)
        try:
            # Use session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()  # CRITICAL: Release connection back to pool
    
    Or use as context manager:
        with get_db_session(db_settings) as session:
            # Use session
            session.commit()
    
    Args:
        db_settings: The database connection settings.
    
    Returns:
        A new SQLAlchemy Session object from the singleton pool.
    """
    session_factory = get_session_factory(db_settings)
    session = session_factory()
    logger.debug("New database session created from pool")
    return session

def close_db_connections():
    """
    Close all database connections and dispose of the engine.
    
    Call this during application shutdown to cleanly release all database resources.
    """
    global _engine, _SessionLocal
    
    if _engine is not None:
        logger.info("Disposing SQLAlchemy engine and closing all connections...")
        _engine.dispose()
        _engine = None
        _SessionLocal = None
        logger.info("✓ All database connections closed")

def get_pool_status(db_settings: DBSettings) -> Dict[str, Any]:
    """
    Get current connection pool status for monitoring and debugging.
    
    Returns a dictionary with pool metrics:
    - size: Current number of connections in pool
    - checked_out: Number of connections currently in use
    - overflow: Number of connections beyond pool_size
    - total: Total connections (size + overflow)
    - max_overflow: Maximum allowed overflow connections
    - available: Connections available for checkout
    
    Args:
        db_settings: The database connection settings.
    
    Returns:
        Dictionary with pool status metrics.
    """
    engine = get_engine(db_settings)
    pool_obj = engine.pool
    
    status = {
        "pool_size": pool_obj.size(),
        "checked_out": pool_obj.checkedout(),
        "overflow": pool_obj.overflow(),
        "total_connections": pool_obj.size() + pool_obj.overflow(),
        "max_overflow": pool_obj._max_overflow,
        "available": pool_obj.size() - pool_obj.checkedout(),
        "pool_class": pool_obj.__class__.__name__,
    }
    
    return status

def log_pool_status(db_settings: DBSettings, prefix: str = ""):
    """
    Log current pool status for monitoring.
    
    Usage in workers:
        # Periodically log pool health
        log_pool_status(db_settings, "[Worker Health Check]")
        
        # After processing a batch of jobs
        log_pool_status(db_settings, "[After Job Batch]")
    
    Args:
        db_settings: The database connection settings.
        prefix: Optional prefix for the log message.
    """
    status = get_pool_status(db_settings)
    logger.info(
        f"{prefix} Pool Status: "
        f"{status['checked_out']}/{status['pool_size']} in use, "
        f"{status['available']} available, "
        f"{status['overflow']} overflow, "
        f"{status['total_connections']} total"
    )