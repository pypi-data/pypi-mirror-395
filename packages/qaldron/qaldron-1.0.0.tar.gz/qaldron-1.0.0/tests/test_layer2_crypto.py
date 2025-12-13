"""
Test Suite for Layer 2 - Crypto Engine

Comprehensive tests for AES-GCM encryption/decryption and key derivation.
"""

import pytest
from qaldron.layer2.crypto import CryptoEngine
from qaldron.layer1 import MarkBluHasher


class TestCryptoEngine:
    """Test cases for cryptographic engine"""
    
    def test_encrypt_decrypt_string(self):
        """Test basic string encryption/decryption"""
        engine = CryptoEngine()
        plaintext = "Hello, QALDRON!"
        
        encrypted = engine.encrypt(plaintext)
        decrypted = engine.decrypt_to_string(encrypted)
        
        assert decrypted == plaintext
        assert encrypted != plaintext  # Ensure it's actually encrypted
    
    def test_encrypt_decrypt_dict(self):
        """Test dictionary encryption/decryption"""
        engine = CryptoEngine()
        data = {"action": "transfer", "amount": 1000, "to": "agent_b"}
        
        encrypted = engine.encrypt(data)
        decrypted = engine.decrypt_to_dict(encrypted)
        
        assert decrypted == data
    
    def test_encrypt_decrypt_bytes(self):
        """Test binary data encryption/decryption"""
        engine = CryptoEngine()
        data = b"\x00\x01\x02\x03\x04\xff\xfe\xfd"
        
        encrypted = engine.encrypt(data)
        decrypted = engine.decrypt(encrypted)
        
        assert decrypted == data
    
    def test_quantum_hash_key_derivation(self):
        """Test key derivation from quantum hash"""
        hasher = MarkBluHasher()
        qh = hasher.get_hash("test_key_material")
        
        engine = CryptoEngine(quantum_hash=qh)
        plaintext = "Test message"
        
        encrypted = engine.encrypt(plaintext)
        decrypted = engine.decrypt_to_string(encrypted)
        
        assert decrypted == plaintext
    
    def test_deterministic_key_derivation(self):
        """Test that same quantum hash produces same key"""
        hasher = MarkBluHasher()
        qh = hasher.get_hash("key_material")
        
        engine1 = CryptoEngine(quantum_hash=qh)
        engine2 = CryptoEngine(quantum_hash=qh)
        
        plaintext = "Determinism test"
        encrypted_by_1 = engine1.encrypt(plaintext)
        
        # Engine 2 should be able to decrypt what Engine 1 encrypted
        decrypted_by_2 = engine2.decrypt_to_string(encrypted_by_1)
        assert decrypted_by_2 == plaintext
    
    def test_tampered_ciphertext_rejection(self):
        """Test that tampered ciphertext is rejected"""
        engine = CryptoEngine()
        plaintext = "Important message"
        
        encrypted = engine.encrypt(plaintext)
        
        # Tamper with the encrypted data
        tampered = encrypted[:-10] + "XXXXXXXXXX"
        
        # Should raise ValueError on decryption
        with pytest.raises(ValueError, match="Decryption failed"):
            engine.decrypt(tampered)
    
    def test_wrong_key_rejection(self):
        """Test that wrong key cannot decrypt"""
        engine1 = CryptoEngine()
        engine2 = CryptoEngine()  # Different random key
        
        plaintext = "Secret message"
        encrypted = engine1.encrypt(plaintext)
        
        # Engine 2 with different key should fail to decrypt
        with pytest.raises(ValueError, match="Decryption failed"):
            engine2.decrypt(encrypted)
    
    def test_empty_data_handling(self):
        """Test encryption of empty data"""
        engine = CryptoEngine()
        
        # Empty string
        encrypted = engine.encrypt("")
        decrypted = engine.decrypt_to_string(encrypted)
        assert decrypted == ""
        
        # Empty bytes
        encrypted = engine.encrypt(b"")
        decrypted = engine.decrypt(encrypted)
        assert decrypted == b""
        
        # Empty dict
        encrypted = engine.encrypt({})
        decrypted = engine.decrypt_to_dict(encrypted)
        assert decrypted == {}
    
    def test_large_payload_encryption(self):
        """Test encryption of large payload (1MB)"""
        engine = CryptoEngine()
        
        # Create 1MB of data
        large_data = "A" * (1024 * 1024)
        
        encrypted = engine.encrypt(large_data)
        decrypted = engine.decrypt_to_string(encrypted)
        
        assert decrypted == large_data
        assert len(decrypted) == 1024 * 1024
    
    def test_unicode_handling(self):
        """Test encryption of unicode characters"""
        engine = CryptoEngine()
        
        unicode_text = "Hello 世界 🌍 Здравствуй مرحبا"
        
        encrypted = engine.encrypt(unicode_text)
        decrypted = engine.decrypt_to_string(encrypted)
        
        assert decrypted == unicode_text
    
    def test_special_characters_in_dict(self):
        """Test dictionary with special characters"""
        engine = CryptoEngine()
        
        data = {
            "message": "Test with \"quotes\" and 'apostrophes'",
            "symbols": "!@#$%^&*()",
            "newlines": "Line1\nLine2\nLine3"
        }
        
        encrypted = engine.encrypt(data)
        decrypted = engine.decrypt_to_dict(encrypted)
        
        assert decrypted == data
    
    def test_custom_key_encrypt_decrypt(self):
        """Test encryption with custom key"""
        engine = CryptoEngine()
        custom_key = CryptoEngine.generate_random_key(256)
        
        plaintext = "Custom key test"
        
        encrypted = engine.encrypt_with_custom_key(plaintext, custom_key)
        decrypted = engine.decrypt_with_custom_key(encrypted, custom_key)
        
        assert decrypted.decode() == plaintext
    
    def test_different_quantum_hashes_different_keys(self):
        """Test that different quantum hashes produce different keys"""
        hasher = MarkBluHasher()
        
        qh1 = hasher.get_hash("key1")
        qh2 = hasher.get_hash("key2")
        
        engine1 = CryptoEngine(quantum_hash=qh1)
        engine2 = CryptoEngine(quantum_hash=qh2)
        
        plaintext = "Test message"
        encrypted_by_1 = engine1.encrypt(plaintext)
        
        # Engine 2 should NOT be able to decrypt
        with pytest.raises(ValueError):
            engine2.decrypt(encrypted_by_1)
    
    def test_nonce_randomness(self):
        """Test that each encryption uses different nonce (different ciphertext)"""
        engine = CryptoEngine()
        plaintext = "Same message"
        
        encrypted1 = engine.encrypt(plaintext)
        encrypted2 = engine.encrypt(plaintext)
        
        # Same plaintext should produce different ciphertext (due to random nonce)
        assert encrypted1 != encrypted2
        
        # But both should decrypt to same plaintext
        assert engine.decrypt_to_string(encrypted1) == plaintext
        assert engine.decrypt_to_string(encrypted2) == plaintext


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
