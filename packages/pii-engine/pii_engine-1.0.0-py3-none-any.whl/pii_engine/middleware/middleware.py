"""
Middleware Integration for FastAPI/Flask
"""

import asyncio
from functools import wraps
from typing import Dict, Any, Callable
from ..database import PIIDatabase

class PIIMiddleware:
    def __init__(self, database_url: str = None):
        self.db = PIIDatabase(database_url)
    
    async def process_input(self, data: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Process input data before database operations"""
        return await self.db.process_input_data(data, table_name)
    
    async def process_output(self, data: Dict[str, Any], table_name: str, display_mode: str = "masked") -> Dict[str, Any]:
        """Process output data for display"""
        return await self.db.process_output_data(data, table_name, display_mode)
    
    def insert_user(self, data: Dict[str, Any]) -> int:
        """Insert user with PII processing"""
        processed_data = asyncio.run(self.process_input(data, "users"))
        return self.db.insert("users", processed_data)
    
    def get_user(self, user_id: int, display_mode: str = "masked") -> Dict[str, Any]:
        """Get user with appropriate display mode"""
        raw_data = self.db.select("users", "id = :id", {"id": user_id})
        if raw_data:
            return asyncio.run(self.process_output(raw_data, "users", display_mode))
        return {}

# Decorators for automatic PII processing
def pii_process_input(table_name: str):
    """Decorator to automatically process input data"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get data from function arguments
            if 'data' in kwargs:
                data = kwargs['data']
            elif len(args) > 0 and isinstance(args[0], dict):
                data = args[0]
            else:
                return await func(*args, **kwargs)
            
            # Process PII data
            middleware = PIIMiddleware()
            processed_data = await middleware.process_input(data, table_name)
            
            # Replace data in kwargs
            if 'data' in kwargs:
                kwargs['data'] = processed_data
            else:
                args = (processed_data,) + args[1:]
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def pii_process_output(table_name: str, display_mode: str = "masked"):
    """Decorator to automatically process output data"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get result from original function
            result = await func(*args, **kwargs)
            
            if isinstance(result, dict):
                # Process single record
                middleware = PIIMiddleware()
                return await middleware.process_output(result, table_name, display_mode)
            elif isinstance(result, list):
                # Process multiple records
                middleware = PIIMiddleware()
                processed_results = []
                for item in result:
                    if isinstance(item, dict):
                        processed_item = await middleware.process_output(item, table_name, display_mode)
                        processed_results.append(processed_item)
                    else:
                        processed_results.append(item)
                return processed_results
            
            return result
        return wrapper
    return decorator

# FastAPI Integration Example
def create_fastapi_middleware():
    """Create FastAPI middleware for automatic PII processing"""
    from fastapi import FastAPI, Request, Response
    from fastapi.middleware.base import BaseHTTPMiddleware
    
    class FastAPIPIIMiddleware(BaseHTTPMiddleware):
        def __init__(self, app: FastAPI, database_url: str = None):
            super().__init__(app)
            self.pii_middleware = PIIMiddleware(database_url)
        
        async def dispatch(self, request: Request, call_next):
            # Process request if needed
            response = await call_next(request)
            return response
    
    return FastAPIPIIMiddleware

# Usage Examples
class PIIService:
    """High-level service for team integration"""
    
    def __init__(self, database_url: str = None):
        self.middleware = PIIMiddleware(database_url)
    
    # User operations
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user with automatic PII processing"""
        processed_data = await self.middleware.process_input(user_data, "users")
        user_id = self.middleware.db.insert("users", processed_data)
        
        # Return masked data for response
        created_user = self.middleware.db.select("users", "id = :id", {"id": user_id})
        return await self.middleware.process_output(created_user, "users", "masked")
    
    async def get_user(self, user_id: int, user_role: str = "user") -> Dict[str, Any]:
        """Get user with role-based display"""
        display_mode = {
            "admin": "plaintext",
            "analyst": "pseudonymized", 
            "user": "masked"
        }.get(user_role, "masked")
        
        raw_data = self.middleware.db.select("users", "id = :id", {"id": user_id})
        if raw_data:
            return await self.middleware.process_output(raw_data, "users", display_mode)
        return {}
    
    async def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user with PATCH support"""
        # Get existing data
        existing_data = self.middleware.db.select("users", "id = :id", {"id": user_id})
        
        if existing_data:
            # Process new data
            processed_update = await self.middleware.process_input(update_data, "users")
            
            # Update database
            self.middleware.db.update("users", processed_update, "id = :id", {"id": user_id})
            
            # Return updated masked data
            updated_data = self.middleware.db.select("users", "id = :id", {"id": user_id})
            return await self.middleware.process_output(updated_data, "users", "masked")
        
        return {}
    
    # Employer operations
    async def create_employer(self, employer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create employer with automatic PII processing"""
        processed_data = await self.middleware.process_input(employer_data, "employers")
        employer_id = self.middleware.db.insert("employers", processed_data)
        
        created_employer = self.middleware.db.select("employers", "id = :id", {"id": employer_id})
        return await self.middleware.process_output(created_employer, "employers", "masked")
    
    # Jobseeker operations
    async def create_jobseeker(self, jobseeker_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create jobseeker with automatic PII processing"""
        processed_data = await self.middleware.process_input(jobseeker_data, "jobseekers")
        jobseeker_id = self.middleware.db.insert("jobseekers", processed_data)
        
        created_jobseeker = self.middleware.db.select("jobseekers", "id = :id", {"id": jobseeker_id})
        return await self.middleware.process_output(created_jobseeker, "jobseekers", "masked")