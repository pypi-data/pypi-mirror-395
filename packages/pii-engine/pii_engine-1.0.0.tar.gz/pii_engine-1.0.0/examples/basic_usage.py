"""
Basic usage example of the PII Engine module.

This example shows how to use the PII engine in any application.
"""

from pii_engine import PIIEngine


def basic_usage_example():
    """Demonstrate basic PII engine usage."""
    
    # Initialize PII engine
    engine = PIIEngine()
    
    print("=== PII Engine Basic Usage Example ===\n")
    
    # Sample input data (what you'd receive from a form/API)
    input_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@company.com",
        "phone": "+1-555-123-4567",
        "department": "Engineering"  # Non-PII field
    }
    
    print("1. Original Input Data:")
    print(f"   {input_data}\n")
    
    # Process input data (tokenize and encrypt PII)
    processed_data = engine.process_input_data(input_data, table_name="employees")
    
    print("2. Processed Data (for database storage):")
    print(f"   {processed_data}\n")
    
    # Get display data for different user roles
    print("3. Display Data for Different Roles:")
    
    # Regular user sees masked data
    user_display = engine.get_display_data(
        processed_data, 
        table_name="employees",
        display_mode="masked",
        user_role="user"
    )
    print(f"   User Role (masked): {user_display}")
    
    # Analyst sees pseudonymized data
    analyst_display = engine.get_display_data(
        processed_data,
        table_name="employees", 
        display_mode="pseudonymized",
        user_role="analyst"
    )
    print(f"   Analyst Role (pseudonymized): {analyst_display}")
    
    # Admin sees plaintext data
    admin_display = engine.get_display_data(
        processed_data,
        table_name="employees",
        display_mode="plaintext", 
        user_role="admin"
    )
    print(f"   Admin Role (plaintext): {admin_display}\n")
    
    # Bulk processing example
    print("4. Bulk Processing Example:")
    
    bulk_data = [
        {"email": "alice@company.com", "name": "Alice Smith"},
        {"email": "bob@company.com", "name": "Bob Wilson"},
        {"email": "carol@company.com", "name": "Carol Johnson"}
    ]
    
    # Process multiple records
    bulk_processed = engine.bulk_process_records(bulk_data, table_name="employees")
    print(f"   Bulk processed: {len(bulk_processed)} records")
    
    # Display multiple records
    bulk_display = engine.bulk_display_records(
        bulk_processed,
        table_name="employees",
        display_mode="masked",
        user_role="user"
    )
    print(f"   Bulk display (first record): {bulk_display[0]}\n")
    
    # Health check
    health = engine.get_health_status()
    print("5. Engine Health Status:")
    print(f"   {health}")


def integration_example():
    """Show how to integrate with existing applications."""
    
    print("\n=== Integration Example ===\n")
    
    engine = PIIEngine()
    
    # Simulate existing application endpoint
    def create_user_endpoint(user_data):
        """Simulate a user creation endpoint."""
        
        # Step 1: Process PII before database storage
        processed_data = engine.process_input_data(user_data, table_name="users")
        
        # Step 2: Save to database (processed_data contains tokens)
        # db.save_user(processed_data)  # Your existing database code
        
        print(f"Saved to database: {processed_data}")
        
        # Step 3: Return appropriate display data
        display_data = engine.get_display_data(
            processed_data,
            table_name="users",
            display_mode="masked",  # Default for API responses
            user_role="user"
        )
        
        return {"status": "success", "user": display_data}
    
    # Test the endpoint
    user_input = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "555-987-6543"
    }
    
    result = create_user_endpoint(user_input)
    print(f"API Response: {result}")


if __name__ == "__main__":
    basic_usage_example()
    integration_example()