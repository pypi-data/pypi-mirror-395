"""
Reverse Proxy middleware for PII processing.

Can be deployed as a standalone service between frontend and backend.
"""

import json
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx

from ..core.engine import PIIEngine


class PIIProxyService:
    """Standalone PII processing proxy service."""
    
    def __init__(self, backend_base_url: str, pii_engine: Optional[PIIEngine] = None):
        """
        Initialize PII proxy service.
        
        Args:
            backend_base_url: Base URL of the backend API
            pii_engine: PII engine instance
        """
        self.backend_base_url = backend_base_url.rstrip("/")
        self.pii_engine = pii_engine or PIIEngine()
        self.app = FastAPI(title="PII Proxy Service")
        self.setup_routes()
    
    def setup_routes(self):
        """Setup proxy routes."""
        
        @self.app.middleware("http")
        async def pii_processing_middleware(request: Request, call_next):
            """Process all requests through PII engine."""
            
            # Extract request info
            method = request.method
            path = request.url.path
            
            # Read request body
            body = await request.body()
            
            # Process request if it contains PII
            if method in ["POST", "PUT", "PATCH"] and body:
                try:
                    data = json.loads(body.decode())
                    table_name = self._get_table_name_from_path(path)
                    
                    # Process PII in request
                    processed_data = self.pii_engine.process_input_data(data, table_name)
                    
                    # Forward processed request to backend
                    backend_response = await self._forward_to_backend(
                        method, path, processed_data, request.headers
                    )
                    
                    # Process response PII
                    response_data = await self._process_response(
                        backend_response, table_name, request
                    )
                    
                    return JSONResponse(content=response_data)
                    
                except Exception as e:
                    # If processing fails, forward original request
                    return await self._forward_original_request(request)
            
            # For GET requests or non-PII endpoints
            return await self._forward_original_request(request)
    
    async def _forward_to_backend(self, method: str, path: str, data: Dict[str, Any], headers) -> httpx.Response:
        """Forward processed request to backend API."""
        async with httpx.AsyncClient() as client:
            url = f"{self.backend_base_url}{path}"
            
            # Filter headers (remove host, etc.)
            filtered_headers = {
                k: v for k, v in headers.items() 
                if k.lower() not in ["host", "content-length"]
            }
            
            response = await client.request(
                method=method,
                url=url,
                json=data,
                headers=filtered_headers
            )
            return response
    
    async def _forward_original_request(self, request: Request) -> Response:
        """Forward original request without PII processing."""
        async with httpx.AsyncClient() as client:
            url = f"{self.backend_base_url}{request.url.path}"
            
            # Read body
            body = await request.body()
            
            # Filter headers
            filtered_headers = {
                k: v for k, v in request.headers.items()
                if k.lower() not in ["host", "content-length"]
            }
            
            response = await client.request(
                method=request.method,
                url=url,
                content=body,
                headers=filtered_headers
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    
    async def _process_response(self, backend_response: httpx.Response, table_name: str, request: Request) -> Dict[str, Any]:
        """Process backend response for PII display."""
        try:
            response_data = backend_response.json()
            
            # Get user context (you may need to customize this)
            user_role = request.headers.get("X-User-Role", "user")
            display_mode = request.headers.get("X-Display-Mode", "masked")
            
            # Process PII in response
            if isinstance(response_data, list):
                processed_data = self.pii_engine.bulk_display_records(
                    response_data, table_name, display_mode, user_role
                )
            elif isinstance(response_data, dict):
                processed_data = self.pii_engine.get_display_data(
                    response_data, table_name, display_mode, user_role
                )
            else:
                processed_data = response_data
            
            return processed_data
            
        except Exception:
            # If processing fails, return original response
            return backend_response.json()
    
    def _get_table_name_from_path(self, path: str) -> str:
        """Extract table name from API path."""
        # Simple mapping - customize based on your API structure
        path_mapping = {
            "/api/users": "users",
            "/api/employees": "employees",
            "/api/customers": "customers",
            "/api/contacts": "contacts"
        }
        
        # Try exact match first
        if path in path_mapping:
            return path_mapping[path]
        
        # Try pattern matching
        for pattern, table in path_mapping.items():
            if path.startswith(pattern):
                return table
        
        return "default"


# Standalone service deployment
def create_pii_proxy_app(backend_url: str) -> FastAPI:
    """Create PII proxy FastAPI application."""
    proxy_service = PIIProxyService(backend_url)
    return proxy_service.app


# Example usage
if __name__ == "__main__":
    import uvicorn
    
    # Create proxy app
    app = create_pii_proxy_app("http://localhost:8001")  # Backend API URL
    
    # Run proxy service
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Proxy runs on 8000