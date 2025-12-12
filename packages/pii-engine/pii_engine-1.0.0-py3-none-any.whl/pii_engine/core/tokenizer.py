"""
Tokenizer module for PII data.

Handles deterministic tokenization and database operations for PII tokens.
"""

import hashlib
from typing import Optional

class Tokenizer:
    """Handles tokenization for PII data (pseudonymized storage version)."""
    
    def __init__(self, db_connection_func=None):
        """
        Initialize tokenizer.
        
        Args:
            db_connection_func: Function to get database connection (optional)
        """
        # No encryptor needed for pseudonymized storage
        self.get_db_connection = db_connection_func or self._get_default_connection
    
    def _get_default_connection(self):
        """Default database connection - override in production."""
        try:
            from db import get_connection
            return get_connection()
        except ImportError:
            raise RuntimeError(
                "No database connection function provided. "
                "Pass db_connection_func to Tokenizer constructor."
            )
    
    def _compute_token(self, kind: str, value: str) -> str:
        """
        Deterministic token: same (kind, value) -> same token.
        Good for duplicate checks and joins.
        
        Args:
            kind: Type of PII (email, phone, etc.)
            value: The PII value to tokenize
            
        Returns:
            Deterministic token string
        """
        kind = kind.lower()
        h = hashlib.sha256(f"{kind}:{value}".encode("utf-8")).hexdigest()
        return f"TKN_{kind.upper()}_{h[:16]}"
    
    def tokenize(self, value: Optional[str], kind: str) -> Optional[str]:
        """
        Generate deterministic token for PII value.

        Args:
            value: The PII value to tokenize
            kind: Type of PII (email, phone, etc.)
            
        Returns:
            Deterministic token or None if value is None
        """
        if value is None:
            return None

        kind_lower = kind.lower()
        token = self._compute_token(kind_lower, value)
        return token
    
    def detokenize(self, token: Optional[str], kind: str) -> Optional[str]:
        """
        For pseudonymized storage, detokenization is not supported.
        Original values are only available in session cache.

        Args:
            token: The token to detokenize
            kind: Type of PII (email, phone, etc.)
            
        Returns:
            None (not supported in pseudonymized mode)
        """
        # In pseudonymized storage mode, we don't store encrypted original values
        # Original values are only available in session cache during processing
        return None