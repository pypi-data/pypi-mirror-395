"""
Time-Based Entropy Generation for QALDRON

Generates deterministic entropy stamps based on time slots to prevent
replay attacks while maintaining verifiability within the time window.
"""

import time
from typing import Optional
from qaldron.layer1 import MarkBluHasher


class EntropyManager:
    """
    Manages time-based entropy generation for replay attack prevention
    
    Generates deterministic entropy stamps that change every rotation interval.
    Messages with entropy stamps older than max_age are rejected.
    
    Args:
        hasher: MarkBluHasher instance for entropy generation
        rotation_interval: Seconds between entropy rotations (default: 300 = 5 min)
        max_age: Maximum age of entropy stamps to accept (default: rotation_interval)
        clock_tolerance: Tolerance for clock skew in seconds (default: 60)
    """
    
    def __init__(
        self,
        hasher: MarkBluHasher,
        rotation_interval: int = 300,
        max_age: Optional[int] = None,
        clock_tolerance: int = 60
    ):
        self.hasher = hasher
        self.rotation_interval = rotation_interval
        self.max_age = max_age if max_age is not None else rotation_interval
        self.clock_tolerance = clock_tolerance
    
    def get_current_time(self) -> int:
        """Get current Unix timestamp (can be overridden for testing)"""
        return int(time.time())
    
    def get_time_slot(self, timestamp: Optional[int] = None) -> int:
        """
        Calculate time slot for a given timestamp
        
        Args:
            timestamp: Unix timestamp (default: current time)
            
        Returns:
            int: Time slot number
        """
        if timestamp is None:
            timestamp = self.get_current_time()
        
        return timestamp // self.rotation_interval
    
    def generate_entropy_stamp(self, timestamp: Optional[int] = None) -> dict:
        """
        Generate entropy stamp for current or given time
        
        Args:
            timestamp: Unix timestamp (default: current time)
            
        Returns:
            dict: Entropy stamp with {entropy, timestamp, time_slot}
        """
        if timestamp is None:
            timestamp = self.get_current_time()
        
        time_slot = self.get_time_slot(timestamp)
        
        # Generate deterministic entropy for this time slot
        entropy_seed = f"entropy_slot_{time_slot}"
        entropy = self.hasher.get_hash(entropy_seed)
        
        return {
            "entropy": entropy,
            "timestamp": timestamp,
            "time_slot": time_slot
        }
    
    def validate_entropy_stamp(
        self,
        entropy_stamp: dict,
        current_time: Optional[int] = None
    ) -> tuple[bool, str]:
        """
        Validate an entropy stamp
        
        Checks:
        1. Entropy matches the time slot
        2. Timestamp is not too old
        3. Timestamp is not in the future (within tolerance)
        
        Args:
            entropy_stamp: Entropy stamp dict from message
            current_time: Current time for validation (default: now)
            
        Returns:
            tuple: (is_valid: bool, reason: str)
        """
        if current_time is None:
            current_time = self.get_current_time()
        
        # Extract entropy info
        entropy = entropy_stamp.get("entropy")
        timestamp = entropy_stamp.get("timestamp")
        time_slot = entropy_stamp.get("time_slot")
        
        # Validate required fields
        if not all([entropy, timestamp is not None, time_slot is not None]):
            return False, "Missing required entropy fields"
        
        # Check if timestamp is too old
        age = current_time - timestamp
        if age > self.max_age:
            return False, f"Entropy too old ({age}s > {self.max_age}s max)"
        
        # Check if timestamp is too far in the future (clock skew)
        if timestamp > current_time + self.clock_tolerance:
            future_diff = timestamp - current_time
            return False, f"Entropy from future ({future_diff}s ahead, max {self.clock_tolerance}s)"
        
        # Validate time slot calculation
        expected_slot = self.get_time_slot(timestamp)
        if time_slot != expected_slot:
            return False, f"Invalid time slot (got {time_slot}, expected {expected_slot})"
        
        # Regenerate entropy for this time slot and verify
        expected_entropy_seed = f"entropy_slot_{time_slot}"
        expected_entropy = self.hasher.get_hash(expected_entropy_seed)
        
        if entropy != expected_entropy:
            return False, "Entropy does not match time slot"
        
        return True, "Valid"
    
    def is_entropy_fresh(
        self,
        entropy_stamp: dict,
        current_time: Optional[int] = None
    ) -> bool:
        """
        Quick check if entropy stamp is fresh (not expired)
        
        Args:
            entropy_stamp: Entropy stamp to check
            current_time: Current time (default: now)
            
        Returns:
            bool: True if fresh, False if expired
        """
        is_valid, _ = self.validate_entropy_stamp(entropy_stamp, current_time)
        return is_valid
    
    def get_entropy_age(self, entropy_stamp: dict, current_time: Optional[int] = None) -> int:
        """
        Get age of entropy stamp in seconds
        
        Args:
            entropy_stamp: Entropy stamp from message
            current_time: Current time (default: now)
            
        Returns:
            int: Age in seconds
        """
        if current_time is None:
            current_time = self.get_current_time()
        
        timestamp = entropy_stamp.get("timestamp", 0)
        return current_time - timestamp
    
    def get_time_until_rotation(self, current_time: Optional[int] = None) -> int:
        """
        Get seconds until next entropy rotation
        
        Args:
            current_time: Current time (default: now)
            
        Returns:
            int: Seconds until next rotation
        """
        if current_time is None:
            current_time = self.get_current_time()
        
        current_slot = self.get_time_slot(current_time)
        next_slot_start = (current_slot + 1) * self.rotation_interval
        
        return next_slot_start - current_time
    
    def get_current_entropy(self) -> str:
        """
        Get current entropy value (shorthand)
        
        Returns:
            str: Current entropy hash
        """
        stamp = self.generate_entropy_stamp()
        return stamp["entropy"]


# Convenience function for quick entropy generation
def generate_entropy(
    hasher: MarkBluHasher,
    rotation_interval: int = 300
) -> dict:
    """
    Quick helper to generate entropy stamp
    
    Args:
        hasher: MarkBluHasher instance
        rotation_interval: Rotation interval in seconds
        
    Returns:
        dict: Entropy stamp
    """
    manager = EntropyManager(hasher, rotation_interval)
    return manager.generate_entropy_stamp()
