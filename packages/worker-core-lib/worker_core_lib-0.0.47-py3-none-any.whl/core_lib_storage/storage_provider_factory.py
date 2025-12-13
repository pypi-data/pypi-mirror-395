from typing import Any
from ..core_lib_auth.credentials_service import Credential
from .base_storage import BaseStorage

class StorageProviderFactory:
    """
    A factory for creating storage provider instances.
    """
    _providers = {}

    @classmethod
    def register_provider(cls, provider_type: str, provider_class: Any) -> None:
        """
        Registers a new storage provider class.
        """
        cls._providers[provider_type] = provider_class

    @classmethod
    def create(cls, provider_type: str, credentials: Credential) -> BaseStorage:
        """
        Creates a new storage provider instance.

        Args:
            provider_type: The type of provider to create (e.g., 's3', 'gdrive').
            credentials: The credentials for the provider.

        Returns:
            An instance of a BaseStorage subclass.

        Raises:
            ValueError: If the provider type is not registered.
        """
        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f"Unsupported provider type: {provider_type}")
        return provider_class(credentials)