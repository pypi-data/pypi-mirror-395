"""
Flask middleware for automatic PII processing.

Provides decorators and middleware for Flask applications.
"""

import json
from functools import wraps
from typing import Dict, Any, Optional
from flask import request, jsonify, g

from ..core.engine import PIIEngine


class PIIFlaskMiddleware:
    """Flask middleware for PII processing."""
    
    def __init__(self, app=None, pii_engine: PIIEngine = None, table_name: str = "default"):
        """
        Initialize Flask PII middleware.
        
        Args:
            app: Flask application instance
            pii_engine: PII engine instance
            table_name: Default table name for PII processing
        """
        self.pii_engine = pii_engine or PIIEngine()
        self.table_name = table_name
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize middleware with Flask app."""
        app.before_request(self._before_request)
        app.after_request(self._after_request)
        
        # Store reference to middleware in app
        app.pii_middleware = self
    
    def _before_request(self):
        """Process request before handling."""
        if request.method in ['POST', 'PUT', 'PATCH'] and request.is_json:
            try:
                # Process PII in request data
                processed_data = self.pii_engine.process_input_data(
                    request.json, self.table_name
                )
                # Store processed data in g for use in route handlers
                g.pii_processed_data = processed_data
            except Exception:
                # If processing fails, continue with original data
                g.pii_processed_data = request.json
    
    def _after_request(self, response):
        """Process response after handling."""
        if response.is_json:
            try:
                user_role = self._get_user_role()
                display_mode = self._get_display_mode()
                
                data = response.get_json()
                
                if isinstance(data, list):
                    processed_data = self.pii_engine.bulk_display_records(
                        data, self.table_name, display_mode, user_role
                    )
                elif isinstance(data, dict):
                    processed_data = self.pii_engine.get_display_data(
                        data, self.table_name, display_mode, user_role
                    )
                else:
                    processed_data = data
                
                response.data = json.dumps(processed_data)
                
            except Exception:
                # If processing fails, return original response
                pass
        
        return response
    
    def _get_user_role(self) -> str:
        """Extract user role from request context."""
        # Default implementation - customize based on your auth system
        return getattr(g, 'user_role', 'user')
    
    def _get_display_mode(self) -> str:
        """Extract display mode from request."""
        return request.args.get('display_mode', 'masked')


def pii_process_input(table_name: str = "default"):
    """
    Decorator to automatically process PII in request data.
    
    Args:
        table_name: Table name for PII processing
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if hasattr(g, 'pii_processed_data'):
                # Use processed data from middleware
                return f(g.pii_processed_data, *args, **kwargs)
            else:
                # Fallback to original function
                return f(*args, **kwargs)
        return decorated_function
    return decorator


def pii_process_output(table_name: str = "default", display_mode: str = "masked"):
    """
    Decorator to automatically process PII in response data.
    
    Args:
        table_name: Table name for PII processing
        display_mode: Default display mode
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            
            try:
                # Get PII engine from app
                pii_engine = PIIEngine()
                user_role = getattr(g, 'user_role', 'user')
                mode = request.args.get('display_mode', display_mode)
                
                if isinstance(result, list):
                    processed_result = pii_engine.bulk_display_records(
                        result, table_name, mode, user_role
                    )
                elif isinstance(result, dict):
                    processed_result = pii_engine.get_display_data(
                        result, table_name, mode, user_role
                    )
                else:
                    processed_result = result
                
                return jsonify(processed_result)
                
            except Exception:
                # If processing fails, return original result
                return jsonify(result)
        
        return decorated_function
    return decorator