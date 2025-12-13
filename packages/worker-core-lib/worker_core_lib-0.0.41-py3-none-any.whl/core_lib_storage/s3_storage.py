from pathlib import Path
from .base_storage import BaseStorage
from ..core_lib_auth.credentials_service import Credential

class S3Storage(BaseStorage):
    """
    A mock S3 storage provider.
    """

    def __init__(self, credentials: Credential):
        """
        Initializes the S3Storage provider.
        """
        print(
            f"Initializing S3 storage with access key: {credentials.access_key}"
        )
        self.credentials = credentials

    async def download(self, uri: str, destination: Path) -> None:
        """
        Downloads a file from S3.
        """
        print(f"Downloading {uri} from S3 to {destination}...")
        (destination / Path(uri).name).touch()

    async def upload(self, source: Path, uri: str) -> None:
        """
        Uploads a file to S3.
        """
        print(f"Uploading {source} to S3 at {uri}...")

    async def get_presigned_url(self, uri: str) -> str:
        """
        Gets a presigned URL for a file in S3.
        """
        print(f"Generating presigned URL for {uri}...")
        return f"https://s3.amazonaws.com/{uri}?presigned=true"