"""
Production FastAPI Application for PII Engine
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
from .middleware import PIIService

app = FastAPI(
    title="PII Engine API",
    description="Production-grade PII processing for Employment Exchange",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PII Service
pii_service = PIIService(database_url=os.getenv('DATABASE_URL'))

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str
    mobile_number: str
    username: str
    device_id: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    device_id: Optional[str] = None

class EmployerCreate(BaseModel):
    company_name: str
    email: str
    mobile_number: str
    address_1: str

class JobseekerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_number: str

# Dependency to get user role
def get_user_role(x_user_role: str = Header(default="user")) -> str:
    return x_user_role

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pii-engine"}

# User endpoints
@app.post("/api/users")
async def create_user(user: UserCreate):
    """Create user with automatic PII processing"""
    try:
        result = await pii_service.create_user(user.dict())
        return {"status": "success", "user": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}")
async def get_user(user_id: int, user_role: str = Depends(get_user_role)):
    """Get user with role-based display"""
    try:
        result = await pii_service.get_user(user_id, user_role)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "user": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
    """Update user with PATCH support"""
    try:
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        result = await pii_service.update_user(user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "user": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Employer endpoints
@app.post("/api/employers")
async def create_employer(employer: EmployerCreate):
    """Create employer with automatic PII processing"""
    try:
        result = await pii_service.create_employer(employer.dict())
        return {"status": "success", "employer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Jobseeker endpoints
@app.post("/api/jobseekers")
async def create_jobseeker(jobseeker: JobseekerCreate):
    """Create jobseeker with automatic PII processing"""
    try:
        result = await pii_service.create_jobseeker(jobseeker.dict())
        return {"status": "success", "jobseeker": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Direct PII processing endpoints for team integration
@app.post("/api/pii/process")
async def process_pii_data(data: Dict[str, Any], table_name: str):
    """Direct PII processing endpoint"""
    try:
        processed = await pii_service.middleware.process_input(data, table_name)
        return {"status": "success", "processed_data": processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pii/display")
async def get_display_data(data: Dict[str, Any], table_name: str, display_mode: str = "masked"):
    """Get display data with specified mode"""
    try:
        display_data = await pii_service.middleware.process_output(data, table_name, display_mode)
        return {"status": "success", "display_data": display_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)