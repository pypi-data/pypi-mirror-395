#!/usr/bin/env python3
"""
CLI utilities for PII Engine
"""

from cryptography.fernet import Fernet

def generate_key():
    """Generate a new Fernet encryption key"""
    key = Fernet.generate_key()
    print(f"Generated encryption key: {key.decode()}")
    print("Set this as your PII_ENC_KEY environment variable")
    return key.decode()

if __name__ == "__main__":
    generate_key()