"""
FastAPI middleware for automatic PII processing.

Automatically processes PII in requests and responses.
"""

import json
from typing import Callable, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ..core.engine import PIIEngine


class PIIMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for automatic PII processing."""
    
    def __init__(
        self, 
        app, 
        pii_engine: PIIEngine = None,
        auto_process_requests: bool = True,
        auto_process_responses: bool = True,
        table_name: str = "default"
    ):
        """
        Initialize PII middleware.
        
        Args:
            app: FastAPI application instance
            pii_engine: PII engine instance (creates new if None)
            auto_process_requests: Automatically process PII in requests
            auto_process_responses: Automatically process PII in responses
            table_name: Default table name for PII processing
        """
        super().__init__(app)
        self.pii_engine = pii_engine or PIIEngine()
        self.auto_process_requests = auto_process_requests
        self.auto_process_responses = auto_process_responses
        self.table_name = table_name
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and response through PII engine."""
        
        # Process request if enabled
        if self.auto_process_requests and request.method in ["POST", "PUT", "PATCH"]:
            request = await self._process_request(request)
        
        # Call the actual endpoint
        response = await call_next(request)
        
        # Process response if enabled
        if self.auto_process_responses:
            response = await self._process_response(response, request)
        
        return response
    
    async def _process_request(self, request: Request) -> Request:
        """Process PII in request body."""
        try:
            # Read request body
            body = await request.body()
            if not body:
                return request
            
            # Parse JSON
            data = json.loads(body.decode())
            
            # Process PII
            processed_data = self.pii_engine.process_input_data(data, self.table_name)
            
            # Replace request body
            new_body = json.dumps(processed_data).encode()
            request._body = new_body
            
        except (json.JSONDecodeError, Exception):
            # If processing fails, return original request
            pass
        
        return request
    
    async def _process_response(self, response: Response, request: Request) -> Response:
        """Process PII in response body."""
        try:
            # Only process JSON responses
            if not isinstance(response, JSONResponse):
                return response
            
            # Get user role from request (you may need to customize this)
            user_role = self._get_user_role(request)
            display_mode = self._get_display_mode(request)
            
            # Get response data
            response_data = response.body.decode()
            data = json.loads(response_data)
            
            # Process display data
            if isinstance(data, list):
                # Handle list of records
                processed_data = self.pii_engine.bulk_display_records(
                    data, self.table_name, display_mode, user_role
                )
            elif isinstance(data, dict):
                # Handle single record
                processed_data = self.pii_engine.get_display_data(
                    data, self.table_name, display_mode, user_role
                )
            else:
                processed_data = data
            
            # Create new response
            return JSONResponse(
                content=processed_data,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
        except (json.JSONDecodeError, Exception):
            # If processing fails, return original response
            return response
    
    def _get_user_role(self, request: Request) -> str:
        """Extract user role from request. Override this method as needed."""
        # Default implementation - customize based on your auth system
        return getattr(request.state, 'user_role', 'user')
    
    def _get_display_mode(self, request: Request) -> str:
        """Extract display mode from request. Override this method as needed."""
        # Check query parameter or header
        return request.query_params.get('display_mode', 'masked')