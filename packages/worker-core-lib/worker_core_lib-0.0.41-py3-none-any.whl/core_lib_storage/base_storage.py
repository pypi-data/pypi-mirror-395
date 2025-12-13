from abc import ABC, abstractmethod
from pathlib import Path

class BaseStorage(ABC):
    """
    An abstract base class for storage providers.
    """

    @abstractmethod
    async def download(self, uri: str, destination: Path) -> None:
        """
        Downloads a file from a given URI to a local destination.
        """
        raise NotImplementedError

    @abstractmethod
    async def upload(self, source: Path, uri: str) -> None:
        """
        Uploads a local file to a given URI.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_presigned_url(self, uri: str) -> str:
        """
        Gets a presigned URL for a file at a given URI.
        """
        raise NotImplementedError