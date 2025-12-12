#!/usr/bin/env python3
"""
PII Engine Key Generator

Generates secure encryption keys for PII Engine.
"""

from cryptography.fernet import Fernet


def generate_key() -> str:
    """Generate a new Fernet encryption key."""
    return Fernet.generate_key().decode("utf-8")


def main():
    """CLI entry point for key generation."""
    key = generate_key()
    print("Generated PII Engine encryption key:")
    print(key)
    print("\nAdd this to your .env file:")
    print(f"PII_ENC_KEY={key}")


if __name__ == "__main__":
    main()