"""
Enriched metrics publisher for detailed worker monitoring.

Publishes comprehensive metrics to backend.logging.events queue including:
- Resource usage (CPU, memory, disk, network)
- LLM token usage and costs
- Detailed timing breakdowns
- User and context attribution
"""
import logging
import os
import socket
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from ..core_lib_bullmq.worker_backend_factory import WorkerBackendFactory

logger = logging.getLogger(__name__)

ENRICHED_METRICS_QUEUE = "backend.logging.events"


@dataclass
class EnrichedMetricsEvent:
    """Enriched metrics event for detailed monitoring."""
    
    # Required fields
    event_type: str = "worker_metrics_enriched"
    worker_id: str = ""
    job_id: str = ""
    status: str = "success"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    # User & context
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    model_id: Optional[str] = None
    metamodel_id: Optional[str] = None
    storage_item_id: Optional[str] = None
    
    # Timing
    timing: Optional[Dict] = None
    
    # LLM usage
    llm_usage: Optional[Dict] = None
    
    # Resources
    resources: Optional[Dict] = None
    
    # Worker-specific
    worker_metrics: Optional[Dict] = None
    
    # Error info
    error: Optional[Dict] = None
    
    # Environment
    environment: Optional[str] = None
    region: Optional[str] = None
    worker_version: Optional[str] = None
    hostname: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for publishing."""
        result = {
            "eventType": self.event_type,
            "workerId": self.worker_id,
            "jobId": self.job_id,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
        }
        
        # Add optional fields if present
        optional_fields = {
            "user_id": "userId",
            "tenant_id": "tenantId",
            "session_id": "sessionId",
            "request_id": "requestId",
            "model_id": "modelId",
            "metamodel_id": "metamodelId",
            "storage_item_id": "storageItemId",
            "timing": "timing",
            "llm_usage": "llmUsage",
            "resources": "resources",
            "worker_metrics": "workerMetrics",
            "error": "error",
            "environment": "environment",
            "region": "region",
            "worker_version": "workerVersion",
            "hostname": "hostname",
        }
        
        for field_name, json_key in optional_fields.items():
            value = getattr(self, field_name, None)
            if value is not None:
                result[json_key] = value
        
        return result


class EnrichedMetricsPublisher:
    """
    Publisher for enriched worker metrics.
    
    Usage:
        publisher = EnrichedMetricsPublisher(worker_id="worker-thumbnail-generation")
        
        # During job processing
        await publisher.publish(
            job_id=job.id,
            status="success",
            user_id=job.data.get("ownerId"),
            timing={...},
            resources={...},
            worker_metrics={...}
        )
    """
    
    def __init__(self, worker_id: str, enabled: bool = True):
        """
        Initialize enriched metrics publisher.
        
        Args:
            worker_id: Worker identifier (e.g., "worker-thumbnail-generation")
            enabled: Whether publishing is enabled (default from env)
        """
        self.worker_id = worker_id
        self.enabled = enabled and os.getenv("ENABLE_ENRICHED_METRICS", "true").lower() == "true"
        self._backend = None
        
        # Cache environment info
        self._environment = os.getenv("ENVIRONMENT", "development")
        self._region = os.getenv("REGION", os.getenv("AWS_REGION", "unknown"))
        self._worker_version = os.getenv("WORKER_VERSION", "unknown")
        try:
            self._hostname = socket.gethostname()
        except Exception:
            self._hostname = "unknown"
        
        if self.enabled:
            logger.info(f"EnrichedMetricsPublisher enabled for {worker_id}")
        else:
            logger.info(f"EnrichedMetricsPublisher disabled for {worker_id}")
    
    async def _get_backend(self):
        """Get or create worker backend instance."""
        if self._backend is None:
            self._backend = WorkerBackendFactory.get_adapter()
        return self._backend
    
    async def publish(
        self,
        job_id: str,
        status: str = "success",
        user_id: Optional[str] = None,
        model_id: Optional[str] = None,
        metamodel_id: Optional[str] = None,
        timing: Optional[Dict] = None,
        llm_usage: Optional[Dict] = None,
        resources: Optional[Dict] = None,
        worker_metrics: Optional[Dict] = None,
        error: Optional[Dict] = None,
        **kwargs
    ) -> bool:
        """
        Publish enriched metrics event.
        
        Args:
            job_id: Job identifier
            status: Job status (success, failure, partial)
            user_id: User who triggered the job
            model_id: Model being processed
            metamodel_id: Metamodel being processed
            timing: Timing metrics dictionary
            llm_usage: LLM usage metrics dictionary
            resources: Resource usage dictionary (from ResourceMetricsCollector)
            worker_metrics: Worker-specific metrics
            error: Error information if failed
            **kwargs: Additional context fields (tenant_id, session_id, etc.)
        
        Returns:
            True if published successfully, False otherwise
        """
        if not self.enabled:
            logger.debug(f"Enriched metrics disabled, skipping publish for job {job_id}")
            return False
        
        try:
            event = EnrichedMetricsEvent(
                worker_id=self.worker_id,
                job_id=job_id,
                status=status,
                user_id=user_id,
                model_id=model_id,
                metamodel_id=metamodel_id,
                timing=timing,
                llm_usage=llm_usage,
                resources=resources,
                worker_metrics=worker_metrics,
                error=error,
                environment=self._environment,
                region=self._region,
                worker_version=self._worker_version,
                hostname=self._hostname,
                **{k: v for k, v in kwargs.items() if k in [
                    "tenant_id", "session_id", "request_id", "storage_item_id"
                ]}
            )
            
            backend = await self._get_backend()
            
            # Publish to backend.logging.events queue
            await backend.publish_message(
                queue=ENRICHED_METRICS_QUEUE,
                message=event.to_dict()
            )
            
            logger.info(
                f"Published enriched metrics for job {job_id}: "
                f"status={status}, user={user_id}, "
                f"llm_cost={llm_usage.get('totalCostUsd', 0) if llm_usage else 0:.4f}USD"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish enriched metrics for job {job_id}: {e}", exc_info=True)
            return False
    
    async def publish_error(
        self,
        job_id: str,
        error: Exception,
        user_id: Optional[str] = None,
        model_id: Optional[str] = None,
        timing: Optional[Dict] = None,
        resources: Optional[Dict] = None,
        **kwargs
    ) -> bool:
        """
        Convenience method to publish error metrics.
        
        Args:
            job_id: Job identifier
            error: Exception that occurred
            user_id: User who triggered the job
            model_id: Model being processed
            timing: Timing metrics
            resources: Resource metrics
            **kwargs: Additional context
        
        Returns:
            True if published successfully
        """
        error_dict = {
            "code": type(error).__name__,
            "message": str(error),
            "category": self._categorize_error(error),
        }
        
        return await self.publish(
            job_id=job_id,
            status="failure",
            user_id=user_id,
            model_id=model_id,
            timing=timing,
            resources=resources,
            error=error_dict,
            **kwargs
        )
    
    def _categorize_error(self, error: Exception) -> str:
        """Categorize error for alerting."""
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()
        
        if "llm" in error_str or "openrouter" in error_str or "token" in error_str:
            return "llm_error"
        elif "network" in error_str or "connection" in error_str or "timeout" in error_str:
            return "network_error"
        elif "memory" in error_str or "out of memory" in error_str:
            return "resource_error"
        elif "validation" in error_str or "invalid" in error_str:
            return "validation_error"
        elif "api" in error_str or "http" in error_str:
            return "external_api_error"
        else:
            return "unknown"
