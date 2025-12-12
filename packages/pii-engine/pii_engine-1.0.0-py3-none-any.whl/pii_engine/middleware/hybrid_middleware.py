"""
FastAPI middleware for handling hybrid encrypted requests.
Automatically decrypts client data and integrates with PII Engine.
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import json
from typing import Callable
from ..core.hybrid_encryptor import HybridEncryptor
from ..core.pseudo_storage_engine import PseudoStorageEngine


class HybridEncryptionMiddleware:
    """Middleware to handle hybrid encrypted requests with pseudonymized storage."""
    
    def __init__(self, app: FastAPI, pii_engine: PseudoStorageEngine = None):
        self.app = app
        self.hybrid_encryptor = HybridEncryptor()
        self.pii_engine = pii_engine or PseudoStorageEngine()
        
        # Add public key endpoint
        @app.get("/api/public-key")
        async def get_public_key():
            return {
                "publicKey": self.hybrid_encryptor.get_public_key_pem(),
                "algorithm": "RSA-OAEP-2048"
            }
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Process request through hybrid encryption middleware."""
        
        # Check if request contains encrypted data
        if (request.method in ["POST", "PUT", "PATCH"] and 
            request.headers.get("x-encryption") == "hybrid"):
            
            try:
                # Get request body
                body = await request.body()
                request_data = json.loads(body)
                
                # Decrypt hybrid encrypted data
                decrypted_data = self.hybrid_encryptor.process_hybrid_request(request_data)
                
                # Process PII data through PII Engine
                if self._contains_pii(decrypted_data):
                    # Extract table name from URL or headers
                    table_name = self._extract_table_name(request)
                    
                    # Process PII data with session ID for caching
                    session_id = request.headers.get("x-session-id", "default")
                    processed_data = self.pii_engine.process_input_data(
                        decrypted_data, table_name, session_id
                    )
                    
                    # Create new request with processed data
                    new_body = json.dumps(processed_data).encode()
                    
                    # Modify request
                    request._body = new_body
                    request.headers.__dict__["_list"].append(
                        (b"content-length", str(len(new_body)).encode())
                    )
                
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Encryption processing failed: {str(e)}"}
                )
        
        # Continue with normal request processing
        response = await call_next(request)
        
        # Process response if needed (apply display modes)
        if (hasattr(request.state, "user_role") and 
            response.headers.get("content-type", "").startswith("application/json")):
            
            response = await self._process_response(request, response)
        
        return response
    
    def _contains_pii(self, data: dict) -> bool:
        """Check if data contains PII fields."""
        pii_fields = {"email", "phone", "name", "first_name", "last_name", 
                     "address", "ssn", "credit_card", "date_of_birth"}
        return any(field in data for field in pii_fields)
    
    def _extract_table_name(self, request: Request) -> str:
        """Extract table name from request URL or headers."""
        # Try to get from header first
        table_name = request.headers.get("x-table-name")
        if table_name:
            return table_name
        
        # Extract from URL path
        path_parts = request.url.path.strip("/").split("/")
        if len(path_parts) >= 2:
            return path_parts[-1]  # Last part of path
        
        return "default_table"
    
    async def _process_response(self, request: Request, response: Response) -> Response:
        """Process response to apply display modes based on user role."""
        try:
            # Get response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            response_data = json.loads(body)
            
            # Apply display processing if response contains tokens
            if self._contains_tokens(response_data):
                user_role = getattr(request.state, "user_role", "user")
                display_mode = request.headers.get("x-display-mode", "masked")
                table_name = self._extract_table_name(request)
                
                session_id = request.headers.get("x-session-id", "default")
                display_data = self.pii_engine.get_display_data(
                    response_data, table_name, display_mode, user_role, session_id
                )
                
                # Create new response
                new_body = json.dumps(display_data).encode()
                return Response(
                    content=new_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type="application/json"
                )
        
        except Exception:
            # If processing fails, return original response
            pass
        
        return response
    
    def _contains_tokens(self, data: dict) -> bool:
        """Check if response data contains PII tokens."""
        if isinstance(data, dict):
            return any(key.endswith("_token") for key in data.keys())
        return False


# Usage example
def create_app_with_hybrid_encryption():
    """Create FastAPI app with hybrid encryption and pseudonymized storage."""
    app = FastAPI(title="PII Service with Pseudonymized Storage")
    
    # Initialize PII Engine with pseudonymized storage
    pii_engine = PseudoStorageEngine()
    
    # Add hybrid encryption middleware
    hybrid_middleware = HybridEncryptionMiddleware(app, pii_engine)
    app.middleware("http")(hybrid_middleware)
    
    @app.post("/api/users")
    async def create_user(request: Request):
        """Create user endpoint - data is automatically decrypted and processed."""
        # At this point, request body contains processed PII tokens
        body = await request.body()
        user_data = json.loads(body)
        
        # Save to database (contains tokens only)
        # database.save_user(user_data)
        
        return {"status": "success", "user_id": 123, "data": user_data}
    
    @app.get("/api/users/{user_id}")
    async def get_user(user_id: int, request: Request):
        """Get user endpoint - response is automatically processed for display."""
        # Simulate getting user tokens from database
        user_tokens = {
            "id": user_id,
            "email_token": "TKN_EMAIL_abc123",
            "phone_token": "TKN_PHONE_def456",
            "name_token": "TKN_NAME_ghi789",
            "department": "Engineering"
        }
        
        # Response will be automatically processed by middleware
        return user_tokens
    
    return app


if __name__ == "__main__":
    import uvicorn
    
    app = create_app_with_hybrid_encryption()
    uvicorn.run(app, host="0.0.0.0", port=8000)