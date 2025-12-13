"""
Analytics Publisher for Worker Metrics.

This module provides a simple interface for workers to emit analytics events
to the dedicated analytics queue. Events are consumed by worker-analytic-collector
and forwarded to ELK for tracking and analysis.

Usage:
    from core_lib.core_lib_bullmq.analytics import AnalyticsPublisher, AnalyticsEvent

    # Initialize once per worker
    analytics = AnalyticsPublisher(worker_id="worker-thumbnail-generation")

    # Emit event on job completion
    await analytics.emit(
        event_type=AnalyticsEventType.THUMBNAIL_GENERATED,
        job_id=job.id,
        user_id=job.data.get("ownerId"),
        model_id=job.data.get("modelId"),
        status="success",
        timing={"processingMs": 3500, "queueWaitMs": 150},
        metrics={
            "renderTimeMs": 2200,
            "blenderVersion": "4.0",
            "outputFormat": "webp",
            "outputSizeBytes": 48000,
        }
    )
"""
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from .worker_backend_factory import WorkerBackendFactory

logger = logging.getLogger(__name__)

# Queue name for analytics events
ANALYTICS_QUEUE = "worker.analytics.events"


class AnalyticsEventType(str, Enum):
    """Types of analytics events that workers can emit."""
    
    THUMBNAIL_GENERATED = "thumbnail_generated"
    METADATA_TECHNICAL_COMPLETED = "metadata_technical_completed"
    METADATA_ENRICHMENT_COMPLETED = "metadata_enrichment_completed"
    MODEL_DISCOVERED = "model_discovered"
    METAMODEL_GROUPED = "metamodel_grouped"
    FILE_DOWNLOADED = "file_downloaded"
    MARKETPLACE_SYNCED = "marketplace_synced"


class AnalyticsStatus(str, Enum):
    """Job completion status."""
    
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


@dataclass
class TimingMetrics:
    """Processing time metrics."""
    
    queue_wait_ms: Optional[int] = None
    processing_ms: Optional[int] = None
    stages: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {}
        if self.queue_wait_ms is not None:
            result["queueWaitMs"] = self.queue_wait_ms
        if self.processing_ms is not None:
            result["processingMs"] = self.processing_ms
        if self.stages:
            result["stages"] = self.stages
        return result


