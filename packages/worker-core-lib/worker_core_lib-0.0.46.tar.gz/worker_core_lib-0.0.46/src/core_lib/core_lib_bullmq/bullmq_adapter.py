"""
BullMQ adapter implementation of the WorkerBackendPort.

This adapter provides BullMQ-specific implementation for queue and worker
operations, maintaining compatibility with existing BullMQ-based code.
"""
import logging
from typing import Any, Dict, Optional, Callable

from bullmq import Queue, Worker
from redis.asyncio import Redis

from .worker_backend_port import WorkerBackendPort
from ..core_lib_config.settings import get_settings

logger = logging.getLogger(__name__)


class BullMQAdapter(WorkerBackendPort):
    """
    BullMQ implementation of the WorkerBackendPort interface.
    
    This adapter wraps BullMQ Queue and Worker functionality, providing
    a standardized interface for queue operations while maintaining all
    BullMQ-specific features and optimizations.
    """

    def __init__(self):
        """Initialize the BullMQ adapter with Redis connection."""
        self._redis_url: Optional[str] = None
        self._redis_client: Optional[Redis] = None
        self._queue_cache: Dict[str, Queue] = {}
        logger.info("BullMQAdapter initialized")

    def _get_redis_url(self) -> str:
        """Get or create Redis URL from settings."""
        if self._redis_url is None:
            settings = get_settings()
            self._redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
            logger.info(f"Initialized Redis URL: {self._redis_url}")
        return self._redis_url

    def _get_redis_client(self) -> Redis:
        """Get or create Redis client instance."""
        if self._redis_client is None:
            redis_url = self._get_redis_url()
            logger.info(f"Creating Redis client for URL: {redis_url}")
            self._redis_client = Redis.from_url(redis_url, decode_responses=False)
        return self._redis_client

    def _get_queue(self, queue_name: str) -> Queue:
        """
        Get or create a BullMQ Queue instance.
        
        Queues are cached to maintain connection context and prevent
        connection loss issues with the BullMQ library.
        
        Args:
            queue_name: Name of the queue
            
        Returns:
            BullMQ Queue instance
        """
        if queue_name not in self._queue_cache:
            logger.info(f"Creating and caching new BullMQ Queue instance for '{queue_name}'")
            redis_client = self._get_redis_client()
            self._queue_cache[queue_name] = Queue(queue_name, {"connection": redis_client})
        
        return self._queue_cache[queue_name]

    async def add_job(
        self, 
        queue_name: str, 
        job_name: str, 
        data: Dict[str, Any], 
        opts: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a job to a BullMQ queue with automatic retry configuration.

        Jobs are automatically configured with retry settings unless explicitly overridden:
        - 5 retry attempts (6 total tries including initial attempt)
        - Exponential backoff starting at 2000ms (2s, 4s, 8s, 16s, 32s)
        - Failed jobs retained for 24 hours for debugging
        - Completed jobs retained for 1 hour

        Args:
            queue_name: Name of the queue to add the job to
            job_name: Name/type of the job
            data: Job data/payload
            opts: Optional job options (will be merged with defaults)
                 - attempts: Override retry attempts
                 - backoff: Override backoff strategy
                 - removeOnComplete: Override completed job retention
                 - removeOnFail: Override failed job retention

        Returns:
            Job ID as a string

        Raises:
            Exception: If job addition fails
        """
        try:
            queue = self._get_queue(queue_name)
            
            # Default retry configuration matching worker-backend TypeScript config
            default_opts = {
                "attempts": 5,  # Retry up to 5 times (6 total tries)
                "backoff": {
                    "type": "exponential",
                    "delay": 2000  # Start at 2s: 2s, 4s, 8s, 16s, 32s
                },
                "removeOnComplete": 3600,  # Keep completed jobs for 1 hour (in count)
                "removeOnFail": 86400,  # Keep failed jobs for 24 hours (in count)
            }
            
            # Merge user opts with defaults (user opts take precedence)
            final_opts = {**default_opts, **(opts or {})}
            
            logger.debug(
                f"Adding job '{job_name}' to queue '{queue_name}' "
                f"with retry: attempts={final_opts['attempts']}, "
                f"backoff={final_opts['backoff']['type']}"
            )
            
            job = await queue.add(job_name, data, final_opts)
            
            logger.info(f"Job '{job_name}' added to queue '{queue_name}' with ID: {job.id}")
            return job.id

        except Exception as e:
            logger.error(f"Failed to add job to queue '{queue_name}'", exc_info=True)
            raise e

    async def create_worker(
        self,
        queue_name: str,
        processor: Callable[[Any, str], Any],
        connection_config: Optional[Dict[str, Any]] = None
    ) -> Worker:
        """
        Create a BullMQ Worker instance for processing jobs with automatic retry.

        Configures workers with default retry settings:
        - Max 5 retry attempts (6 total tries including initial attempt)
        - Exponential backoff starting at 2 seconds
        - Automatic retry on job failures
        - Configurable lock duration via WORKER_LOCK_DURATION_MS env var

        Args:
            queue_name: Name of the queue to process jobs from
            processor: Async function to process jobs (receives job and token)
            connection_config: Optional connection configuration (defaults to Redis URL)

        Returns:
            BullMQ Worker instance with retry configuration

        Raises:
            Exception: If worker creation fails
        """
        try:
            # Use provided connection config or default to Redis URL
            connection = connection_config or {"connection": self._get_redis_url()}
            
            # Get configurable lock duration from environment or use default
            # Default: 2 minutes for standard workers
            # Can be overridden via WORKER_LOCK_DURATION_MS for long-running workers
            import os
            lock_duration_ms = int(os.environ.get("WORKER_LOCK_DURATION_MS", "120000"))
            
            # Get configurable concurrency from environment or use default
            # Default: 2 concurrent jobs per worker instance
            # Should match deployment replica count * concurrency = total concurrent jobs
            worker_concurrency = int(os.environ.get("WORKER_CONCURRENCY", "2"))
            
            # Configure worker with automatic retry settings
            # These settings mirror the TypeScript worker-backend config.ts files
            worker_opts = {
                "autorun": True,
                "concurrency": worker_concurrency,  # Configurable concurrency per worker
                "limiter": {
                    "max": 10,  # Max 10 jobs
                    "duration": 1000,  # Per 1 second (1000ms)
                },
                "settings": {
                    "maxStalledCount": 2,  # Max times a job can be stalled before failed
                    "stalledInterval": 30000,  # Check for stalled jobs every 30s
                    "lockDuration": lock_duration_ms,  # Configurable lock duration
                }
            }
            
            logger.info(
                f"Creating BullMQ Worker for queue '{queue_name}' with settings: "
                f"concurrency={worker_concurrency} (from WORKER_CONCURRENCY), "
                f"rate_limit={worker_opts['limiter']['max']}/s, "
                f"lock_duration={lock_duration_ms}ms"
            )
            
            # Merge connection and worker options
            full_config = {**connection, **worker_opts}
            worker = Worker(queue_name, processor, full_config)
            
            return worker

        except Exception as e:
            logger.error(f"Failed to create worker for queue '{queue_name}'", exc_info=True)
            raise e

    async def close_worker(self, worker: Worker) -> None:
        """
        Close a BullMQ Worker instance and clean up resources.

        Args:
            worker: The BullMQ Worker instance to close

        Raises:
            Exception: If worker closure fails
        """
        try:
            if worker and not worker.closed:
                await worker.close()
                logger.info(f"Worker closed successfully")
        except Exception as e:
            logger.error("Failed to close worker", exc_info=True)
            raise e

    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get connection information for the BullMQ backend.

        Returns:
            Dictionary containing Redis connection details
        """
        settings = get_settings()
        return {
            "backend": "bullmq",
            "redis_url": self._get_redis_url(),
            "redis_host": settings.REDIS_HOST,
            "redis_port": settings.REDIS_PORT,
        }
