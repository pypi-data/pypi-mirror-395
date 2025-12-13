import logging
import os
from functools import lru_cache
from typing import Any

from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings

# Configure a basic logger
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CoreSettings(BaseSettings):
    """
    Core settings shared by all workers.
    """
    REDIS_HOST: str
    REDIS_PORT: int
    LOG_LEVEL: str = "INFO"
    ENCRYPTION_KEY: str = Field(..., min_length=64, max_length=64, description="Encryption key must be exactly 64 characters (hex string)")

    ENABLE_VERBOSE_TRACES: bool = False

    def model_post_init(self, __context: Any) -> None:
        """Hook called after settings are loaded and validated."""
        if self.ENABLE_VERBOSE_TRACES:

            logger.info("--- CoreSettings loaded from environment ---")
            
            # Set standard environment variables that redis-py and other libs might use
            redis_url = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
            os.environ["REDIS_HOST"] = self.REDIS_HOST
            os.environ["REDIS_PORT"] = str(self.REDIS_PORT)
            os.environ["REDIS_URL"] = redis_url
            os.environ["ENCRYPTION_KEY"] = self.ENCRYPTION_KEY

            # Use model_dump to create a dictionary, excluding sensitive fields
            config_to_print = self.model_dump(exclude={'ENCRYPTION_KEY'})
            for key, value in config_to_print.items():
                logger.info(f"  - {key}: {value}")
            
            logger.info(f"  - Set REDIS_URL: {redis_url}")

            if not self.ENCRYPTION_KEY:
                logger.warning("  - ENCRYPTION_KEY is NOT set.")
            else:
                logger.info("  - ENCRYPTION_KEY: [REDACTED]")
            logger.info("---------------------------------------------")
        pass


class S3Settings(BaseSettings):
    """
    Settings for connecting to S3-compatible storage.
    """
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_BUCKET: str

    def model_post_init(self, __context: Any) -> None:
        """Hook called after settings are loaded and validated."""
        logger.info("--- S3Settings loaded from environment ---")
        config_to_print = self.model_dump(exclude={'S3_SECRET_ACCESS_KEY'})
        for key, value in config_to_print.items():
            logger.info(f"  - {key}: {value}")
        logger.info("  - S3_SECRET_ACCESS_KEY: [REDACTED]")
        logger.info("------------------------------------------")


class DBSettings(BaseSettings):
    """
    Settings for connecting to the database.
    """
    DB_USER: str = Field(..., validation_alias=AliasChoices("DB_USERNAME", "POSTGRES_USER"))
    DB_PASSWORD: str = Field(..., validation_alias=AliasChoices("DB_PASSWORD", "POSTGRES_PASSWORD"))
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str = Field(..., validation_alias=AliasChoices("DB_DATABASE", "POSTGRES_DB"))

    @property
    def database_url(self) -> str:
        if self.DB_HOST == ":memory:":
            return "sqlite:///:memory:"
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def model_post_init(self, __context: Any) -> None:
        """Hook called after settings are loaded and validated."""
        logger.info("--- DBSettings loaded from environment ---")
        config_to_print = self.model_dump(exclude={'DB_PASSWORD'})
        for key, value in config_to_print.items():
            logger.info(f"  - {key}: {value}")
        logger.info("  - DB_PASSWORD: [REDACTED]")
        logger.info(f"  - Generated DB URL (password redacted): postgresql://{self.DB_USER}:[REDACTED]@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        logger.info("------------------------------------------")


class GoogleSettings(BaseSettings):
    """
    Settings for Google API authentication.
    """
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    def model_post_init(self, __context: Any) -> None:
        """Hook called after settings are loaded and validated."""
        logger.info("--- GoogleSettings loaded from environment ---")
        config_to_print = self.model_dump(exclude={'GOOGLE_CLIENT_SECRET'})
        for key, value in config_to_print.items():
            logger.info(f"  - {key}: {value}")
        logger.info("  - GOOGLE_CLIENT_SECRET: [REDACTED]")
        logger.info("----------------------------------------------")


@lru_cache()
def get_settings() -> CoreSettings:
    return CoreSettings()

class OllamaSettings(BaseSettings):
    OLLAMA_API_URL: str = "http://ollama-service:11434"
    OLLAMA_MODEL: str = "llama2"
    OLLAMA_REQUEST_TIMEOUT: int = 60
