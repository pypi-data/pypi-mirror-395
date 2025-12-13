# worker-core-lib/src/core_lib/core_lib_bullmq/queue_manager.py
import logging
from typing import Optional
from bullmq import Queue
from redis.asyncio import Redis
from ..core_lib_config.settings import get_settings
from .worker_backend_factory import WorkerBackendFactory
from .worker_backend_port import WorkerBackendPort

logger = logging.getLogger(__name__)


class QueueManager:
    """
    A centralized factory for creating and CACHING BullMQ and Redis components.
    This ensures that a single, persistent Queue instance is used for each queue name,
    preventing connection context loss bugs in the bullmq library.
    
    This class now also supports the adapter pattern through WorkerBackendFactory,
    allowing seamless switching between BullMQ and external worker backend services.
    """

    _redis_url: str | None = None
    _redis_client: Redis | None = None
    _queue_cache: dict[str, Queue] = {}  # Caching mechanism for Queue instances
    _adapter: Optional[WorkerBackendPort] = None

    @classmethod
    def get_adapter(cls) -> WorkerBackendPort:
        """
        Get the worker backend adapter instance.
        
        Returns:
            WorkerBackendPort implementation (BullMQ or External)
        """
        if cls._adapter is None:
            cls._adapter = WorkerBackendFactory.get_adapter()
        return cls._adapter

    @classmethod
    def get_redis_url(cls) -> str:
        if cls._redis_url is None:
            settings = get_settings()
            cls._redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
            logger.info(f"Initialized Redis URL for QueueManager: {cls._redis_url}")
        return cls._redis_url

    @classmethod
    def get_redis_client(cls) -> Redis:
        if cls._redis_client is None:
            redis_url = cls.get_redis_url()
            logger.info(f"Creating new singleton Redis client for URL: {redis_url}")
            cls._redis_client = Redis.from_url(redis_url, decode_responses=False)
        return cls._redis_client

    @classmethod
    def get_queue(cls, name: str) -> Queue:
        """
        Gets a BullMQ `Queue` instance. If an instance for the given name
        already exists in the cache, it's returned. Otherwise, a new one
        is created, cached, and returned.
        """
        if name not in cls._queue_cache:
            logger.info(f"Creating and caching new BullMQ Queue instance for '{name}'")
            redis_client = cls.get_redis_client()
            cls._queue_cache[name] = Queue(name, {"connection": redis_client})
        
        return cls._queue_cache[name]
        
    @classmethod
    async def safe_add_job(cls, queue_name: str, job_name: str, data: dict, opts: dict = {}):
        """
        The new, robust add_job method. It fetches the persistent, cached Queue
        instance and uses its standard `.add()` method. This is efficient and
        avoids the library's context-loss bug.
        
        This method now uses the adapter pattern and delegates to the configured
        worker backend adapter (BullMQ or External).
        """
        try:
            # Use the adapter pattern to add the job
            adapter = cls.get_adapter()
            job_id = await adapter.add_job(queue_name, job_name, data, opts)
            
            logger.info(f"Job '{job_name}' added to queue '{queue_name}' with ID: {job_id}")
            return job_id

        except Exception as e:
            logger.error(f"Failed to add job to queue '{queue_name}'", exc_info=True)
            raise e