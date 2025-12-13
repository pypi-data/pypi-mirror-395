from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class WorkerHooks(ABC):
    """
    Abstract base class for defining worker lifecycle hooks.

    This class provides a contract for implementing callbacks that can be
    injected into the BaseWorker to add custom logic (e.g., logging,
    analytics) at specific points in the job lifecycle without modifying
    the worker's core business logic.
    """

    async def on_request_received(self, job: Any) -> None:
        """
        Called when a new job is received by the worker.
        """
        pass

    async def on_error_occurred(self, job: Any, error: Exception) -> None:
        """
        Called when an exception occurs during job processing.
        """
        pass

    async def before_message_sent(
        self, job: Any, queue_name: str, message_data: Dict[str, Any]
    ) -> None:
        """
        Called before a result (success or failure) is sent to a queue.
        """
        pass