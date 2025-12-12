#!/usr/bin/env python3
"""
Fabricator - Production PII Engine Core
"""

import hashlib
import json
import os
from typing import List, Dict, Tuple, Optional
from faker import Faker
from cryptography.fernet import Fernet
import base64

fake = Faker()
ENCRYPTION_KEY = os.getenv('PII_ENC_KEY', Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

# Schema Definition
FABRICATOR = {
    "database": {
        "table_schema": {
            "users": [
                {"name": "id", "type": "bigint", "M": False, "P": False},
                {"name": "email", "type": "varchar(100)", "M": True, "P": True},
                {"name": "password", "type": "varchar(255)", "M": True, "P": True},
                {"name": "mobile_number", "type": "varchar(15)", "M": True, "P": True},
                {"name": "device_id", "type": "varchar(50)", "M": True, "P": True},
                {"name": "parent_email", "type": "varchar(100)", "M": True, "P": True},
                {"name": "account_no", "type": "varchar(20)", "M": True, "P": True},
                {"name": "tag_id", "type": "varchar(30)", "M": True, "P": True},
                {"name": "created_at", "type": "timestamp", "M": False, "P": False},
                {"name": "updated_at", "type": "timestamp", "M": False, "P": False},
                {"name": "username", "type": "varchar(255)", "M": False, "P": False},
                {"name": "user_status", "type": "enum('T','P','A','I')", "M": False, "P": False}
            ],
            "employers": [
                {"name": "id", "type": "bigint", "M": False, "P": False},
                {"name": "company_name", "type": "varchar(255)", "M": True, "P": True},
                {"name": "email", "type": "varchar(150)", "M": True, "P": True},
                {"name": "mobile_number", "type": "varchar(20)", "M": True, "P": True},
                {"name": "address_1", "type": "varchar(255)", "M": True, "P": True},
                {"name": "created_at", "type": "timestamp", "M": False, "P": False}
            ],
            "jobseekers": [
                {"name": "id", "type": "int", "M": False, "P": False},
                {"name": "first_name", "type": "varchar(100)", "M": True, "P": True},
                {"name": "last_name", "type": "varchar(100)", "M": True, "P": True},
                {"name": "email", "type": "varchar(150)", "M": True, "P": True},
                {"name": "mobile_number", "type": "varchar(20)", "M": True, "P": True},
                {"name": "created_at", "type": "timestamp", "M": False, "P": False}
            ]
        }
    }
}

fabricator_config = {
    "product_name": {
        "employment_exchange": [
            {"fabricator_name": "EMPLOYMENT_EXCHANGE_FABRICATOR", "token_size": "10", "prefix": "EE"}
        ]
    }
}

class GroceryMarker:
    def __init__(self, table_name: str, column_name: str, data_type: str, mask: bool, pseudo: bool):
        self.table_name = table_name
        self.column_name = column_name
        self.data_type = data_type
        self.mask = mask
        self.pseudo = pseudo

TOKEN_STORAGE = {}
PSEUDO_STORAGE = {}
ENCRYPTED_STORAGE = {}

async def mask(table_name: str, column_name: str, column_value: str, data_type: str) -> Tuple[str, str]:
    if not column_value:
        return column_value, ""
    
    config = fabricator_config["product_name"]["employment_exchange"][0]
    token_size = int(config["token_size"])
    prefix = config["prefix"]
    
    token_key = f"{table_name}_{column_name}_{column_value}"
    token_hash = hashlib.sha256(token_key.encode()).hexdigest()[:token_size]
    m_token = f"{prefix}{token_hash}"
    
    TOKEN_STORAGE[m_token] = column_value
    
    if "email" in column_name.lower() or "@" in str(column_value):
        parts = str(column_value).split("@")
        if len(parts) == 2:
            masked_val = f"{parts[0][0]}***@{parts[1][0]}***.{parts[1].split('.')[-1]}"
        else:
            masked_val = f"{str(column_value)[:2]}***"
    elif "phone" in column_name.lower() or "mobile" in column_name.lower():
        masked_val = f"******{str(column_value)[-4:]}"
    elif "name" in column_name.lower():
        masked_val = f"{str(column_value)[0]}***"
    else:
        masked_val = f"{str(column_value)[:2]}***"
    
    return masked_val, m_token

async def unmask(table_name: str, column_name: str, column_value: str, data_type: str, m_token: str) -> str:
    return TOKEN_STORAGE.get(m_token, column_value)

async def pseudo(table_name: str, column_name: str, column_value: str, data_type: str) -> Tuple[str, str]:
    if not column_value:
        return column_value, ""
    
    config = fabricator_config["product_name"]["employment_exchange"][0]
    token_size = int(config["token_size"])
    prefix = config["prefix"]
    
    token_key = f"{table_name}_{column_name}_{column_value}"
    token_hash = hashlib.sha256(token_key.encode()).hexdigest()[:token_size]
    pseudo_token = f"{prefix}{token_hash}"
    
    PSEUDO_STORAGE[pseudo_token] = column_value
    
    if "email" in column_name.lower():
        pseudo_val = fake.email()
    elif "phone" in column_name.lower() or "mobile" in column_name.lower():
        pseudo_val = fake.phone_number()
    elif "first_name" in column_name.lower():
        pseudo_val = fake.first_name()
    elif "last_name" in column_name.lower():
        pseudo_val = fake.last_name()
    elif "company" in column_name.lower():
        pseudo_val = fake.company()
    elif "address" in column_name.lower():
        pseudo_val = fake.address()
    else:
        pseudo_val = fake.word()
    
    return str(pseudo_val), pseudo_token

async def unpseudo(table_name: str, column_name: str, column_value: str, data_type: str, pseudo_token: str) -> str:
    return PSEUDO_STORAGE.get(pseudo_token, column_value)

async def encrypt(table_name: str, column_name: str, column_value: str, data_type: str) -> Tuple[str, str]:
    if not column_value:
        return column_value, ""
    
    config = fabricator_config["product_name"]["employment_exchange"][0]
    token_size = int(config["token_size"])
    prefix = config["prefix"]
    
    token_key = f"{table_name}_{column_name}_{column_value}"
    token_hash = hashlib.sha256(token_key.encode()).hexdigest()[:token_size]
    enc_token = f"{prefix}{token_hash}"
    
    encrypted_bytes = fernet.encrypt(str(column_value).encode())
    encrypted_value = base64.b64encode(encrypted_bytes).decode()
    
    ENCRYPTED_STORAGE[enc_token] = encrypted_value
    return encrypted_value, enc_token

async def decrypt(table_name: str, column_name: str, encrypted_value: str, data_type: str, enc_token: str) -> str:
    if not encrypted_value or not enc_token:
        return encrypted_value
    
    try:
        stored_encrypted = ENCRYPTED_STORAGE.get(enc_token, encrypted_value)
        encrypted_bytes = base64.b64decode(stored_encrypted.encode())
        decrypted_bytes = fernet.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()
    except Exception:
        return encrypted_value

async def fabricator_check(fabricator_config: Dict, table_name: str) -> List[GroceryMarker]:
    grocery_markers = []
    schema = FABRICATOR["database"]["table_schema"].get(table_name, [])
    
    for column in schema:
        if column.get("M") or column.get("P"):
            marker = GroceryMarker(
                table_name, column["name"], column["type"],
                column.get("M", False), column.get("P", False)
            )
            grocery_markers.append(marker)
    
    return grocery_markers

async def update_token_set(existing_token_json: str, new_data: Dict, table_name: str) -> str:
    try:
        existing_tokens = json.loads(existing_token_json) if existing_token_json else {}
    except:
        existing_tokens = {}
    
    grocery_markers = await fabricator_check(fabricator_config, table_name)
    pii_fields = [marker.column_name for marker in grocery_markers]
    
    for field, value in new_data.items():
        if field in pii_fields:
            _, token = await pseudo(table_name, field, value, "varchar")
            existing_tokens[field] = token
    
    return json.dumps(existing_tokens)