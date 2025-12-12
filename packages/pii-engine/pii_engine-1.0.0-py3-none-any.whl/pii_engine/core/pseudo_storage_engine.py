"""
PII Engine with pseudonymized database storage.
Stores deterministic fake data instead of encrypted blobs.
"""

import hashlib
from typing import Dict, Any, Optional
from .tokenizer import Tokenizer
from .pseudonymizer import Pseudonymizer
from .masker import Masker
from .policy_engine import PolicyEngine


class PseudoStorageEngine:
    """PII Engine that stores pseudonymized data in database."""
    
    def __init__(self):
        """Initialize PII engine components."""
        self.tokenizer = Tokenizer()
        self.pseudonymizer = Pseudonymizer()
        self.masker = Masker()
        self.policy_engine = PolicyEngine()
        
        # In-memory cache for original PII (session-based)
        self._session_cache = {}
    
    def process_input_data(self, data: Dict[str, Any], table_name: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process input data for storage with pseudonymization.
        
        Args:
            data: Input data containing PII
            table_name: Target table name
            session_id: Optional session ID for caching original data
            
        Returns:
            Processed data with tokens and pseudonymized values
        """
        processed_data = {}
        
        for field, value in data.items():
            if self.policy_engine.is_pii_field(field):
                pii_type = self.policy_engine.get_pii_type(field)
                
                # Generate deterministic token
                token = self.tokenizer.tokenize(value, pii_type)
                
                # Generate deterministic pseudonymized value
                pseudo_value = self.pseudonymizer.pseudonymize(value, pii_type)
                
                # Store in processed data
                processed_data[f"{field}_token"] = token
                processed_data[field] = pseudo_value  # Store pseudonymized value
                
                # Cache original value for session (if admin needs it)
                if session_id:
                    cache_key = f"{session_id}:{token}"
                    self._session_cache[cache_key] = value
                    
            else:
                # Non-PII data stored as-is
                processed_data[field] = value
        
        return processed_data
    
    def get_display_data(self, stored_data: Dict[str, Any], table_name: str, 
                        display_mode: str, user_role: str, session_id: str = None) -> Dict[str, Any]:
        """
        Get display data based on user role and display mode.
        
        Args:
            stored_data: Data from database (contains tokens and pseudonymized values)
            table_name: Source table name
            display_mode: "masked", "pseudonymized", or "plaintext"
            user_role: User's role for access control
            session_id: Session ID for accessing cached original data
            
        Returns:
            Display-appropriate data
        """
        display_data = {}
        
        for field, value in stored_data.items():
            if field.endswith('_token'):
                # This is a token field, get corresponding display field
                base_field = field.replace('_token', '')
                token = value
                
                if display_mode == "plaintext" and self._can_view_plaintext(user_role):
                    # Try to get original value from session cache
                    if session_id:
                        cache_key = f"{session_id}:{token}"
                        original_value = self._session_cache.get(cache_key)
                        if original_value:
                            display_data[base_field] = original_value
                            continue
                    
                    # If not in cache, show pseudonymized (can't recover original)
                    pseudo_value = stored_data.get(base_field)
                    display_data[base_field] = pseudo_value or "***"
                    
                elif display_mode == "pseudonymized":
                    # Use stored pseudonymized value
                    pseudo_value = stored_data.get(base_field)
                    display_data[base_field] = pseudo_value or "***"
                    
                else:  # masked mode
                    # Apply masking to pseudonymized value
                    pseudo_value = stored_data.get(base_field)
                    if pseudo_value:
                        pii_type = self.policy_engine.get_pii_type_from_field(base_field)
                        display_data[base_field] = self.masker.mask(pseudo_value, pii_type)
                    else:
                        display_data[base_field] = "***"
                        
            elif not field.replace('_token', '') + '_token' in stored_data:
                # Non-PII field, copy as-is
                display_data[field] = value
        
        return display_data
    
    def _can_view_plaintext(self, user_role: str) -> bool:
        """Check if user role can view plaintext data."""
        return user_role in ["admin", "super_admin"]
    
    def clear_session_cache(self, session_id: str):
        """Clear cached original PII for a session."""
        keys_to_remove = [key for key in self._session_cache.keys() if key.startswith(f"{session_id}:")]
        for key in keys_to_remove:
            del self._session_cache[key]
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get engine health status."""
        return {
            "status": "healthy",
            "components": {
                "tokenizer": "active",
                "pseudonymizer": "active", 
                "masker": "active",
                "policy_engine": "active"
            },
            "cache_size": len(self._session_cache),
            "storage_mode": "pseudonymized"
        }


# Example usage
if __name__ == "__main__":
    # Test the pseudo storage engine
    engine = PseudoStorageEngine()
    
    # Test data
    input_data = {
        "email": "john.smith@gmail.com",
        "phone": "555-123-4567",
        "name": "John Smith",
        "department": "Engineering"  # Non-PII
    }
    
    print("=== Pseudo Storage Engine Test ===")
    print(f"Input: {input_data}")
    
    # Process for storage
    processed = engine.process_input_data(input_data, "users", session_id="session_123")
    print(f"Stored in DB: {processed}")
    
    # Get different display modes
    masked = engine.get_display_data(processed, "users", "masked", "user")
    print(f"Masked display: {masked}")
    
    pseudo = engine.get_display_data(processed, "users", "pseudonymized", "analyst")
    print(f"Pseudonymized display: {pseudo}")
    
    plaintext = engine.get_display_data(processed, "users", "plaintext", "admin", session_id="session_123")
    print(f"Admin plaintext: {plaintext}")
    
    # Clear session cache
    engine.clear_session_cache("session_123")
    print("Session cache cleared")