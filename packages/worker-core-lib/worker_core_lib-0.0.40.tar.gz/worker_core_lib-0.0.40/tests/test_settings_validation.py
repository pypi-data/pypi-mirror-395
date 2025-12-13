"""
Tests for CoreSettings validation, especially ENCRYPTION_KEY validation.
"""
import os
import pytest
from pydantic import ValidationError

from src.core_lib.core_lib_config.settings import CoreSettings


class TestCoreSettingsValidation:
    """Tests for CoreSettings validation."""
    
    def test_encryption_key_too_short(self):
        """Test that ENCRYPTION_KEY must be at least 64 characters."""
        # Setup environment with short encryption key
        test_env = {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "ENCRYPTION_KEY": "short-key-only-9-chars"
        }
        
        # Execute & Assert
        with pytest.raises(ValidationError) as exc_info:
            CoreSettings(**test_env)
        
        # Check the error message
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert errors[0]["loc"] == ("ENCRYPTION_KEY",)
        assert "at least 64 characters" in errors[0]["msg"]
    
    def test_encryption_key_too_long(self):
        """Test that ENCRYPTION_KEY must be at most 64 characters."""
        # Setup environment with long encryption key
        test_env = {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "ENCRYPTION_KEY": "a" * 65  # 65 characters, one too many
        }
        
        # Execute & Assert
        with pytest.raises(ValidationError) as exc_info:
            CoreSettings(**test_env)
        
        # Check the error message
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert errors[0]["loc"] == ("ENCRYPTION_KEY",)
        assert "at most 64 characters" in errors[0]["msg"]
    
    def test_encryption_key_valid(self):
        """Test that ENCRYPTION_KEY with exactly 64 characters is accepted."""
        # Setup environment with valid encryption key
        test_env = {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "ENCRYPTION_KEY": "a" * 64,  # Exactly 64 characters
            "LOG_LEVEL": "INFO"
        }
        
        # Execute
        settings = CoreSettings(**test_env)
        
        # Assert
        assert settings.ENCRYPTION_KEY == "a" * 64
        assert len(settings.ENCRYPTION_KEY) == 64
    
    def test_encryption_key_hex_string_format(self):
        """Test that a valid 64-character hex string is accepted."""
        # Setup environment with valid hex string
        valid_hex_key = "0123456789abcdef" * 4  # 64 hex characters
        test_env = {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "ENCRYPTION_KEY": valid_hex_key,
            "LOG_LEVEL": "DEBUG"
        }
        
        # Execute
        settings = CoreSettings(**test_env)
        
        # Assert
        assert settings.ENCRYPTION_KEY == valid_hex_key
        assert len(settings.ENCRYPTION_KEY) == 64
    
    def test_encryption_key_required(self):
        """Test that ENCRYPTION_KEY is a required field."""
        # Setup environment without encryption key
        test_env = {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
        }
        
        # Execute & Assert
        with pytest.raises(ValidationError) as exc_info:
            CoreSettings(**test_env)
        
        # Check the error message
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("ENCRYPTION_KEY",) for error in errors)
    
    def test_all_required_fields(self):
        """Test that all required fields are validated."""
        # Setup environment with all required fields
        test_env = {
            "REDIS_HOST": "redis.example.com",
            "REDIS_PORT": "6380",
            "ENCRYPTION_KEY": "f" * 64,
            "LOG_LEVEL": "WARNING"
        }
        
        # Execute
        settings = CoreSettings(**test_env)
        
        # Assert
        assert settings.REDIS_HOST == "redis.example.com"
        assert settings.REDIS_PORT == 6380
        assert settings.LOG_LEVEL == "WARNING"
        assert len(settings.ENCRYPTION_KEY) == 64


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
