"""
Session management utilities for workers.

Provides a context manager for per-job session handling that ensures
connections are properly returned to the pool.
"""

from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session
from .session import get_db_session, log_pool_status
from ..core_lib_config.settings import DBSettings
import logging

logger = logging.getLogger(__name__)


@contextmanager
def job_session(db_settings: DBSettings, job_id: str = None) -> Generator[Session, None, None]:
    """
    Context manager for per-job database sessions.
    
    Automatically handles session lifecycle:
    - Creates fresh session from pool
    - Commits on success
    - Rollbacks on error
    - Always closes session to return connection to pool
    
    Usage in workers:
        class MyWorker(BaseWorker):
            def __init__(self):
                self.db_settings = DBSettings()
            
            async def process(self, job, job_token: str):
                with job_session(self.db_settings, job.id) as session:
                    # Use session for database operations
                    service = SomeService(session)
                    result = await service.do_work()
                    # session.commit() called automatically on success
                return result
    
    Args:
        db_settings: Database connection settings
        job_id: Optional job ID for logging context
    
    Yields:
        Active SQLAlchemy session
    
    Example:
        with job_session(db_settings, "job-123") as session:
            user = session.query(User).filter_by(id=user_id).first()
            user.last_active = datetime.now()
            # Commit happens automatically
    """
    session = get_db_session(db_settings)
    job_prefix = f"[Job {job_id}]" if job_id else "[Session]"
    
    try:
        logger.debug(f"{job_prefix} Database session created from pool")
        yield session
        session.commit()
        logger.debug(f"{job_prefix} Session committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"{job_prefix} Session rolled back due to error: {e}")
        raise
    finally:
        session.close()
        logger.debug(f"{job_prefix} Session closed, connection returned to pool")


def with_session_monitoring(db_settings: DBSettings, log_frequency: int = 10):
    """
    Decorator to add pool monitoring to worker process methods.
    
    Logs pool status every N job completions to detect connection leaks.
    
    Usage:
        class MyWorker(BaseWorker):
            def __init__(self):
                self.db_settings = DBSettings()
                self.job_count = 0
            
            @with_session_monitoring(db_settings, log_frequency=10)
            async def process(self, job, job_token: str):
                # Process job
                pass
    
    Args:
        db_settings: Database connection settings
        log_frequency: Log pool status every N jobs (default: 10)
    """
    def decorator(func):
        job_counter = [0]  # Use list to allow modification in nested function
        
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                job_counter[0] += 1
                
                # Log pool status periodically
                if job_counter[0] % log_frequency == 0:
                    log_pool_status(db_settings, f"[After {job_counter[0]} jobs]")
                
                return result
            except Exception as e:
                logger.error(f"Job failed, logging pool status for debugging")
                log_pool_status(db_settings, "[On Error]")
                raise
        
        return wrapper
    return decorator
