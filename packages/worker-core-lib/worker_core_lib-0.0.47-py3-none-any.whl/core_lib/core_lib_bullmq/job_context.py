import logging
from typing import Any, Dict, Optional, List
from ..core_lib_utils.hooks import WorkerHooks

logger = logging.getLogger(__name__)

class JobContext:
    """
    Provides a standardized interface for interacting with a job and its
    lifecycle, including reporting progress, success, and failure.
    
    This class now supports BullMQ-like patterns for creating child jobs,
    job dependencies, and job flows.
    """

    def __init__(
        self,
        job: Any,
        result_queue: Any,
        hooks: Optional[WorkerHooks] = None,
        queue_manager: Optional[Any] = None,
    ):
        """
        Initializes the JobContext.

        Args:
            job: The BullMQ job instance.
            result_queue: The BullMQ queue instance for reporting results.
            hooks: An optional WorkerHooks instance for lifecycle callbacks.
            queue_manager: Optional QueueManager instance for creating child jobs.
        """
        self.job = job
        self.result_queue = result_queue
        self.hooks = hooks
        self._queue_manager = queue_manager
        self._child_jobs: List[str] = []  # Track child job IDs
        logger.debug(f"[Job {self.job.id}] JobContext initialized.")


    async def report_progress(self, progress: int, message: str = "") -> None:
        """
        Reports the progress of a job.

        Args:
            progress: The progress percentage (0-100).
            message: An optional message to include with the progress.
        """
        logger.info(f"[Job {self.job.id}] Progress: {progress}%. Message: {message}")
        # In a real implementation, this would call job.updateProgress()
        # This functionality is part of bullmq-pro, but we can log it.

    async def report_success(self, result_data: Dict[str, Any]) -> None:
        """
        Reports a job as successful by sending data to the result queue.

        Args:
            result_data: A dictionary containing the job's results.
        """
        logger.info(f"[Job {self.job.id}] Reporting success to queue '{self.result_queue.name}'.")
        logger.debug(f"[Job {self.job.id}] Success data: {result_data}")
        if self.hooks:
            await self.hooks.before_message_sent(
                self.job, self.result_queue.name, result_data
            )
        # In a real implementation, this would add a job to the result_queue
        # This logic should be handled by the worker's return value.
        # This method is for logging and hook purposes.

    async def report_failure(self, error: Exception) -> None:
        """
        Reports a job as failed. This is primarily for logging and hooks,
        as the actual failure is signaled by raising an exception.

        Args:
            error: The exception that caused the failure.
        """
        logger.error(f"[Job {self.job.id}] Reporting failure: {error}", exc_info=True)
        failure_data = {"error": str(error)}
        if self.hooks:
            await self.hooks.before_message_sent(
                self.job, self.result_queue.name, failure_data
            )

    async def add_child_job(
        self, 
        queue_name: str, 
        job_name: str, 
        data: Dict[str, Any],
        opts: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a child job to a queue. Child jobs are tracked and can be used
        to create job dependencies similar to BullMQ's flow pattern.
        
        This mimics BullMQ's behavior where child jobs can be created
        and the parent job can wait for their completion.

        Args:
            queue_name: Name of the queue to add the child job to
            job_name: Name/type of the child job
            data: Child job data/payload
            opts: Optional job options (priority, delay, parent job reference, etc.)

        Returns:
            Child job ID as a string

        Raises:
            RuntimeError: If QueueManager is not available
            Exception: If child job creation fails
        """
        if self._queue_manager is None:
            raise RuntimeError(
                "QueueManager not available in JobContext. "
                "Pass queue_manager parameter when creating JobContext."
            )
        
        try:
            # Add parent job reference to options for dependency tracking
            child_opts = opts or {}
            if not child_opts.get('parent'):
                child_opts['parent'] = {
                    'id': self.job.id,
                    'queue': getattr(self.job, 'queueName', 'unknown')
                }
            
            # Use QueueManager to add the child job
            child_job_id = await self._queue_manager.safe_add_job(
                queue_name, job_name, data, child_opts
            )
            
            # Track the child job
            self._child_jobs.append(child_job_id)
            
            logger.info(
                f"[Job {self.job.id}] Created child job {child_job_id} "
                f"in queue '{queue_name}'"
            )
            
            return child_job_id
            
        except Exception as e:
            logger.error(
                f"[Job {self.job.id}] Failed to create child job in queue '{queue_name}'",
                exc_info=True
            )
            raise e

    async def add_bulk_child_jobs(
        self,
        jobs: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Add multiple child jobs in bulk. This is useful for creating
        multiple related jobs efficiently.
        
        Mimics BullMQ's bulk add functionality for child jobs.

        Args:
            jobs: List of job definitions, each containing:
                - queue_name: Queue to add job to
                - job_name: Type/name of job
                - data: Job payload
                - opts: Optional job options

        Returns:
            List of child job IDs

        Raises:
            RuntimeError: If QueueManager is not available
            Exception: If bulk job creation fails
        """
        child_ids = []
        
        for job_def in jobs:
            queue_name = job_def.get('queue_name')
            job_name = job_def.get('job_name')
            data = job_def.get('data', {})
            opts = job_def.get('opts', {})
            
            if not queue_name or not job_name:
                logger.warning(
                    f"[Job {self.job.id}] Skipping invalid job definition: {job_def}"
                )
                continue
            
            child_id = await self.add_child_job(queue_name, job_name, data, opts)
            child_ids.append(child_id)
        
        logger.info(
            f"[Job {self.job.id}] Created {len(child_ids)} child jobs in bulk"
        )
        
        return child_ids

    def get_child_jobs(self) -> List[str]:
        """
        Get the list of child job IDs created by this job.
        
        This can be used to track job dependencies and flows,
        similar to BullMQ's getChildrenValues() method.

        Returns:
            List of child job IDs
        """
        return self._child_jobs.copy()

    async def move_to_waiting_children(self) -> None:
        """
        Signal that this job is waiting for child jobs to complete.
        
        This mimics BullMQ's moveToWaitingChildren behavior, where a job
        can wait for its children before completing.
        
        Note: Actual implementation depends on the backend adapter being used.
        With BullMQ, this would use job.moveToWaitingChildren().
        With external backend, this is handled server-side.
        """
        if hasattr(self.job, 'moveToWaitingChildren'):
            # BullMQ implementation
            await self.job.moveToWaitingChildren(self._child_jobs)
            logger.info(
                f"[Job {self.job.id}] Moved to waiting for {len(self._child_jobs)} children"
            )
        else:
            # For external backend or mock implementations
            logger.info(
                f"[Job {self.job.id}] Would wait for {len(self._child_jobs)} children "
                "(moveToWaitingChildren not available in current backend)"
            )