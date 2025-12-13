# worker-core-lib/src/core_lib/core_lib_auth/crypto.py
import os
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

# This key must be the same 32-byte (64 hex characters) key used in the NestJS backend.
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
if not ENCRYPTION_KEY or len(ENCRYPTION_KEY) != 64:
    raise ValueError("ENCRYPTION_KEY environment variable must be a 64-character hex string.")

KEY_BYTES = bytes.fromhex(ENCRYPTION_KEY)
IV_LENGTH = 12  # As defined in your NestJS service
TAG_LENGTH = 16 # As defined in your NestJS service

def decrypt(encrypted_text: str) -> str:
    """
    Decrypts a string that was encrypted by the NestJS backend using AES-256-GCM.
    Expects the format to be 'iv_hex:tag_hex:encrypted_text_hex'.
    """
    if not encrypted_text:
        return ""
        
    try:
        # 1. Split the input into its three hex-encoded parts
        iv_hex, tag_hex, encrypted_hex = encrypted_text.split(':')
        
        # 2. Convert hex parts back to bytes
        iv = bytes.fromhex(iv_hex)
        tag = bytes.fromhex(tag_hex)
        encrypted_data = bytes.fromhex(encrypted_hex)

        # 3. Verify component lengths
        if len(iv) != IV_LENGTH:
            raise ValueError(f"Invalid IV length. Expected {IV_LENGTH}, got {len(iv)}.")
        if len(tag) != TAG_LENGTH:
            raise ValueError(f"Invalid authTag length. Expected {TAG_LENGTH}, got {len(tag)}.")

        # 4. Create the AES-GCM cipher for decryption
        # For GCM in cryptography, the tag is passed during initialization of the mode.
        cipher = Cipher(algorithms.AES(KEY_BYTES), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # 5. Decrypt the data. GCM authenticates the tag automatically.
        # If the tag is invalid, this will raise an InvalidTag exception.
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        return decrypted_data.decode('utf-8')
        
    except Exception as e:
        # This catches format errors (e.g., split fails), hex decoding errors,
        # or an InvalidTag exception from the cryptography library, which indicates
        # the data was tampered with or the key is wrong.
        logger.error(f"Decryption failed. The data may be corrupted, tampered with, or the key is incorrect. Error: {e}")
        raise ValueError("Decryption failed. Please check credentials format and encryption key.") from e