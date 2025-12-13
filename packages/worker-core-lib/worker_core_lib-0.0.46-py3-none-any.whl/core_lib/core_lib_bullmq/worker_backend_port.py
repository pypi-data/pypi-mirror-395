"""
Port interface for worker backend operations.

This module defines the abstract interface for queue and worker operations,
allowing different implementations (BullMQ, external services, etc.) to be
used interchangeably through the adapter pattern.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable, List


class WorkerBackendPort(ABC):
    """
    Abstract interface for worker backend operations.
    
    This port defines the contract that all worker backend adapters must implement,
    enabling easy swapping between different queue implementations (e.g., BullMQ,
    external worker services).
    """

    @abstractmethod
    async def add_job(
        self, 
        queue_name: str, 
        job_name: str, 
        data: Dict[str, Any], 
        opts: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a job to a queue.

        Args:
            queue_name: Name of the queue to add the job to
            job_name: Name/type of the job
            data: Job data/payload
            opts: Optional job options (priority, delay, parent, etc.)

        Returns:
            Job ID as a string

        Raises:
            Exception: If job addition fails
        """
        pass

    @abstractmethod
    async def create_worker(
        self,
        queue_name: str,
        processor: Callable[[Any, str], Any],
        connection_config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Create a worker instance for processing jobs from a queue.

        Args:
            queue_name: Name of the queue to process jobs from
            processor: Async function to process jobs (receives job and token)
            connection_config: Optional connection configuration

        Returns:
            Worker instance

        Raises:
            Exception: If worker creation fails
        """
        pass

    @abstractmethod
    async def close_worker(self, worker: Any) -> None:
        """
        Close a worker instance and clean up resources.

        Args:
            worker: The worker instance to close

        Raises:
            Exception: If worker closure fails
        """
        pass

    @abstractmethod
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get connection information for the backend.

        Returns:
            Dictionary containing connection details (URL, host, port, etc.)
        """
        pass

    async def add_bulk_jobs(
        self,
        queue_name: str,
        jobs: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Add multiple jobs to a queue in bulk.
        
        This is an optional method with a default implementation that
        calls add_job sequentially. Adapters can override for better performance.

        Args:
            queue_name: Name of the queue to add jobs to
            jobs: List of job definitions, each containing:
                - name: Job name/type
                - data: Job data/payload
                - opts: Optional job options

        Returns:
            List of job IDs

        Raises:
            Exception: If bulk job addition fails
        """
        job_ids = []
        for job_def in jobs:
            job_name = job_def.get('name', 'bulk-job')
            data = job_def.get('data', {})
            opts = job_def.get('opts', {})
            
            job_id = await self.add_job(queue_name, job_name, data, opts)
            job_ids.append(job_id)
        
        return job_ids

