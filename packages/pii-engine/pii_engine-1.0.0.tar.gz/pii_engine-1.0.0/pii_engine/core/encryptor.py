"""
Encryption/Decryption module for PII data.

Handles AES-256 encryption using Fernet for secure PII storage.
"""

import os
from typing import Optional
from cryptography.fernet import Fernet


class Encryptor:
    """Handles encryption and decryption of PII data."""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryptor with encryption key.
        
        Args:
            encryption_key: Base64 encoded Fernet key. If None, reads from PII_ENC_KEY env var.
        """
        if encryption_key is None:
            encryption_key = os.environ.get("PII_ENC_KEY")
        
        if not encryption_key:
            raise RuntimeError(
                "PII_ENC_KEY environment variable is not set. "
                "Create a .env file or export PII_ENC_KEY before running."
            )
        
        # Fernet key is already base64 encoded, use as bytes
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode("utf-8")
        self.fernet = Fernet(encryption_key)
    
    def encrypt(self, value: str) -> bytes:
        """
        Encrypt a plaintext string to ciphertext bytes.
        
        Args:
            value: Plaintext string to encrypt
            
        Returns:
            Encrypted bytes
        """
        return self.fernet.encrypt(value.encode("utf-8"))
    
    def decrypt(self, cipher: bytes) -> str:
        """
        Decrypt ciphertext bytes to plaintext string.
        
        Args:
            cipher: Encrypted bytes to decrypt
            
        Returns:
            Decrypted plaintext string
        """
        return self.fernet.decrypt(cipher).decode("utf-8")
    
    @staticmethod
    def generate_key() -> str:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            Base64 encoded encryption key
        """
        return Fernet.generate_key().decode("utf-8")