@dataclass
class AnalyticsEvent:
    """
    Analytics event to be published to ELK.
    
    This dataclass represents the full event structure as defined in
    worker-analytics-event.yaml message contract.
    """
    
    # Required fields
    event_type: AnalyticsEventType
    worker_id: str
    job_id: str
    status: AnalyticsStatus
    
    # Context fields
    user_id: Optional[str] = None
    model_id: Optional[str] = None
    metamodel_id: Optional[str] = None
    storage_item_id: Optional[str] = None
    
    # Error fields
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    
    # Timing
    timing: Optional[TimingMetrics] = None
    
    # Worker-specific metrics
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Auto-generated
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for BullMQ job payload."""
        result = {
            "eventType": self.event_type.value,
            "workerId": self.worker_id,
            "jobId": self.job_id,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
        }
        
        # Add optional context
        if self.user_id:
            result["userId"] = self.user_id
        if self.model_id:
            result["modelId"] = self.model_id
        if self.metamodel_id:
            result["metamodelId"] = self.metamodel_id
        if self.storage_item_id:
            result["storageItemId"] = self.storage_item_id
        
        # Add error info
        if self.error_code:
            result["errorCode"] = self.error_code
        if self.error_message:
            result["errorMessage"] = self.error_message
        
        # Add timing
        if self.timing:
            result["timing"] = self.timing.to_dict()
        
        # Add worker-specific metrics
        if self.metrics:
            result["metrics"] = self.metrics
        
        return result


class AnalyticsPublisher:
    """
    Publisher for worker analytics events.
    
    Provides a simple interface for workers to emit analytics events
    to the dedicated queue for processing by worker-analytic-collector.
    """
    
    def __init__(self, worker_id: str, enabled: bool = True):
        """
        Initialize the analytics publisher.
        
        Args:
            worker_id: Identifier of the worker (e.g., "worker-thumbnail-generation")
            enabled: Whether analytics publishing is enabled
        """
        self.worker_id = worker_id
        self.enabled = enabled
        self._backend = None
        
        if enabled:
            logger.info(f"AnalyticsPublisher initialized for {worker_id}")
        else:
            logger.info(f"AnalyticsPublisher disabled for {worker_id}")
    
    async def _get_backend(self):
        """Get or create worker backend instance."""
        if self._backend is None:
            self._backend = WorkerBackendFactory.get_adapter()
        return self._backend
    
    async def emit(
        self,
        event_type: AnalyticsEventType,
        job_id: str,
        status: AnalyticsStatus = AnalyticsStatus.SUCCESS,
        user_id: Optional[str] = None,
        model_id: Optional[str] = None,
        metamodel_id: Optional[str] = None,
        storage_item_id: Optional[str] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        timing: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Emit an analytics event to the queue.
        
        Args:
            event_type: Type of analytics event
            job_id: Unique job identifier
            status: Job completion status
            user_id: User who triggered the job
            model_id: Model identifier (if applicable)
            metamodel_id: Metamodel identifier (if applicable)
            storage_item_id: Storage item identifier (for downloads)
            error_code: Error code if status is failure
            error_message: Error message if status is failure
            timing: Timing metrics dict with keys: queueWaitMs, processingMs, stages
            metrics: Worker-specific metrics
            
        Returns:
            True if event was emitted, False if disabled or failed
        """
        if not self.enabled:
            return False
        
        try:
            # Build timing metrics
            timing_obj = None
            if timing:
                timing_obj = TimingMetrics(
                    queue_wait_ms=timing.get("queueWaitMs"),
                    processing_ms=timing.get("processingMs"),
                    stages=timing.get("stages", {}),
                )
            
            # Create event
            event = AnalyticsEvent(
                event_type=event_type,
                worker_id=self.worker_id,
                job_id=job_id,
                status=status,
                user_id=user_id,
                model_id=model_id,
                metamodel_id=metamodel_id,
                storage_item_id=storage_item_id,
                error_code=error_code,
                error_message=error_message,
                timing=timing_obj,
                metrics=metrics or {},
            )
            
            # Publish to queue
            backend = await self._get_backend()
            await backend.add_job(
                queue_name=ANALYTICS_QUEUE,
                job_name="analytics-event",
                data=event.to_dict(),
                opts={
                    "removeOnComplete": True,  # Don't keep completed analytics jobs
                    "removeOnFail": 100,  # Keep last 100 failed for debugging
                    "attempts": 3,
                    "backoff": {"type": "exponential", "delay": 1000},
                },
            )
            
            logger.debug(
                f"Analytics event emitted: {event_type.value} for job {job_id}"
            )
            return True
            
        except Exception as e:
            # Analytics should never break the main worker flow
            logger.warning(f"Failed to emit analytics event: {e}")
            return False
    
    async def emit_success(
        self,
        event_type: AnalyticsEventType,
        job_id: str,
        user_id: Optional[str] = None,
        model_id: Optional[str] = None,
        processing_ms: Optional[int] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> bool:
        """
        Convenience method to emit a success event.
        
        Args:
            event_type: Type of analytics event
            job_id: Unique job identifier
            user_id: User who triggered the job
            model_id: Model identifier
            processing_ms: Total processing time in milliseconds
            metrics: Worker-specific metrics
            **kwargs: Additional fields (metamodel_id, storage_item_id, etc.)
            
        Returns:
            True if event was emitted
        """
        timing = None
        if processing_ms is not None:
            timing = {"processingMs": processing_ms}
        
        return await self.emit(
            event_type=event_type,
            job_id=job_id,
            status=AnalyticsStatus.SUCCESS,
            user_id=user_id,
            model_id=model_id,
            timing=timing,
            metrics=metrics,
            **kwargs,
        )
    
    async def emit_failure(
        self,
        event_type: AnalyticsEventType,
        job_id: str,
        error_code: str,
        error_message: str,
        user_id: Optional[str] = None,
        model_id: Optional[str] = None,
        processing_ms: Optional[int] = None,
        **kwargs,
    ) -> bool:
        """
        Convenience method to emit a failure event.
        
        Args:
            event_type: Type of analytics event
            job_id: Unique job identifier
            error_code: Error code
            error_message: Error message
            user_id: User who triggered the job
            model_id: Model identifier
            processing_ms: Processing time before failure
            **kwargs: Additional fields
            
        Returns:
            True if event was emitted
        """
        timing = None
        if processing_ms is not None:
            timing = {"processingMs": processing_ms}
        
        return await self.emit(
            event_type=event_type,
            job_id=job_id,
            status=AnalyticsStatus.FAILURE,
            user_id=user_id,
            model_id=model_id,
            error_code=error_code,
            error_message=error_message,
            timing=timing,
            **kwargs,
        )


# =============================================================================
# Worker-Specific Metric Builders
# =============================================================================

def build_thumbnail_metrics(
    render_time_ms: int,
    blender_version: str,
    output_format: str = "webp",
    output_size_bytes: Optional[int] = None,
    resolution: str = "512x512",
    view_angles: int = 4,
) -> Dict[str, Any]:
    """Build metrics for thumbnail generation events."""
    return {
        "renderTimeMs": render_time_ms,
        "blenderVersion": blender_version,
        "outputFormat": output_format,
        "outputSizeBytes": output_size_bytes,
        "resolution": resolution,
        "viewAngles": view_angles,
    }


def build_metadata_technical_metrics(
    blender_time_ms: int,
    file_format: str,
    vertex_count: int,
    face_count: int,
    file_size_bytes: int,
    has_textures: bool = False,
    is_manifold: Optional[bool] = None,
) -> Dict[str, Any]:
    """Build metrics for technical metadata events."""
    return {
        "blenderTimeMs": blender_time_ms,
        "fileFormat": file_format,
        "vertexCount": vertex_count,
        "faceCount": face_count,
        "fileSizeBytes": file_size_bytes,
        "hasTextures": has_textures,
        "isManifold": is_manifold,
    }


def build_metadata_enrichment_metrics(
    llm_provider: str,
    llm_model: str,
    tokens_input: int,
    tokens_output: int,
    llm_time_ms: int,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    confidence: Optional[float] = None,
    tags_generated: int = 0,
) -> Dict[str, Any]:
    """Build metrics for metadata enrichment events."""
    return {
        "llmProvider": llm_provider,
        "llmModel": llm_model,
        "tokensInput": tokens_input,
        "tokensOutput": tokens_output,
        "llmTimeMs": llm_time_ms,
        "category": category,
        "subcategory": subcategory,
        "confidence": confidence,
        "tagsGenerated": tags_generated,
    }


def build_download_metrics(
    source_type: str,
    file_hash: str,
    file_size_bytes: int,
    download_time_ms: int,
    transfer_rate_mbps: Optional[float] = None,
    was_resumed: bool = False,
) -> Dict[str, Any]:
    """Build metrics for file download events."""
    return {
        "sourceType": source_type,
        "fileHash": file_hash,
        "fileSizeBytes": file_size_bytes,
        "downloadTimeMs": download_time_ms,
        "transferRateMbps": transfer_rate_mbps,
        "wasResumed": was_resumed,
    }


def build_discovery_metrics(
    source_type: str,
    files_found: int,
    models_identified: int,
    scan_time_ms: int,
    folder_depth: int = 0,
) -> Dict[str, Any]:
    """Build metrics for model discovery events."""
    return {
        "sourceType": source_type,
        "filesFound": files_found,
        "modelsIdentified": models_identified,
        "scanTimeMs": scan_time_ms,
        "folderDepth": folder_depth,
    }


def build_metamodel_metrics(
    models_grouped: int,
    heuristic_used: str,
    confidence: float,
    processing_time_ms: int,
) -> Dict[str, Any]:
    """Build metrics for metamodel grouping events."""
    return {
        "modelsGrouped": models_grouped,
        "heuristicUsed": heuristic_used,
        "confidence": confidence,
        "processingTimeMs": processing_time_ms,
    }


def build_marketplace_metrics(
    marketplace: str,
    action: str,  # publish, update, unpublish
    listing_id: Optional[str] = None,
    api_calls_used: int = 1,
    sync_time_ms: int = 0,
) -> Dict[str, Any]:
    """Build metrics for marketplace sync events."""
    return {
        "marketplace": marketplace,
        "action": action,
        "listingId": listing_id,
        "apiCallsUsed": api_calls_used,
        "syncTimeMs": sync_time_ms,
    }
