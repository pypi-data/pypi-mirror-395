"""
Data masking module for PII display.

Provides various masking strategies for different PII types.
"""

import re
from typing import Optional


class Masker:
    """Handles masking of PII data for display purposes."""
    
    def mask(self, value: Optional[str], pii_type: str) -> Optional[str]:
        """
        Return a masked version based on PII data type.
        
        Args:
            value: The plaintext value to mask
            pii_type: Type of PII (email, phone, etc.)
            
        Returns:
            Masked version of the value
        """
        if value is None:
            return None
        
        pii_type = pii_type.lower()
        
        # Map data types to masking functions
        masking_map = {
            "email": self._mask_email,
            "phone": self._mask_phone,
            "person_name": self._mask_text,
            "company_name": self._mask_text,
            "address": self._mask_address,
            "ssn": self._mask_ssn,
            "credit_card": self._mask_credit_card,
            "ip_address": self._mask_ip_address,
            "date_of_birth": self._mask_text,
            "generic_text": self._mask_text,
        }
        
        masking_func = masking_map.get(pii_type, lambda x: x)
        return masking_func(value)
    
    def _mask_email(self, email: str) -> str:
        """Mask email address."""
        if not email or "@" not in email:
            return email
        name, domain = email.split("@", 1)
        if not name:
            return "***@" + domain
        return name[0] + "***@" + domain
    
    def _mask_phone(self, phone: str) -> str:
        """Mask phone number."""
        if not phone:
            return phone
        cleaned = re.sub(r"\D", "", phone)
        if len(cleaned) <= 4:
            return "*" * len(cleaned)
        return "*" * (len(cleaned) - 4) + cleaned[-4:]
    
    def _mask_text(self, text: str) -> str:
        """Mask generic text."""
        if not text:
            return text
        if len(text) <= 2:
            return text[0] + "*"
        return text[0] + "*" * (len(text) - 1)
    
    def _mask_address(self, address: str) -> str:
        """Mask address keeping only first few characters."""
        if not address or len(address) <= 10:
            return "***"
        return address[:10] + "***"
    
    def _mask_ssn(self, ssn: str) -> str:
        """Mask SSN showing only last 4 digits."""
        cleaned = re.sub(r"\D", "", ssn)
        if len(cleaned) <= 4:
            return "***"
        return "***-**-" + cleaned[-4:]
    
    def _mask_credit_card(self, cc: str) -> str:
        """Mask credit card showing only last 4 digits."""
        cleaned = re.sub(r"\D", "", cc)
        if len(cleaned) <= 4:
            return "****"
        return "****-****-****-" + cleaned[-4:]
    
    def _mask_ip_address(self, ip: str) -> str:
        """Mask IP address showing only first octet."""
        parts = ip.split(".")
        if len(parts) != 4:
            return "***.***.***.***"
        return f"{parts[0]}.***.***.***"