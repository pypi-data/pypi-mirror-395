"""
PII Engine - Production-grade PII processing for Employment Exchange
"""

from .fabricator import (
    mask, unmask, pseudo, unpseudo, encrypt, decrypt,
    fabricator_check, update_token_set, FABRICATOR, fabricator_config
)
from .middleware import PIIMiddleware, PIIService, pii_process_input, pii_process_output
from .database import PIIDatabase

__version__ = "1.0.0"
__all__ = [
    "mask", "unmask", "pseudo", "unpseudo", "encrypt", "decrypt",
    "fabricator_check", "update_token_set", "FABRICATOR", "fabricator_config",
    "PIIMiddleware", "PIIService", "pii_process_input", "pii_process_output", "PIIDatabase"
]