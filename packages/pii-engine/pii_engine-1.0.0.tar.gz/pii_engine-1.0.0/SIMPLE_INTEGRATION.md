# Simple PII Integration - No Docker Required

## 🎯 **3 Simple Options (No Docker)**

### **Option 1: Standalone Python Service**

```bash
# 1. Install PII engine
pip install -e .

# 2. Set encryption key
export PII_ENC_KEY="your-generated-key"

# 3. Run proxy service
python run_pii_proxy.py
```

**Result:** PII proxy runs on port 8000, forwards to your backend on 8001

### **Option 2: Add to Existing Backend (Recommended)**

Add 3 lines to your existing API endpoints:

```python
# Add to your existing backend code
from pii_engine import PIIEngine

# Initialize once (global or dependency injection)
pii_engine = PIIEngine()

# Modify existing endpoints
@app.post("/api/users")
def create_user(user_data: dict):
    # ADD THIS LINE: Process PII before saving
    processed_data = pii_engine.process_input_data(user_data, "users")
    
    # Your existing code (use processed_data instead of user_data)
    user_id = database.save(processed_data)
    
    # ADD THIS LINE: Format for display
    display_data = pii_engine.get_display_data(processed_data, "users", "masked", "user")
    
    # Return display data instead of raw data
    return {"user": display_data}
```

### **Option 3: Nginx/Apache Module**

```nginx
# nginx.conf - Use lua script for PII processing
location /api/ {
    access_by_lua_block {
        -- Call PII processing service
        local res = ngx.location.capture("/pii-process", {
            method = ngx.HTTP_POST,
            body = ngx.var.request_body
        })
        ngx.req.set_body_data(res.body)
    }
    
    proxy_pass http://backend;
}

location /pii-process {
    proxy_pass http://pii-service:8000;
}
```

## 🚀 **Quickest Setup (5 minutes)**

### **Step 1: Install Module**
```bash
cd pii_poc
pip install -e ".[fastapi]"
```

### **Step 2: Generate Key**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# Copy the output
```

### **Step 3: Set Environment**
```bash
export PII_ENC_KEY="paste-your-key-here"
export BACKEND_URL="http://localhost:8001"  # Your backend URL
```

### **Step 4: Run Proxy**
```bash
python run_pii_proxy.py
```

### **Step 5: Update Frontend**
```javascript
// Change frontend API calls from:
const API_BASE = "http://localhost:8001";

// To:
const API_BASE = "http://localhost:8000";  // PII proxy
```

**Done!** All PII processing happens automatically.

## 🔧 **Alternative: Direct Backend Integration**

If you prefer **no separate service**, add to existing backend:

### **FastAPI Backend**
```python
from fastapi import FastAPI
from pii_engine.middleware.fastapi_middleware import PIIMiddleware

app = FastAPI()

# Add PII middleware (automatic processing)
app.add_middleware(PIIMiddleware, pii_engine=PIIEngine())

# Your existing endpoints work unchanged
@app.post("/users")
def create_user(user_data: dict):
    # PII automatically processed by middleware
    return database.save(user_data)
```

### **Flask Backend**
```python
from flask import Flask
from pii_engine.middleware.flask_middleware import PIIFlaskMiddleware

app = Flask(__name__)
PIIFlaskMiddleware(app)  # Add PII processing

# Your existing endpoints work unchanged
@app.route("/users", methods=["POST"])
def create_user():
    # PII automatically processed by middleware
    return database.save(request.json)
```

### **Any Python Backend**
```python
from pii_engine import PIIEngine

engine = PIIEngine()

def process_request(request_data):
    # Process PII in request
    processed = engine.process_input_data(request_data, "users")
    
    # Save to database (contains tokens only)
    result = database.save(processed)
    
    # Return masked data to frontend
    display = engine.get_display_data(processed, "users", "masked", "user")
    return display
```

## 📊 **Comparison**

| Option | Setup Time | Infrastructure | Backend Changes |
|--------|------------|----------------|-----------------|
| **Standalone Service** | 5 minutes | +1 Python process | None |
| **Backend Integration** | 2 minutes | None | 3 lines per endpoint |
| **Nginx Module** | 15 minutes | Nginx config | None |

## 🎯 **Recommendation**

**For quickest deployment:** Use **Standalone Service** (Option 1)
- No backend changes needed
- Easy to test and rollback
- Can be deployed on any server with Python

**For long-term:** Use **Backend Integration** (Option 2)  
- No extra infrastructure
- Better performance
- Easier to maintain

## 📞 **Support**

Choose the option that fits your infrastructure. All options provide the same security benefits:
- ✅ Zero plaintext PII in database
- ✅ Role-based data masking
- ✅ Audit logging
- ✅ GDPR/CCPA compliance