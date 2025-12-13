"""
Test Suite for Layer 1 - Quantum Hashing
"""

import pytest
from qaldron.layer1 import MarkBluHasher


class TestMarkBluHasher:
    """Test cases for MARK-BLU quantum hashing"""
    
    def test_hash_generation(self):
        """Test basic hash generation"""
        hasher = MarkBluHasher()
        hash_value = hasher.get_hash("test message")
        
        assert isinstance(hash_value, str)
        assert len(hash_value) == 32  # 16 bytes = 32 hex chars
    
    def test_hash_determinism(self):
        """Test that same input produces same hash"""
        hasher = MarkBluHasher()
        hash1 = hasher.get_hash("deterministic test")
        hash2 = hasher.get_hash("deterministic test")
        
        assert hash1 == hash2
    
    def test_hash_uniqueness(self):
        """Test that different inputs produce different hashes"""
        hasher = MarkBluHasher()
        hash1 = hasher.get_hash("message 1")
        hash2 = hasher.get_hash("message 2")
        
        assert hash1 != hash2
    
    def test_avalanche_effect(self):
        """Test that small input change causes significant hash change"""
        hasher = MarkBluHasher()
        hash1 = hasher.get_hash("test")
        hash2 = hasher.get_hash("Test")  # One bit different
        
        # Convert to binary and count differences
        bin1 = bin(int(hash1, 16))[2:].zfill(128)
        bin2 = bin(int(hash2, 16))[2:].zfill(128)
        diff_count = sum(c1 != c2 for c1, c2 in zip(bin1, bin2))
        
        # Should change ~50% of bits (64 ± 20)
        assert 44 <= diff_count <= 84
    
    def test_sign_verify(self):
        """Test signature generation and verification"""
        hasher = MarkBluHasher()
        message = "important message"
        
        signature = hasher.sign(message)
        is_valid = hasher.verify(message, signature)
        
        assert is_valid
    
    def test_verify_fails_on_wrong_message(self):
        """Test that verification fails for wrong message"""
        hasher = MarkBluHasher()
        message = "original message"
        signature = hasher.sign(message)
        
        is_valid = hasher.verify("tampered message", signature)
        
        assert not is_valid
    
    def test_different_keys_produce_different_hashes(self):
        """Test that different auth keys produce different hashes"""
        hasher1 = MarkBluHasher(auth_key=b"key1")
        hasher2 = MarkBluHasher(auth_key=b"key2")
        
        hash1 = hasher1.get_hash("same message")
        hash2 = hasher2.get_hash("same message")
        
        assert hash1 != hash2
    
    def test_bytes_and_string_input(self):
        """Test that bytes and string inputs work correctly"""
        hasher = MarkBluHasher()
        
        hash_from_string = hasher.get_hash("test")
        hash_from_bytes = hasher.get_hash(b"test")
        
        assert hash_from_string == hash_from_bytes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
