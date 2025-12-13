# worker-core-lib/src/core_lib/core_lib_bullmq/base_worker.py
import asyncio
import logging
import os
import signal
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from bullmq import Worker, WaitingChildrenError

from ..core_lib_utils.hooks import WorkerHooks
from .queue_manager import QueueManager
from .worker_backend_factory import WorkerBackendFactory

logger = logging.getLogger(__name__)


class BaseWorker(ABC):
    """
    An abstract base class for creating BullMQ workers.
    It now uses a centralized QueueManager for consistent Redis connections
    and includes improved shutdown logic and internal state management.
    
    This class supports the adapter pattern through WorkerBackendFactory,
    allowing it to work with either BullMQ or external worker backend services.
    
    Analytics Integration:
    - Automatically emits analytics events on job completion
    - Set ANALYTICS_ENABLED=false to disable
    - Override `get_analytics_metrics()` to provide custom metrics
    """

    # Worker ID for analytics (override in subclass)
    WORKER_ID: str = "unknown-worker"
    
    # Analytics event type (override in subclass)
    ANALYTICS_EVENT_TYPE: str = "unknown_event"

    def __init__(
        self,
        queue_name: str,
        hooks: Optional[WorkerHooks] = None,
    ):
        """
        Initializes the BaseWorker.
        
        Args:
            queue_name: Name of the queue to process jobs from
            hooks: Optional WorkerHooks instance for lifecycle callbacks
        """
        self.queue_name = queue_name
        self.hooks = hooks
        self.redis_connection = QueueManager.get_redis_url()
        self._worker_instance: Optional[Worker] = None
        self._shutdown_event = asyncio.Event()
        # **CRITICAL FIX**: Add internal state to prevent re-running.
        self._is_running = False
        
        self._backend_adapter = WorkerBackendFactory.get_adapter()
        
        # Initialize analytics publisher
        self._analytics_enabled = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"
        self._analytics_publisher = None
        if self._analytics_enabled:
            try:
                from .analytics import AnalyticsPublisher
                worker_id = getattr(self, 'WORKER_ID', self.__class__.__name__)
                self._analytics_publisher = AnalyticsPublisher(worker_id=worker_id)
            except ImportError:
                logger.debug("Analytics module not available, analytics disabled")
                self._analytics_enabled = False
        
        logger.info(
            f"BaseWorker for queue '{self.queue_name}' initialized with adapter: "
            f"{self._backend_adapter.__class__.__name__}, analytics={self._analytics_enabled}"
        )

    @abstractmethod
    async def process(self, job: Any, job_token: str) -> Any:
        raise NotImplementedError

    def get_analytics_metrics(self, job: Any, result: Any, processing_ms: int) -> Optional[Dict[str, Any]]:
        """
        Override this method to provide worker-specific metrics.
        
        Args:
            job: The processed job
            result: The job result
            processing_ms: Processing time in milliseconds
            
        Returns:
            Dictionary of metrics or None
        """
        return None

    async def _emit_analytics(
        self,
        job: Any,
        result: Any,
        processing_ms: int,
        error: Optional[Exception] = None,
    ):
        """Emit analytics event for job completion."""
        if not self._analytics_enabled or not self._analytics_publisher:
            return
        
        try:
            from .analytics import AnalyticsEventType, AnalyticsStatus
            
            # Map event type string to enum
            event_type_str = getattr(self, 'ANALYTICS_EVENT_TYPE', 'unknown_event')
            try:
                event_type = AnalyticsEventType(event_type_str)
            except ValueError:
                # Unknown event type, skip analytics
                return
            
            # Extract context from job data
            job_data = job.data if hasattr(job, 'data') else {}
            user_id = job_data.get("ownerId") or job_data.get("userId")
            model_id = job_data.get("modelId")
            metamodel_id = job_data.get("metamodelId")
            storage_item_id = job_data.get("storageItemId")
            
            # Get worker-specific metrics
            metrics = self.get_analytics_metrics(job, result, processing_ms)
            
            if error:
                await self._analytics_publisher.emit_failure(
                    event_type=event_type,
                    job_id=str(job.id),
                    user_id=user_id,
                    model_id=model_id,
                    error_code=error.__class__.__name__,
                    error_message=str(error)[:500],
                    processing_ms=processing_ms,
                    metamodel_id=metamodel_id,
                    storage_item_id=storage_item_id,
                )
            else:
                await self._analytics_publisher.emit_success(
                    event_type=event_type,
                    job_id=str(job.id),
                    user_id=user_id,
                    model_id=model_id,
                    processing_ms=processing_ms,
                    metrics=metrics,
                    metamodel_id=metamodel_id,
                    storage_item_id=storage_item_id,
                )
        except Exception as e:
            # Analytics should never break main flow
            logger.debug(f"Failed to emit analytics: {e}")

    async def _job_processor(self, job: Any, job_token: str) -> Any:
        if self.hooks and hasattr(self.hooks, "on_request_received"):
            await self.hooks.on_request_received(job)
        
        start_time = time.time()
        error_occurred = None
        result = None
        
        try:
            result = await self.process(job, job_token)
            if self.hooks and hasattr(self.hooks, "on_request_completed"):
                await self.hooks.on_request_completed(job, result)
            return result
        except WaitingChildrenError:
            logger.info(f"Job {job.id} is waiting for children to complete.")
            raise
        except Exception as e:
            error_occurred = e
            logger.error(f"Error processing job {job.id} in queue {self.queue_name}: {e}", exc_info=True)
            if self.hooks and hasattr(self.hooks, "on_error_occurred"):
                await self.hooks.on_error_occurred(job, e)
            raise
        finally:
            # Emit analytics (don't emit for WaitingChildrenError)
            if not isinstance(error_occurred, WaitingChildrenError):
                processing_ms = int((time.time() - start_time) * 1000)
                await self._emit_analytics(job, result, processing_ms, error_occurred)

    async def enqueue_child_job(self, parent_job_id: str, job_name: str, job_data: dict) -> Any:
        """
        Enqueues a child job, making the current job its parent.

        Args:
            parent_job_id: The ID of the parent job.
            job_name: The name of the child job to enqueue.
            job_data: The data for the child job.

        Returns:
            The newly created job object.
        """
        queue = QueueManager.get_queue(self.queue_name)
        logger.info(f"Enqueueing child job '{job_name}' for parent '{parent_job_id}' in queue '{self.queue_name}'.")
        job = await queue.add(name=job_name, data=job_data, opts={"parentId": parent_job_id})
        return job

    def _signal_handler(self):
        logger.info(f"Shutdown signal received for {self.queue_name}. Shutting down...")
        self._shutdown_event.set()

    async def run(self) -> None:
        # **CRITICAL FIX**: Prevent the run method from being entered more than once.
        if self._is_running:
            logger.warning(f"Worker for queue '{self.queue_name}' is already running. Ignoring redundant run call.")
            return
        self._is_running = True

        logger.info(f"Worker starting for queue: {self.queue_name}")

        # Create worker using adapter pattern
        logger.info(f"Creating worker via adapter: {self._backend_adapter.__class__.__name__}")
        self._worker_instance = await self._backend_adapter.create_worker(
            self.queue_name,
            self._job_processor,
            {"connection": self.redis_connection}
        )

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, self._signal_handler)
        loop.add_signal_handler(signal.SIGINT, self._signal_handler)

        try:
            worker_task = asyncio.create_task(self._worker_instance.run())
            await self._shutdown_event.wait()

            logger.info(f"Gracefully shutting down worker {self.queue_name}...")
            await self.close()
            worker_task.cancel()
            try:
                await worker_task
            except asyncio.CancelledError:
                logger.info(f"Worker task for {self.queue_name} cancelled successfully.")

        except Exception as e:
            logger.error(f"Worker for queue {self.queue_name} stopped unexpectedly: {e}", exc_info=True)
        finally:
            if self._worker_instance and not self._worker_instance.closed:
                await self._backend_adapter.close_worker(self._worker_instance)
            self._is_running = False # Reset state
            logger.info(f"Worker {self.queue_name} shutdown complete.")

    async def close(self) -> None:
        if self._worker_instance and not self._worker_instance.closed:
            await self._backend_adapter.close_worker(self._worker_instance)
            self._worker_instance = None
            self._is_running = False # Reset state
            logger.info(f"Worker {self.queue_name} connections closed.")