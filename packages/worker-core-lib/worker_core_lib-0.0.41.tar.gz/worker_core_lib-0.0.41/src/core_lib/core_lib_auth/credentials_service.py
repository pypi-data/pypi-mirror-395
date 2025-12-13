# worker-core-lib/src/core_lib/core_lib_auth/credentials_service.py
import json
import logging
import re
from typing import NamedTuple, Dict, Any

from sqlalchemy.orm import Session, joinedload

from .crypto import decrypt
from ..core_lib_db.models import StorageConnection, StorageProviderConfig

logger = logging.getLogger(__name__)


def to_snake_case(name: str) -> str:
    """Converts a camelCase string to snake_case."""
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Credential(NamedTuple):
    """A generic container for credentials."""
    # Google Drive / OAuth
    access_token: str = None
    refresh_token: str = None
    token_type: str = None
    expiry_date: Any = None  # Changed from int to Any for flexibility
    scope: str = None
    # Can hold the full token dictionary for libraries that need it
    token: Dict[str, Any] = None

    # SFTP / Basic Auth
    username: str = None
    password: str = None
    private_key: str = None
    
    # S3 / AWS
    access_key: str = None
    secret_key: str = None


class CredentialsService:
    """
    A service to fetch and decrypt credentials from the database for a given storage connection.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_credentials_for_connection(self, storage_connection_id: str) -> Credential:
        """
        Fetches and decrypts credentials for a given storage connection ID.
        """
        logger.info(f"Fetching credentials for storage connection ID: {storage_connection_id}")

        try:
            connection = (
                self.db_session.query(StorageConnection)
                .filter(StorageConnection.id == storage_connection_id)
                .one_or_none()
            )
        except Exception as e:
            # Rollback the session if query fails
            logger.error(f"Database query failed: {e}")
            self.db_session.rollback()
            raise

        if not connection:
            raise ValueError(f"StorageConnection with ID '{storage_connection_id}' not found.")

        # Credentials are stored directly on the storage_connections table
        encrypted_creds = connection.encrypted_credentials
        if not encrypted_creds:
            raise ValueError(f"Missing encrypted credentials for connection ID '{storage_connection_id}'.")

        logger.debug(f"Found encrypted credentials (length: {len(encrypted_creds) if encrypted_creds else 0})")

        # The encrypted_creds is a single encrypted string, not JSON
        # We need to decrypt it first, then parse as JSON
        try:
            decrypted_json_str = decrypt(encrypted_creds)
            encrypted_creds = json.loads(decrypted_json_str)
            logger.info(f"DEBUG: Decrypted credentials dict: {encrypted_creds}")
        except (ValueError, TypeError) as e:
            logger.error(f"Failed to decrypt or parse credentials: {e}")
            raise ValueError(f"Failed to decrypt/parse credentials for connection '{storage_connection_id}'") from e
        
        # At this point, encrypted_creds is a dict with decrypted values
        # For Google Drive, handle the token field specially
        if connection.provider == 'google_drive' and 'token' in encrypted_creds:
            token_value = encrypted_creds['token']
            if isinstance(token_value, str):
                try:
                    token_data = json.loads(token_value)
                    return Credential(token=token_data)
                except ValueError:
                    logger.warning(f"The 'token' field for connection {storage_connection_id} could not be parsed as JSON.")
            elif isinstance(token_value, dict):
                return Credential(token=token_value)
        
        # Convert all keys from camelCase to snake_case to match Python model
        snake_case_creds = {to_snake_case(k): v for k, v in encrypted_creds.items()}
        logger.info(f"DEBUG: After snake_case conversion: {snake_case_creds}")
        
        # Get the set of valid field names for the Credential NamedTuple
        valid_keys = set(Credential._fields)
        
        # Filter the dictionary to only include keys that are valid fields
        filtered_creds = {k: v for k, v in snake_case_creds.items() if k in valid_keys}
        logger.info(f"DEBUG: After filtering to valid fields: {filtered_creds}")
        
        logger.info(f"Successfully decrypted credentials for connection {storage_connection_id}.")
        return Credential(**filtered_creds)

    def get_connection_config(self, storage_connection_id: str) -> Dict[str, Any]:
        """
        Fetches configuration data (host, port, etc.) for a given storage connection ID.
        Also retrieves scanRootPath from the related storage_provider_configs table.
        
        NOTE: host, port are now stored in encryptedCredentials, not as separate columns.
        Use get_credentials_for_connection() to retrieve these values.
        """
        logger.info(f"Fetching connection config for storage connection ID: {storage_connection_id}")

        try:
            connection = (
                self.db_session.query(StorageConnection)
                .options(joinedload(StorageConnection.config))
                .filter(StorageConnection.id == storage_connection_id)
                .one_or_none()
            )
        except Exception as e:
            logger.error(f"Database query failed: {e}")
            self.db_session.rollback()
            raise

        if not connection:
            raise ValueError(f"StorageConnection with ID '{storage_connection_id}' not found.")

        config = {}
        
        # host and port are now inside encryptedCredentials, retrieve them
        # by decrypting the credentials
        encrypted_creds = connection.encrypted_credentials
        if encrypted_creds:
            try:
                decrypted_json_str = decrypt(encrypted_creds)
                creds_data = json.loads(decrypted_json_str)
                
                if 'host' in creds_data:
                    config['host'] = creds_data['host']
                if 'port' in creds_data:
                    config['port'] = creds_data['port']
            except Exception as e:
                logger.warning(f"Failed to extract host/port from encrypted credentials: {e}")
        
        # Get scanRootPath from the related storage_provider_configs table
        if connection.config:
            scan_root_path = getattr(connection.config, 'scanRootPath', None)
            if scan_root_path:
                config['scanRootPath'] = scan_root_path
        
        logger.info(f"Successfully retrieved config for connection {storage_connection_id}: {config}")
        return config