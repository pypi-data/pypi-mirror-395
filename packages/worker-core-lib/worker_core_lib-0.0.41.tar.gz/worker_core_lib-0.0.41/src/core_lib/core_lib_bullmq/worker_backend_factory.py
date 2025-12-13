"""
Factory for creating worker backend adapter instances.

This module provides a centralized factory for instantiating the appropriate
worker backend adapter based on configuration.
"""
import logging
import os
from typing import Optional

from .worker_backend_port import WorkerBackendPort
from .bullmq_adapter import BullMQAdapter
from .external_worker_adapter import ExternalWorkerBackendAdapter

logger = logging.getLogger(__name__)


class WorkerBackendFactory:
    """
    Factory for creating worker backend adapter instances.
    
    This factory determines which adapter to use based on environment
    configuration and provides a singleton instance for the application.
    """

    _instance: Optional[WorkerBackendPort] = None
    _adapter_type: Optional[str] = None

    @classmethod
    def create_adapter(
        cls,
        adapter_type: Optional[str] = None,
        **kwargs
    ) -> WorkerBackendPort:
        """
        Create a worker backend adapter instance.
        
        Args:
            adapter_type: Type of adapter to create ('bullmq' or 'external').
                         If None, determined from WORKER_BACKEND_TYPE env var.
            **kwargs: Additional configuration for the adapter
                     (e.g., backend_url, api_key for external adapter)
        
        Returns:
            WorkerBackendPort implementation instance
            
        Raises:
            ValueError: If adapter_type is invalid
        """
        # Determine adapter type from parameter or environment
        if adapter_type is None:
            adapter_type = os.getenv("WORKER_BACKEND_TYPE", "bullmq").lower()
        
        logger.info(f"Creating worker backend adapter: {adapter_type}")
        
        if adapter_type == "bullmq":
            return BullMQAdapter()
        elif adapter_type == "external":
            backend_url = kwargs.get("backend_url") or os.getenv("WORKER_BACKEND_URL")
            api_key = kwargs.get("api_key") or os.getenv("WORKER_BACKEND_API_KEY")
            
            if not backend_url:
                logger.warning(
                    "WORKER_BACKEND_URL not set. External adapter may not function correctly."
                )
            
            return ExternalWorkerBackendAdapter(
                backend_url=backend_url,
                api_key=api_key
            )
        else:
            raise ValueError(
                f"Unknown adapter type: {adapter_type}. "
                "Supported types are 'bullmq' and 'external'."
            )

    @classmethod
    def get_adapter(cls, force_recreate: bool = False) -> WorkerBackendPort:
        """
        Get the singleton worker backend adapter instance.
        
        This method creates and caches a single adapter instance for the
        entire application, ensuring consistent behavior across all components.
        
        Args:
            force_recreate: If True, recreates the adapter even if one exists
        
        Returns:
            WorkerBackendPort implementation instance
        """
        current_type = os.getenv("WORKER_BACKEND_TYPE", "bullmq").lower()
        
        # Recreate if forced, type changed, or instance doesn't exist
        if force_recreate or cls._adapter_type != current_type or cls._instance is None:
            logger.info(f"Creating new adapter instance (type: {current_type})")
            cls._instance = cls.create_adapter(adapter_type=current_type)
            cls._adapter_type = current_type
        
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """
        Reset the factory singleton instance.
        
        This is primarily useful for testing purposes to ensure a clean state.
        """
        logger.debug("Resetting WorkerBackendFactory singleton")
        cls._instance = None
        cls._adapter_type = None
