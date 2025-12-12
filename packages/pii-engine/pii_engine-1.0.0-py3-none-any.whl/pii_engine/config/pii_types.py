# pii_config.py
from enum import Enum
from typing import Dict, List

class PIIDataType(Enum):
    """Standardized PII data types for masking and tokenization."""
    EMAIL = "email"
    PHONE = "phone" 
    PERSON_NAME = "person_name"
    COMPANY_NAME = "company_name"
    ADDRESS = "address"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    IP_ADDRESS = "ip_address"
    DATE_OF_BIRTH = "date_of_birth"
    GENERIC_TEXT = "generic_text"

# Schema mapping: table -> column -> data type
SCHEMA_CONFIG: Dict[str, Dict[str, PIIDataType]] = {
    "demo_contacts": {
        "first_name": PIIDataType.PERSON_NAME,
        "last_name": PIIDataType.PERSON_NAME,
        "email": PIIDataType.EMAIL,
        "phone": PIIDataType.PHONE,
    },
    "authorized_communications": {
        "business_email": PIIDataType.EMAIL,
        "personal_email": PIIDataType.EMAIL,
        "contact_phone": PIIDataType.PHONE,
        "company_name": PIIDataType.COMPANY_NAME,
    },
    "jobseekers": {
        "full_name": PIIDataType.PERSON_NAME,
        "email_address": PIIDataType.EMAIL,
        "mobile_number": PIIDataType.PHONE,
        "home_address": PIIDataType.ADDRESS,
    },
    "employers": {
        "company_name": PIIDataType.COMPANY_NAME,
        "hr_email": PIIDataType.EMAIL,
        "office_phone": PIIDataType.PHONE,
        "headquarters_address": PIIDataType.ADDRESS,
    }
}

def get_pii_type(table_name: str, column_name: str) -> PIIDataType:
    """Get PII data type for a specific table column."""
    table_config = SCHEMA_CONFIG.get(table_name, {})
    return table_config.get(column_name, PIIDataType.GENERIC_TEXT)

def get_pii_columns(table_name: str) -> List[str]:
    """Get all PII columns for a table."""
    return list(SCHEMA_CONFIG.get(table_name, {}).keys())