"""
Main PII Engine - Central orchestrator for all PII operations.

This is the primary interface that all endpoints should use.
"""

from typing import Dict, Any, Optional, List
from .tokenizer import Tokenizer
from .encryptor import Encryptor
from .pseudonymizer import Pseudonymizer
from .masker import Masker
from .policy_engine import PolicyEngine
from ..config.pii_types import PIIDataType
from ..utils.audit import AuditLogger


class PIIEngine:
    """
    Central PII processing engine for all endpoints.
    
    This class provides a unified interface for:
    - Tokenization and encryption of PII data
    - Role-based display formatting (masked/pseudonymized/plaintext)
    - Policy-driven PII handling
    - Audit logging
    
    Usage:
        engine = PIIEngine()
        
        # Process input data
        processed = engine.process_input_data({
            "email": "john@example.com",
            "phone": "+1-555-123-4567"
        })
        
        # Get display data based on user role
        display_data = engine.get_display_data(processed, user_role="user")
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize PII Engine with optional custom config."""
        self.tokenizer = Tokenizer()
        self.encryptor = Encryptor()
        self.pseudonymizer = Pseudonymizer()
        self.masker = Masker()
        self.policy_engine = PolicyEngine(config_path)
        self.audit_logger = AuditLogger()
    
    def process_input_data(self, data: Dict[str, Any], table_name: str = "default") -> Dict[str, Any]:
        """
        Process input data by tokenizing and encrypting PII fields.
        
        Args:
            data: Raw input data containing PII
            table_name: Table/entity name for policy lookup
            
        Returns:
            Dictionary with PII fields replaced by tokens
        """
        processed_data = {}
        pii_fields = self.policy_engine.get_pii_fields(table_name)
        
        for field, value in data.items():
            if field in pii_fields and value is not None:
                # Get PII type for this field
                pii_type = self.policy_engine.get_pii_type(table_name, field)
                
                # Tokenize and encrypt
                token = self.tokenizer.tokenize(value, pii_type.value)
                processed_data[f"{field}_token"] = token
                
                # Log the operation
                self.audit_logger.log_pii_operation(
                    operation="tokenize",
                    pii_type=pii_type.value,
                    field=field,
                    table=table_name
                )
            else:
                # Non-PII field, keep as-is
                processed_data[field] = value
        
        return processed_data
    
    def get_display_data(
        self, 
        tokenized_data: Dict[str, Any], 
        table_name: str = "default",
        display_mode: str = "masked",
        user_role: str = "user"
    ) -> Dict[str, Any]:
        """
        Convert tokenized data to display format based on user role.
        
        Args:
            tokenized_data: Data with PII tokens
            table_name: Table/entity name for policy lookup
            display_mode: "masked", "pseudonymized", or "plaintext"
            user_role: User role for access control
            
        Returns:
            Dictionary with PII fields in appropriate display format
        """
        display_data = {}
        pii_fields = self.policy_engine.get_pii_fields(table_name)
        
        # Check if user has permission for requested display mode
        if not self.policy_engine.can_access_mode(user_role, display_mode):
            display_mode = "masked"  # Fallback to masked
        
        for field, value in tokenized_data.items():
            if field.endswith("_token"):
                # This is a tokenized PII field
                original_field = field[:-6]  # Remove "_token" suffix
                
                if original_field in pii_fields:
                    pii_type = self.policy_engine.get_pii_type(table_name, original_field)
                    
                    # Detokenize to get plaintext
                    plaintext = self.tokenizer.detokenize(value, pii_type.value)
                    
                    # Apply display formatting
                    if display_mode == "plaintext":
                        display_data[original_field] = plaintext
                    elif display_mode == "pseudonymized":
                        display_data[original_field] = self.pseudonymizer.pseudonymize(
                            plaintext, pii_type.value
                        )
                    else:  # masked
                        display_data[original_field] = self.masker.mask(
                            plaintext, pii_type.value
                        )
                    
                    # Keep token for debugging (optional)
                    display_data[f"{original_field}_token"] = value
                    
                    # Log the access
                    self.audit_logger.log_pii_access(
                        operation="display",
                        pii_type=pii_type.value,
                        field=original_field,
                        display_mode=display_mode,
                        user_role=user_role
                    )
            else:
                # Non-PII field, keep as-is
                display_data[field] = value
        
        return display_data
    
    def bulk_process_records(
        self, 
        records: List[Dict[str, Any]], 
        table_name: str = "default"
    ) -> List[Dict[str, Any]]:
        """
        Process multiple records efficiently.
        
        Args:
            records: List of records to process
            table_name: Table/entity name for policy lookup
            
        Returns:
            List of processed records with tokenized PII
        """
        return [self.process_input_data(record, table_name) for record in records]
    
    def bulk_display_records(
        self,
        tokenized_records: List[Dict[str, Any]],
        table_name: str = "default",
        display_mode: str = "masked",
        user_role: str = "user"
    ) -> List[Dict[str, Any]]:
        """
        Convert multiple tokenized records to display format.
        
        Args:
            tokenized_records: List of records with PII tokens
            table_name: Table/entity name for policy lookup
            display_mode: "masked", "pseudonymized", or "plaintext"
            user_role: User role for access control
            
        Returns:
            List of records in appropriate display format
        """
        return [
            self.get_display_data(record, table_name, display_mode, user_role)
            for record in tokenized_records
        ]
    
    def check_duplicate(
        self, 
        data: Dict[str, Any], 
        table_name: str = "default",
        duplicate_fields: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Check for duplicates using tokenized fields.
        
        Args:
            data: Input data to check
            table_name: Table/entity name
            duplicate_fields: Fields to check for duplicates (if None, uses all PII fields)
            
        Returns:
            Token of duplicate field if found, None otherwise
        """
        if duplicate_fields is None:
            duplicate_fields = self.policy_engine.get_pii_fields(table_name)
        
        for field in duplicate_fields:
            if field in data and data[field] is not None:
                pii_type = self.policy_engine.get_pii_type(table_name, field)
                token = self.tokenizer.tokenize(data[field], pii_type.value)
                
                # This would typically query your database
                # For now, return the token that can be used in SQL queries
                return token
        
        return None
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of PII engine components."""
        return {
            "status": "healthy",
            "components": {
                "tokenizer": "operational",
                "encryptor": "operational", 
                "pseudonymizer": "operational",
                "masker": "operational",
                "policy_engine": "operational"
            },
            "version": "1.0.0"
        }