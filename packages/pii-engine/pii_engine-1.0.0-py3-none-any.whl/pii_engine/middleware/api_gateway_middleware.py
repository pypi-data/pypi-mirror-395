"""
API Gateway middleware for PII processing.

Intercepts all requests/responses at the gateway level for automatic PII handling.
"""

import json
from typing import Dict, Any, Optional
from ..core.engine import PIIEngine


class APIGatewayPIIProcessor:
    """PII processor for API Gateway integration."""
    
    def __init__(self, pii_engine: Optional[PIIEngine] = None):
        """Initialize with PII engine."""
        self.pii_engine = pii_engine or PIIEngine()
    
    def process_request(self, request_body: str, endpoint_config: Dict[str, Any]) -> str:
        """
        Process incoming request to tokenize PII.
        
        Args:
            request_body: JSON request body as string
            endpoint_config: Configuration for this endpoint
            
        Returns:
            Modified request body with tokenized PII
        """
        try:
            data = json.loads(request_body)
            table_name = endpoint_config.get("table_name", "default")
            
            # Process PII in request
            processed_data = self.pii_engine.process_input_data(data, table_name)
            
            return json.dumps(processed_data)
        except Exception:
            # If processing fails, return original request
            return request_body
    
    def process_response(self, response_body: str, endpoint_config: Dict[str, Any], user_context: Dict[str, Any]) -> str:
        """
        Process outgoing response to mask/pseudonymize PII.
        
        Args:
            response_body: JSON response body as string
            endpoint_config: Configuration for this endpoint
            user_context: User role and permissions
            
        Returns:
            Modified response body with appropriate PII display
        """
        try:
            data = json.loads(response_body)
            table_name = endpoint_config.get("table_name", "default")
            display_mode = user_context.get("display_mode", "masked")
            user_role = user_context.get("role", "user")
            
            # Process PII in response
            if isinstance(data, list):
                processed_data = self.pii_engine.bulk_display_records(
                    data, table_name, display_mode, user_role
                )
            elif isinstance(data, dict):
                processed_data = self.pii_engine.get_display_data(
                    data, table_name, display_mode, user_role
                )
            else:
                processed_data = data
            
            return json.dumps(processed_data)
        except Exception:
            # If processing fails, return original response
            return response_body


# Configuration example for API Gateway
ENDPOINT_CONFIG = {
    "/api/users": {
        "table_name": "users",
        "pii_fields": ["email", "phone", "name"],
        "process_requests": True,
        "process_responses": True
    },
    "/api/employees": {
        "table_name": "employees", 
        "pii_fields": ["email", "phone", "first_name", "last_name"],
        "process_requests": True,
        "process_responses": True
    }
}


def lambda_handler(event, context):
    """
    AWS Lambda function for API Gateway integration.
    
    This function processes all requests/responses through the PII engine.
    """
    processor = APIGatewayPIIProcessor()
    
    # Extract request information
    http_method = event.get("httpMethod")
    path = event.get("path")
    body = event.get("body", "{}")
    
    # Get endpoint configuration
    endpoint_config = ENDPOINT_CONFIG.get(path, {})
    
    if not endpoint_config.get("process_requests", False):
        # Skip PII processing for this endpoint
        return {
            "statusCode": 200,
            "body": body,
            "headers": {"Content-Type": "application/json"}
        }
    
    # Process request
    if http_method in ["POST", "PUT", "PATCH"]:
        processed_body = processor.process_request(body, endpoint_config)
        
        # Forward to backend API
        # backend_response = call_backend_api(path, processed_body)
        
        # For demo, return processed request
        return {
            "statusCode": 200,
            "body": processed_body,
            "headers": {"Content-Type": "application/json"}
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "PII processing complete"}),
        "headers": {"Content-Type": "application/json"}
    }