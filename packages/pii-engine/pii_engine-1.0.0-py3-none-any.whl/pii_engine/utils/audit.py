"""
Audit logging for PII operations.

Provides comprehensive logging of all PII access and operations for compliance.
"""

import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLogger:
    """Handles audit logging for PII operations."""
    
    def __init__(self, logger_name: str = "pii_audit"):
        """
        Initialize audit logger.
        
        Args:
            logger_name: Name of the logger instance
        """
        self.logger = logging.getLogger(logger_name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup audit logger with appropriate formatting."""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def log_pii_operation(
        self,
        operation: str,
        pii_type: str,
        field: str,
        table: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        """
        Log PII processing operation.
        
        Args:
            operation: Type of operation (tokenize, encrypt, decrypt, etc.)
            pii_type: Type of PII being processed
            field: Field name being processed
            table: Table/entity name
            user_id: ID of user performing operation
            session_id: Session ID
            additional_data: Additional context data
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "pii_operation",
            "operation": operation,
            "pii_type": pii_type,
            "field": field,
            "table": table,
            "user_id": user_id,
            "session_id": session_id,
            "additional_data": additional_data or {}
        }
        
        self.logger.info(f"PII_OPERATION: {json.dumps(audit_entry)}")
    
    def log_pii_access(
        self,
        operation: str,
        pii_type: str,
        field: str,
        display_mode: str,
        user_role: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """
        Log PII access/display operation.
        
        Args:
            operation: Type of operation (display, export, etc.)
            pii_type: Type of PII being accessed
            field: Field name being accessed
            display_mode: How data is displayed (masked, pseudonymized, plaintext)
            user_role: Role of accessing user
            user_id: ID of user accessing data
            session_id: Session ID
            ip_address: IP address of request
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "pii_access",
            "operation": operation,
            "pii_type": pii_type,
            "field": field,
            "display_mode": display_mode,
            "user_role": user_role,
            "user_id": user_id,
            "session_id": session_id,
            "ip_address": ip_address
        }
        
        # Log as WARNING for plaintext access to ensure visibility
        if display_mode == "plaintext":
            self.logger.warning(f"PII_PLAINTEXT_ACCESS: {json.dumps(audit_entry)}")
        else:
            self.logger.info(f"PII_ACCESS: {json.dumps(audit_entry)}")
    
    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        """
        Log security-related events.
        
        Args:
            event_type: Type of security event
            severity: Severity level (low, medium, high, critical)
            description: Description of the event
            user_id: ID of user involved
            ip_address: IP address involved
            additional_data: Additional context data
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "security_event",
            "security_event_type": event_type,
            "severity": severity,
            "description": description,
            "user_id": user_id,
            "ip_address": ip_address,
            "additional_data": additional_data or {}
        }
        
        # Log based on severity
        if severity.lower() in ["high", "critical"]:
            self.logger.error(f"SECURITY_EVENT: {json.dumps(audit_entry)}")
        elif severity.lower() == "medium":
            self.logger.warning(f"SECURITY_EVENT: {json.dumps(audit_entry)}")
        else:
            self.logger.info(f"SECURITY_EVENT: {json.dumps(audit_entry)}")
    
    def log_compliance_event(
        self,
        regulation: str,
        event_type: str,
        description: str,
        user_id: Optional[str] = None,
        data_subject_id: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        """
        Log compliance-related events (GDPR, CCPA, etc.).
        
        Args:
            regulation: Regulation type (GDPR, CCPA, HIPAA, etc.)
            event_type: Type of compliance event
            description: Description of the event
            user_id: ID of user involved
            data_subject_id: ID of data subject
            additional_data: Additional context data
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "compliance_event",
            "regulation": regulation,
            "compliance_event_type": event_type,
            "description": description,
            "user_id": user_id,
            "data_subject_id": data_subject_id,
            "additional_data": additional_data or {}
        }
        
        self.logger.info(f"COMPLIANCE_EVENT: {json.dumps(audit_entry)}")