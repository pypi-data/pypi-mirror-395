"""
Hybrid encryption handler for client-server communication.
Handles AES+RSA decryption from clients and Fernet encryption for storage.
"""

import base64
import json
import os
from typing import Dict, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.fernet import Fernet


class HybridEncryptor:
    """Handles hybrid encryption for client-server communication."""
    
    def __init__(self):
        """Initialize with RSA key pair and Fernet key."""
        self.rsa_private_key = None
        self.rsa_public_key = None
        self.fernet_key = None
        self.fernet = None
        
        self._load_or_generate_keys()
    
    def _load_or_generate_keys(self):
        """Load existing keys or generate new ones."""
        # Load Fernet key for storage encryption
        fernet_key_env = os.environ.get('PII_ENC_KEY')
        if fernet_key_env:
            # Key is already base64 encoded string, convert to bytes
            self.fernet_key = fernet_key_env.encode('utf-8')
        else:
            self.fernet_key = Fernet.generate_key()
        
        self.fernet = Fernet(self.fernet_key)
        
        # Load or generate RSA key pair for client communication
        rsa_private_path = os.environ.get('RSA_PRIVATE_KEY_PATH', 'rsa_private.pem')
        rsa_public_path = os.environ.get('RSA_PUBLIC_KEY_PATH', 'rsa_public.pem')
        
        try:
            # Try to load existing keys
            with open(rsa_private_path, 'rb') as f:
                self.rsa_private_key = serialization.load_pem_private_key(
                    f.read(), password=None
                )
            with open(rsa_public_path, 'rb') as f:
                self.rsa_public_key = serialization.load_pem_public_key(f.read())
        except FileNotFoundError:
            # Generate new RSA key pair
            self.rsa_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self.rsa_public_key = self.rsa_private_key.public_key()
            
            # Save keys
            with open(rsa_private_path, 'wb') as f:
                f.write(self.rsa_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            with open(rsa_public_path, 'wb') as f:
                f.write(self.rsa_public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
    
    def get_public_key_pem(self) -> str:
        """Get RSA public key in PEM format for client."""
        return self.rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    def decrypt_client_data(self, encrypted_payload: Dict[str, str]) -> Dict[str, Any]:
        """
        Decrypt data received from client using hybrid encryption.
        
        Args:
            encrypted_payload: Dict containing encryptedData, encryptedKey, iv
            
        Returns:
            Decrypted PII data as dictionary
        """
        try:
            # 1. Decode base64 components
            encrypted_data = base64.b64decode(encrypted_payload['encryptedData'])
            encrypted_aes_key = base64.b64decode(encrypted_payload['encryptedKey'])
            iv = base64.b64decode(encrypted_payload['iv'])
            
            # 2. Decrypt AES key using RSA private key
            aes_key_bytes = self.rsa_private_key.decrypt(
                encrypted_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # 3. Decrypt data using AES key
            cipher = Cipher(
                algorithms.AES(aes_key_bytes),
                modes.GCM(iv)
            )
            decryptor = cipher.decryptor()
            
            # Extract authentication tag (last 16 bytes)
            ciphertext = encrypted_data[:-16]
            auth_tag = encrypted_data[-16:]
            
            decryptor.authenticate_additional_data(b'')
            plaintext = decryptor.update(ciphertext) + decryptor.finalize_with_tag(auth_tag)
            
            # 4. Parse JSON data
            pii_data = json.loads(plaintext.decode('utf-8'))
            
            return pii_data
            
        except Exception as e:
            raise ValueError(f"Failed to decrypt client data: {str(e)}")
    
    def encrypt_for_storage(self, plaintext: str) -> bytes:
        """Encrypt data for database storage using Fernet."""
        return self.fernet.encrypt(plaintext.encode('utf-8'))
    
    def decrypt_from_storage(self, encrypted_bytes: bytes) -> str:
        """Decrypt data from database storage using Fernet."""
        return self.fernet.decrypt(encrypted_bytes).decode('utf-8')
    
    def process_hybrid_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a hybrid encrypted request from client.
        
        Args:
            request_data: Request containing 'encrypted' payload and other data
            
        Returns:
            Processed data with PII decrypted and ready for tokenization
        """
        result = {}
        
        # Copy non-encrypted data
        for key, value in request_data.items():
            if key != 'encrypted':
                result[key] = value
        
        # Decrypt PII data if present
        if 'encrypted' in request_data:
            pii_data = self.decrypt_client_data(request_data['encrypted'])
            result.update(pii_data)
        
        return result


# Example usage and testing
if __name__ == "__main__":
    # Test the hybrid encryption
    encryptor = HybridEncryptor()
    
    print("RSA Public Key (for client):")
    print(encryptor.get_public_key_pem())
    
    # Test Fernet encryption for storage
    test_data = "john.smith@gmail.com"
    encrypted = encryptor.encrypt_for_storage(test_data)
    decrypted = encryptor.decrypt_from_storage(encrypted)
    
    print(f"\nFernet Test:")
    print(f"Original: {test_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")