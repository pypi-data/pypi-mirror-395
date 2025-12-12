"""
FastAPI integration example with PII Engine.

Shows how to integrate the PII engine with FastAPI applications.
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from pii_engine import PIIEngine
from pii_engine.middleware.fastapi_middleware import PIIMiddleware


# Pydantic models
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    department: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    department: str
    created_at: str


# Initialize FastAPI app
app = FastAPI(title="PII Engine FastAPI Example")

# Initialize PII engine
pii_engine = PIIEngine()

# Add PII middleware (optional - for automatic processing)
app.add_middleware(
    PIIMiddleware,
    pii_engine=pii_engine,
    auto_process_requests=True,
    auto_process_responses=True,
    table_name="users"
)

# Simulated database
fake_db = []
next_id = 1


def get_current_user_role() -> str:
    """Dependency to get current user role. Customize based on your auth system."""
    # In real app, this would extract role from JWT token or session
    return "user"  # Default role


@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, user_role: str = Depends(get_current_user_role)):
    """Create a new user with automatic PII processing."""
    global next_id
    
    # Convert to dict
    user_data = user.dict()
    
    # Process PII (tokenize and encrypt)
    processed_data = pii_engine.process_input_data(user_data, table_name="users")
    
    # Add metadata
    processed_data["id"] = next_id
    processed_data["created_at"] = "2024-01-01T00:00:00Z"
    next_id += 1
    
    # Save to "database"
    fake_db.append(processed_data)
    
    # Return display data based on user role
    display_data = pii_engine.get_display_data(
        processed_data,
        table_name="users",
        display_mode="masked",  # Default for API responses
        user_role=user_role
    )
    
    return display_data


@app.get("/users", response_model=List[UserResponse])
async def get_users(
    display_mode: str = "masked",
    user_role: str = Depends(get_current_user_role)
):
    """Get all users with role-based PII display."""
    
    # Get display data for all users
    display_data = pii_engine.bulk_display_records(
        fake_db,
        table_name="users",
        display_mode=display_mode,
        user_role=user_role
    )
    
    return display_data


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    display_mode: str = "masked",
    user_role: str = Depends(get_current_user_role)
):
    """Get specific user with role-based PII display."""
    
    # Find user in fake database
    user_data = None
    for user in fake_db:
        if user["id"] == user_id:
            user_data = user
            break
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get display data
    display_data = pii_engine.get_display_data(
        user_data,
        table_name="users",
        display_mode=display_mode,
        user_role=user_role
    )
    
    return display_data


@app.get("/users/search/duplicate")
async def check_duplicate_user(email: str):
    """Check for duplicate users using tokenized email."""
    
    # Create sample data to check
    check_data = {"email": email}
    
    # Get token for duplicate checking
    duplicate_token = pii_engine.check_duplicate(
        check_data,
        table_name="users",
        duplicate_fields=["email"]
    )
    
    # In real app, you'd query database with this token
    # SELECT * FROM users WHERE email_token = duplicate_token
    
    return {
        "email": email,
        "duplicate_token": duplicate_token,
        "message": "Use this token to query database for duplicates"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return pii_engine.get_health_status()


@app.get("/admin/pii-stats")
async def get_pii_stats(user_role: str = Depends(get_current_user_role)):
    """Admin endpoint to get PII processing statistics."""
    
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return {
        "total_users": len(fake_db),
        "pii_fields_processed": ["first_name", "last_name", "email", "phone"],
        "encryption_status": "active",
        "tokenization_status": "active"
    }


if __name__ == "__main__":
    print("Starting FastAPI PII Engine Example...")
    print("Visit http://localhost:8000/docs for API documentation")
    print("\nExample requests:")
    print("- POST /users - Create user (PII automatically processed)")
    print("- GET /users?display_mode=masked - Get users with masked PII")
    print("- GET /users?display_mode=pseudonymized - Get users with fake PII")
    print("- GET /users?display_mode=plaintext - Get users with real PII (admin only)")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)