"""
Database Integration for PII Engine
"""

import os
import json
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .fabricator import fabricator_check, pseudo, unpseudo, mask, unmask, fabricator_config

class PIIDatabase:
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///pii_engine.db')
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    async def process_input_data(self, data: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Process input data before database insertion"""
        processed_data = {}
        tokens = {}
        
        # Get PII fields from schema
        grocery_markers = await fabricator_check(fabricator_config, table_name)
        pii_fields = [marker.column_name for marker in grocery_markers]
        
        for field, value in data.items():
            if field in pii_fields:
                # Apply pseudonymization for PII fields
                pseudo_val, token = await pseudo(table_name, field, str(value), "varchar")
                processed_data[field] = pseudo_val
                tokens[field] = token
            else:
                # Keep non-PII fields as-is
                processed_data[field] = value
        
        # Add token JSON for reversibility
        processed_data['token_json'] = json.dumps(tokens)
        return processed_data
    
    async def process_output_data(self, data: Dict[str, Any], table_name: str, display_mode: str = "masked") -> Dict[str, Any]:
        """Process output data for display"""
        if display_mode == "plaintext":
            return await self._get_original_data(data, table_name)
        elif display_mode == "masked":
            return await self._get_masked_data(data, table_name)
        else:  # pseudonymized
            return self._get_pseudonymized_data(data)
    
    async def _get_original_data(self, data: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Get original data using tokens"""
        result = data.copy()
        
        if 'token_json' in data:
            try:
                tokens = json.loads(data['token_json'])
                for field, token in tokens.items():
                    if field in data:
                        original_val = await unpseudo(table_name, field, data[field], "varchar", token)
                        result[field] = original_val
            except:
                pass
        
        # Remove token_json from output
        result.pop('token_json', None)
        return result
    
    async def _get_masked_data(self, data: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Get masked data for UI display"""
        result = data.copy()
        
        # Get PII fields from schema
        grocery_markers = await fabricator_check(fabricator_config, table_name)
        pii_fields = [marker.column_name for marker in grocery_markers if marker.mask]
        
        for field in pii_fields:
            if field in data:
                masked_val, _ = await mask(table_name, field, str(data[field]), "varchar")
                result[field] = masked_val
        
        # Remove token_json from output
        result.pop('token_json', None)
        return result
    
    def _get_pseudonymized_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get pseudonymized data (already in database)"""
        result = data.copy()
        result.pop('token_json', None)
        return result
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """Insert processed data into database"""
        with self.SessionLocal() as session:
            columns = ', '.join(data.keys())
            placeholders = ', '.join([f':{key}' for key in data.keys()])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            result = session.execute(text(query), data)
            session.commit()
            return result.lastrowid
    
    def select(self, table_name: str, where_clause: str = "", params: Dict = None) -> Dict[str, Any]:
        """Select data from database"""
        with self.SessionLocal() as session:
            query = f"SELECT * FROM {table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            
            result = session.execute(text(query), params or {})
            row = result.fetchone()
            
            if row:
                return dict(row._mapping)
            return {}
    
    def update(self, table_name: str, data: Dict[str, Any], where_clause: str, params: Dict = None) -> bool:
        """Update data in database"""
        with self.SessionLocal() as session:
            set_clause = ', '.join([f"{key} = :{key}" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            
            all_params = {**data, **(params or {})}
            session.execute(text(query), all_params)
            session.commit()
            return True