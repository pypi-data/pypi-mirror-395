"""
Policy engine for PII handling rules and access control.

Manages PII classification, processing rules, and role-based access.
"""

import yaml
from typing import Dict, List, Optional
from pathlib import Path
from ..config.pii_types import PIIDataType, SCHEMA_CONFIG


class PolicyEngine:
    """Manages PII policies and access control rules."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize policy engine with configuration.
        
        Args:
            config_path: Path to policy configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self.policies = self._load_policies()
        self.schema_config = SCHEMA_CONFIG
    
    def _get_default_config_path(self) -> str:
        """Get default policy configuration path."""
        return str(Path(__file__).parent.parent / "config" / "policies.yaml")
    
    def _load_policies(self) -> Dict:
        """Load policies from configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Return default policies if config file not found
            return self._get_default_policies()
    
    def _get_default_policies(self) -> Dict:
        """Get default PII policies."""
        return {
            "pii_policies": {
                "email": {
                    "classification": "HIGH_RISK",
                    "processing": {
                        "tokenize": True,
                        "encrypt": True,
                        "mask_display": True
                    },
                    "retention_days": 2555
                },
                "phone": {
                    "classification": "MEDIUM_RISK", 
                    "processing": {
                        "tokenize": True,
                        "encrypt": True,
                        "pseudonymize": True
                    },
                    "retention_days": 1825
                },
                "person_name": {
                    "classification": "HIGH_RISK",
                    "processing": {
                        "tokenize": True,
                        "encrypt": True,
                        "pseudonymize": True
                    },
                    "retention_days": 2555
                }
            },
            "access_policies": {
                "roles": {
                    "admin": {
                        "can_view_plaintext": True,
                        "audit_required": True
                    },
                    "user": {
                        "can_view_masked": True,
                        "can_view_pseudonymized": True
                    },
                    "analyst": {
                        "can_view_pseudonymized": True,
                        "can_view_aggregated": True
                    }
                }
            }
        }
    
    def get_pii_data_type(self, table_name: str, column_name: str) -> PIIDataType:
        """
        Get PII data type enum for a specific table column.
        
        Args:
            table_name: Name of the table/entity
            column_name: Name of the column/field
            
        Returns:
            PIIDataType enum value
        """
        table_config = self.schema_config.get(table_name, {})
        return table_config.get(column_name, PIIDataType.GENERIC_TEXT)
    
    def get_pii_fields(self, table_name: str) -> List[str]:
        """
        Get all PII fields for a table.
        
        Args:
            table_name: Name of the table/entity
            
        Returns:
            List of PII field names
        """
        return list(self.schema_config.get(table_name, {}).keys())
    
    def should_tokenize(self, pii_type: str) -> bool:
        """
        Check if PII type should be tokenized.
        
        Args:
            pii_type: Type of PII data
            
        Returns:
            True if should be tokenized
        """
        policy = self.policies.get("pii_policies", {}).get(pii_type, {})
        processing = policy.get("processing", {})
        return processing.get("tokenize", False)
    
    def should_encrypt(self, pii_type: str) -> bool:
        """
        Check if PII type should be encrypted.
        
        Args:
            pii_type: Type of PII data
            
        Returns:
            True if should be encrypted
        """
        policy = self.policies.get("pii_policies", {}).get(pii_type, {})
        processing = policy.get("processing", {})
        return processing.get("encrypt", False)
    
    def can_access_mode(self, user_role: str, display_mode: str) -> bool:
        """
        Check if user role can access specific display mode.
        
        Args:
            user_role: Role of the user
            display_mode: Requested display mode (masked, pseudonymized, plaintext)
            
        Returns:
            True if access is allowed
        """
        roles = self.policies.get("access_policies", {}).get("roles", {})
        role_permissions = roles.get(user_role, {})
        
        if display_mode == "plaintext":
            return role_permissions.get("can_view_plaintext", False)
        elif display_mode == "pseudonymized":
            return role_permissions.get("can_view_pseudonymized", False)
        else:  # masked
            return role_permissions.get("can_view_masked", True)  # Default allow masked
    
    def get_retention_days(self, pii_type: str) -> int:
        """
        Get retention period for PII type.
        
        Args:
            pii_type: Type of PII data
            
        Returns:
            Number of days to retain data
        """
        policy = self.policies.get("pii_policies", {}).get(pii_type, {})
        return policy.get("retention_days", 365)  # Default 1 year
    
    def get_classification(self, pii_type: str) -> str:
        """
        Get risk classification for PII type.
        
        Args:
            pii_type: Type of PII data
            
        Returns:
            Risk classification (HIGH_RISK, MEDIUM_RISK, LOW_RISK)
        """
        policy = self.policies.get("pii_policies", {}).get(pii_type, {})
        return policy.get("classification", "MEDIUM_RISK")
    
    def is_pii_field(self, field_name: str, table_name: str = None) -> bool:
        """
        Check if a field is classified as PII.
        
        Args:
            field_name: Name of the field
            table_name: Name of the table/entity (optional)
            
        Returns:
            True if field contains PII data
        """
        # Check if field is in schema config for this table
        if table_name:
            table_config = self.schema_config.get(table_name, {})
            if field_name in table_config:
                return True
        
        # Check common PII field names
        pii_field_patterns = [
            'email', 'phone', 'name', 'ssn', 'social_security',
            'address', 'credit_card', 'passport', 'license',
            'first_name', 'last_name', 'full_name', 'person_name'
        ]
        
        field_lower = field_name.lower()
        return any(pattern in field_lower for pattern in pii_field_patterns)
    
    def get_pii_type_from_field(self, field_name: str) -> str:
        """
        Get PII type from field name.
        
        Args:
            field_name: Name of the field
            
        Returns:
            PII type string
        """
        field_lower = field_name.lower()
        
        if 'email' in field_lower:
            return 'email'
        elif 'phone' in field_lower:
            return 'phone'
        elif 'name' in field_lower:
            return 'name'
        elif 'ssn' in field_lower or 'social_security' in field_lower:
            return 'ssn'
        elif 'address' in field_lower:
            return 'address'
        elif 'credit_card' in field_lower or 'card' in field_lower:
            return 'credit_card'
        else:
            return 'generic_text'
    
    def get_pii_type(self, field_name: str, table_name: str = None) -> str:
        """
        Get PII data type for a specific field.
        
        Args:
            field_name: Name of the field
            table_name: Name of the table/entity (optional)
            
        Returns:
            PII type string
        """
        return self.get_pii_type_from_field(field_name)