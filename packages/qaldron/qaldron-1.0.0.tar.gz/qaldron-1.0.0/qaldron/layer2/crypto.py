"""
Cryptographic Engine for QALDRON

Provides authenticated encryption/decryption using AES-GCM with key derivation
from quantum hashes for secure message payload protection.
"""

import os
from typing import Union, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json


class CryptoEngine:
    """
    Authenticated encryption engine using AES-GCM
    
    Provides encryption and decryption with built-in integrity checking.
    Uses quantum hash for key derivation to tie encryption to QALDRON's
    quantum-inspired security layer.
    
    Args:
        quantum_hash: Base quantum hash for key derivation
        key_size: AES key size in bits (default: 256)
    """
    
    def __init__(self, quantum_hash: str = None, key_size: int = 256):
        self.key_size = key_size
        self.key_bytes = key_size // 8  # 256 bits = 32 bytes
        
        # If quantum hash provided, derive key from it
        if quantum_hash:
            self.key = self._derive_key_from_hash(quantum_hash)
        else:
            # Generate random key (for testing or standalone use)
            self.key = AESGCM.generate_key(bit_length=key_size)
        
        self.cipher = AESGCM(self.key)
    
    def _derive_key_from_hash(self, quantum_hash: str, salt: bytes = None) -> bytes:
        """
        Derive encryption key from quantum hash using PBKDF2
        
        Args:
            quantum_hash: Hex string quantum hash
            salt: Optional salt (default: fixed salt for determinism)
            
        Returns:
            bytes: Derived encryption key
        """
        # Use fixed salt for deterministic key derivation
        # In production, could use per-message salt stored with ciphertext
        if salt is None:
            salt = b"QALDRON_SALT_V1"
        
        # Convert hex hash to bytes
        hash_bytes = bytes.fromhex(quantum_hash)
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_bytes,
            salt=salt,
            iterations=100000,  # 100k iterations for security
        )
        
        return kdf.derive(hash_bytes)
    
    def encrypt(self, data: Union[str, bytes, dict]) -> str:
        """
        Encrypt data using AES-GCM authenticated encryption
        
        Args:
            data: Data to encrypt (str, bytes, or dict)
            
        Returns:
            str: Base64-encoded encrypted data with nonce
        """
        # Convert data to bytes
        if isinstance(data, dict):
            data_bytes = json.dumps(data).encode()
        elif isinstance(data, str):
            data_bytes = data.encode()
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")
        
        # Generate random nonce (12 bytes for GCM)
        nonce = os.urandom(12)
        
        # Encrypt with authenticated encryption
        ciphertext = self.cipher.encrypt(nonce, data_bytes, None)
        
        # Combine nonce + ciphertext for transport
        encrypted_package = nonce + ciphertext
        
        # Encode to base64 for JSON serialization
        return base64.b64encode(encrypted_package).decode('utf-8')
    
    def decrypt(self, encrypted_data: str) -> bytes:
        """
        Decrypt data and verify authenticity
        
        Args:
            encrypted_data: Base64-encoded encrypted package
            
        Returns:
            bytes: Decrypted plaintext data
            
        Raises:
            ValueError: If decryption fails or data is tampered
        """
        try:
            # Decode from base64
            encrypted_package = base64.b64decode(encrypted_data)
            
            # Extract nonce (first 12 bytes) and ciphertext
            nonce = encrypted_package[:12]
            ciphertext = encrypted_package[12:]
            
            # Decrypt and verify authenticity
            plaintext = self.cipher.decrypt(nonce, ciphertext, None)
            
            return plaintext
            
        except Exception as e:
            raise ValueError(f"Decryption failed (possible tampering): {e}")
    
    def decrypt_to_string(self, encrypted_data: str) -> str:
        """
        Decrypt data and return as string
        
        Args:
            encrypted_data: Base64-encoded encrypted package
            
        Returns:
            str: Decrypted string
        """
        plaintext = self.decrypt(encrypted_data)
        return plaintext.decode('utf-8')
    
    def decrypt_to_dict(self, encrypted_data: str) -> dict:
        """
        Decrypt data and parse as JSON dictionary
        
        Args:
            encrypted_data: Base64-encoded encrypted package
            
        Returns:
            dict: Decrypted dictionary
        """
        plaintext = self.decrypt(encrypted_data)
        return json.loads(plaintext.decode('utf-8'))
    
    def encrypt_with_custom_key(self, data: Union[str, bytes, dict], key: bytes) -> str:
        """
        Encrypt data with a custom key (not the instance key)
        
        Useful for per-message keys or testing.
        
        Args:
            data: Data to encrypt
            key: Custom encryption key (32 bytes for AES-256)
            
        Returns:
            str: Base64-encoded encrypted data
        """
        if len(key) != self.key_bytes:
            raise ValueError(f"Key must be {self.key_bytes} bytes for AES-{self.key_size}")
        
        cipher = AESGCM(key)
        
        # Convert data to bytes
        if isinstance(data, dict):
            data_bytes = json.dumps(data).encode()
        elif isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = data
        
        # Generate nonce and encrypt
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, data_bytes, None)
        
        # Package and encode
        encrypted_package = nonce + ciphertext
        return base64.b64encode(encrypted_package).decode('utf-8')
    
    def decrypt_with_custom_key(self, encrypted_data: str, key: bytes) -> bytes:
        """
        Decrypt data with a custom key
        
        Args:
            encrypted_data: Base64-encoded encrypted package
            key: Custom decryption key (32 bytes for AES-256)
            
        Returns:
            bytes: Decrypted plaintext
        """
        if len(key) != self.key_bytes:
            raise ValueError(f"Key must be {self.key_bytes} bytes for AES-{self.key_size}")
        
        cipher = AESGCM(key)
        
        try:
            encrypted_package = base64.b64decode(encrypted_data)
            nonce = encrypted_package[:12]
            ciphertext = encrypted_package[12:]
            return cipher.decrypt(nonce, ciphertext, None)
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    @staticmethod
    def generate_random_key(key_size: int = 256) -> bytes:
        """
        Generate a random encryption key
        
        Args:
            key_size: Key size in bits (default: 256)
            
        Returns:
            bytes: Random encryption key
        """
        return AESGCM.generate_key(bit_length=key_size)
