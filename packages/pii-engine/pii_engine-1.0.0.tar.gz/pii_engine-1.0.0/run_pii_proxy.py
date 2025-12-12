#!/usr/bin/env python3
"""
Simple PII Proxy Service - No Docker Required

Run this script to start a PII processing proxy between frontend and backend.
"""

import os
import sys
import uvicorn
from pii_engine.middleware.proxy_middleware import create_pii_proxy_app

def main():
    """Start PII proxy service."""
    
    # Configuration
    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8001")
    proxy_port = int(os.environ.get("PROXY_PORT", "8000"))
    proxy_host = os.environ.get("PROXY_HOST", "0.0.0.0")
    
    # Check encryption key
    if not os.environ.get("PII_ENC_KEY"):
        print("❌ ERROR: PII_ENC_KEY environment variable not set!")
        print("Generate key: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"")
        sys.exit(1)
    
    print(f"🚀 Starting PII Proxy Service...")
    print(f"   Proxy: http://{proxy_host}:{proxy_port}")
    print(f"   Backend: {backend_url}")
    print(f"   Frontend should call proxy instead of backend")
    
    # Create and run app
    app = create_pii_proxy_app(backend_url)
    uvicorn.run(app, host=proxy_host, port=proxy_port)

if __name__ == "__main__":
    main()