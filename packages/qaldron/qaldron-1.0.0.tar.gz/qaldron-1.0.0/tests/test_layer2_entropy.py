"""
Test Suite for Layer 2 - Entropy Manager

Tests for time-based entropy generation and validation.
"""

import pytest
import time
from qaldron.layer2.entropy import EntropyManager, generate_entropy
from qaldron.layer1 import MarkBluHasher


class MockEntropyManager(EntropyManager):
    """Mock manager for testing with controllable time"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mock_time = None
    
    def get_current_time(self):
        if self.mock_time is not None:
            return self.mock_time
        return int(time.time())


class TestEntropyManager:
    """Test cases for entropy manager"""
    
    def test_entropy_generation(self):
        """Test basic entropy generation"""
        hasher = MarkBluHasher()
        manager = EntropyManager(hasher, rotation_interval=300)
        
        stamp = manager.generate_entropy_stamp()
        
        assert "entropy" in stamp
        assert "timestamp" in stamp
        assert "time_slot" in stamp
        assert isinstance(stamp["entropy"], str)
        assert len(stamp["entropy"]) == 32  # 128-bit hash = 32 hex chars
    
    def test_entropy_deterministic_within_slot(self):
        """Test that entropy is same within a time slot"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300)
        
        # Set mock time - slot 3 (900-1199)
        manager.mock_time = 900
        stamp1 = manager.generate_entropy_stamp()
        
        # Same time slot (still within 900-1199)
        manager.mock_time = 1100
        stamp2 = manager.generate_entropy_stamp()
        
        # Should have same entropy (same time slot)
        assert stamp1["entropy"] == stamp2["entropy"]
        assert stamp1["time_slot"] == stamp2["time_slot"]
    
    def test_entropy_changes_after_rotation(self):
        """Test that entropy changes after rotation interval"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300)
        
        # Time slot 1
        manager.mock_time = 1000
        stamp1 = manager.generate_entropy_stamp()
        
        # Time slot 2 (after 300s)
        manager.mock_time = 1301
        stamp2 = manager.generate_entropy_stamp()
        
        # Should have different entropy (different time slot)
        assert stamp1["entropy"] != stamp2["entropy"]
        assert stamp1["time_slot"] != stamp2["time_slot"]
    
    def test_validate_valid_entropy(self):
        """Test validation of valid entropy stamp"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300, max_age=300)
        
        # Generate entropy at T=1000
        manager.mock_time = 1000
        stamp = manager.generate_entropy_stamp()
        
        # Validate at T=1100 (100s later, still valid)
        manager.mock_time = 1100
        is_valid, reason = manager.validate_entropy_stamp(stamp)
        
        assert is_valid
        assert reason == "Valid"
    
    def test_reject_old_entropy(self):
        """Test rejection of expired entropy"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300, max_age=300)
        
        # Generate entropy at T=1000
        manager.mock_time = 1000
        stamp = manager.generate_entropy_stamp()
        
        # Validate at T=1400 (400s later, expired)
        manager.mock_time = 1400
        is_valid, reason = manager.validate_entropy_stamp(stamp)
        
        assert not is_valid
        assert "too old" in reason.lower()
    
    def test_reject_future_entropy(self):
        """Test rejection of entropy from future (clock skew)"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300, clock_tolerance=60)
        
        # Generate entropy at T=2000
        manager.mock_time = 2000
        stamp = manager.generate_entropy_stamp()
        
        # Validate at T=1000 (stamp is 1000s in future, beyond tolerance)
        manager.mock_time = 1000
        is_valid, reason = manager.validate_entropy_stamp(stamp)
        
        assert not is_valid
        assert "future" in reason.lower()
    
    def test_clock_skew_tolerance(self):
        """Test that small clock skew is tolerated"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300, clock_tolerance=60)
        
        # Generate entropy at T=1050
        manager.mock_time = 1050
        stamp = manager.generate_entropy_stamp()
        
        # Validate at T=1000 (50s behind, within 60s tolerance)
        manager.mock_time = 1000
        is_valid, reason = manager.validate_entropy_stamp(stamp)
        
        assert is_valid
        assert reason == "Valid"
    
    def test_reject_tampered_entropy(self):
        """Test rejection of tampered entropy value"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300)
        
        manager.mock_time = 1000
        stamp = manager.generate_entropy_stamp()
        
        # Tamper with entropy
        stamp["entropy"] = "0" * 32  # Wrong hash
        
        is_valid, reason = manager.validate_entropy_stamp(stamp)
        
        assert not is_valid
        assert "does not match" in reason.lower()
    
    def test_reject_invalid_time_slot(self):
        """Test rejection of mismatched time slot"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300)
        
        manager.mock_time = 1000
        stamp = manager.generate_entropy_stamp()
        
        # Tamper with time slot
        stamp["time_slot"] = 999
        
        is_valid, reason = manager.validate_entropy_stamp(stamp)
        
        assert not is_valid
        assert "time slot" in reason.lower()
    
    def test_get_entropy_age(self):
        """Test entropy age calculation"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300)
        
        manager.mock_time = 1000
        stamp = manager.generate_entropy_stamp()
        
        manager.mock_time = 1150
        age = manager.get_entropy_age(stamp)
        
        assert age == 150
    
    def test_time_until_rotation(self):
        """Test calculation of time until next rotation"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300)
        
        # At T=1050, time slot=3 (0-299, 300-599, 600-899, 900-1199)
        # Next slot starts at 1200
        manager.mock_time = 1050
        time_left = manager.get_time_until_rotation()
        
        assert time_left == 150  # 1200 - 1050
    
    def test_is_entropy_fresh(self):
        """Test quick freshness check"""
        hasher = MarkBluHasher()
        manager = MockEntropyManager(hasher, rotation_interval=300, max_age=300)
        
        manager.mock_time = 1000
        stamp = manager.generate_entropy_stamp()
        
        # Fresh (100s old)
        manager.mock_time = 1100
        assert manager.is_entropy_fresh(stamp) is True
        
        # Expired (400s old)
        manager.mock_time = 1400
        assert manager.is_entropy_fresh(stamp) is False
    
    def test_get_current_entropy(self):
        """Test convenience method for current entropy"""
        hasher = MarkBluHasher()
        manager = EntropyManager(hasher, rotation_interval=300)
        
        entropy = manager.get_current_entropy()
        
        assert isinstance(entropy, str)
        assert len(entropy) == 32
    
    def test_convenience_function(self):
        """Test generate_entropy convenience function"""
        hasher = MarkBluHasher()
        stamp = generate_entropy(hasher, rotation_interval=300)
        
        assert "entropy" in stamp
        assert "timestamp" in stamp
        assert "time_slot" in stamp
    
    def test_missing_entropy_fields(self):
        """Test validation with missing fields"""
        hasher = MarkBluHasher()
        manager = EntropyManager(hasher, rotation_interval=300)
        
        # Missing entropy field
        stamp = {"timestamp": 1000, "time_slot": 3}
        is_valid, reason = manager.validate_entropy_stamp(stamp)
        assert not is_valid
        assert "missing" in reason.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
