"""
External Worker Backend adapter implementation.

This adapter provides integration with an external worker backend service,
using the mesh-sync-worker-backend-client package (worker_client module).
"""
import logging
from typing import Any, Dict, Optional, Callable
import requests

from .worker_backend_port import WorkerBackendPort

logger = logging.getLogger(__name__)

# Import the worker_client from mesh-sync-worker-backend-client
try:
    from worker_client import WorkerClient
    WORKER_CLIENT_AVAILABLE = True
except ImportError:
    WORKER_CLIENT_AVAILABLE = False
    logger.warning(
        "worker_client module not available. "
        "Install mesh-sync-worker-backend-client package to use ExternalWorkerBackendAdapter."
    )


class ExternalWorkerBackendAdapter(WorkerBackendPort):
    """
    External worker backend service implementation of the WorkerBackendPort interface.
    
    This adapter integrates with a dedicated external worker backend service using
    the mesh-sync-worker-backend-client package (worker_client module).
    
    Note:
        This adapter requires the mesh-sync-worker-backend-client package to be installed.
        Install via: pip install mesh-sync-worker-backend-client
    """

    def __init__(self, backend_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the external worker backend adapter.
        
        Args:
            backend_url: URL of the external worker backend service
            api_key: Optional API key for authentication
            
        Raises:
            ImportError: If worker_client module is not available
        """
        if not WORKER_CLIENT_AVAILABLE:
            raise ImportError(
                "worker_client module not found. "
                "Please install: pip install mesh-sync-worker-backend-client"
            )
        
        self.backend_url = backend_url
        self.api_key = api_key
        logger.info(f"ExternalWorkerBackendAdapter initialized with backend: {backend_url}")
        
        # Initialize the WorkerClient from mesh-sync-worker-backend-client
        self._client = WorkerClient(backend_url, api_key=api_key) if backend_url else None
        self._worker_instances: Dict[str, Any] = {}

    async def add_job(
        self, 
        queue_name: str, 
        job_name: str, 
        data: Dict[str, Any], 
        opts: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a job to the external worker backend service.

        Args:
            queue_name: Name of the queue to add the job to
            job_name: Name/type of the job (message type)
            data: Job data/payload
            opts: Optional job options (priority, delay, parent, children, etc.)
                  Note: Children dependencies are passed in the payload for external backend

        Returns:
            Job ID as a string

        Raises:
            RuntimeError: If client is not initialized
            requests.HTTPError: If the HTTP request to the backend fails
            requests.ConnectionError: If connection to the backend fails
            requests.Timeout: If the request times out
            ValueError: If the response is invalid
        """
        if self._client is None:
            raise RuntimeError(
                "WorkerClient not initialized. Provide backend_url when creating adapter."
            )
        
        try:
            logger.info(f"Adding job '{job_name}' to external queue '{queue_name}'")
            
            # Merge opts into data payload for external backend
            # This includes child dependencies if present in opts
            payload = data.copy()
            if opts:
                # Add job options to payload, especially 'children' for FlowBuilder support
                if 'children' in opts:
                    payload['_children'] = opts['children']
                    logger.debug(f"Job '{job_name}' has {len(opts['children'])} child dependencies")
                
                # Include other options that the external backend might support
                for key in ['priority', 'delay', 'attempts', 'backoff', 'parent']:
                    if key in opts:
                        payload[f'_{key}'] = opts[key]
            
            # Use the WorkerClient to send job to the queue
            # The send_to_queue method takes message_type and payload
            response = self._client.send_to_queue(job_name, payload)
            
            if not response.success:
                raise RuntimeError(f"Failed to add job: {response}")
            
            logger.info(f"Job '{job_name}' added with ID: {response.job_id}")
            return response.job_id

        except requests.HTTPError as e:
            logger.error(
                f"HTTP error adding job to external queue '{queue_name}': {e.response.status_code}",
                exc_info=True
            )
            raise
        except requests.ConnectionError as e:
            logger.error(
                f"Connection error to external backend at '{self.backend_url}': {e}",
                exc_info=True
            )
            raise
        except requests.Timeout as e:
            logger.error(
                f"Timeout connecting to external backend at '{self.backend_url}': {e}",
                exc_info=True
            )
            raise
        except (RuntimeError, ValueError) as e:
            # These are already logged, just re-raise
            logger.error(f"Failed to add job to external queue '{queue_name}': {e}", exc_info=True)
            raise
        except Exception as e:
            # Catch-all for unexpected errors
            logger.error(
                f"Unexpected error adding job to external queue '{queue_name}'",
                exc_info=True
            )
            raise RuntimeError(f"Unexpected error adding job: {e}") from e

    async def create_worker(
        self,
        queue_name: str,
        processor: Callable[[Any, str], Any],
        connection_config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Create a worker instance for the external backend service.
        
        Note: The external worker backend manages workers server-side.
        This method returns a mock worker object for compatibility with
        the BaseWorker interface.

        Args:
            queue_name: Name of the queue to process jobs from
            processor: Async function to process jobs (receives job and token)
            connection_config: Optional connection configuration

        Returns:
            Mock worker instance for compatibility

        Raises:
            RuntimeError: If client is not initialized
        """
        if self._client is None:
            raise RuntimeError(
                "WorkerClient not initialized. Provide backend_url when creating adapter."
            )
        
        logger.info(f"Creating worker for external queue: {queue_name}")
        logger.info(
            "Note: External worker backend manages workers server-side. "
            "Returning mock worker for compatibility."
        )
        
        # Create a mock worker object for compatibility
        # The external backend manages workers server-side
        class MockWorker:
            def __init__(self, queue_name, processor):
                self.queue_name = queue_name
                self.processor = processor
                self.closed = False
            
            async def run(self):
                logger.warning(
                    f"Mock worker for '{self.queue_name}' cannot run. "
                    "External backend manages workers server-side."
                )
            
            async def close(self):
                self.closed = True
        
        worker = MockWorker(queue_name, processor)
        self._worker_instances[queue_name] = worker
        
        return worker

    async def close_worker(self, worker: Any) -> None:
        """
        Close a worker instance from the external backend.

        Args:
            worker: The worker instance to close

        Raises:
            Exception: If worker closure fails
        """
        try:
            if hasattr(worker, 'closed') and not worker.closed:
                await worker.close()
                logger.info(f"Worker closed successfully")
        except Exception as e:
            logger.error("Failed to close external worker", exc_info=True)
            raise e

    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get connection information for the external backend.

        Returns:
            Dictionary containing backend connection details
        """
        return {
            "backend": "external",
            "backend_url": self.backend_url,
            "authenticated": self.api_key is not None,
        }
