"""
API Key Authentication System

Manages client API keys, validation, and usage tracking.
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple


class APIKeyManager:
    """
    Manage client API keys for QALDRON SDK access
    
    Features:
    - Generate secure API keys
    - Validate keys
    - Track usage
    - Enforce tier limits
    """
    
    def __init__(self):
        # In production, use database instead
        self.keys: Dict[str, dict] = {}
        self.usage_logs: list = []
    
    def generate_key(
        self,
        client_id: str,
        tier: str = "free",
        company_name: str = "",
        email: str = ""
    ) ->str:
        """
        Generate new API key for client
        
        Args:
            client_id: Unique client identifier
            tier: Subscription tier (free, startup, business, enterprise)
            company_name: Client company name
            email: Client email
            
        Returns:
            str: New API key (sk-{tier}-{random})
        """
        # Generate secure random key
        random_part = secrets.token_urlsafe(32)
        tier_prefix = tier[:4]  # free, star, biz, ent
        api_key = f"sk-{tier_prefix}-{random_part}"
        
        # Hash the key for storage (never store plain text)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Store key metadata
        self.keys[key_hash] = {
            "client_id": client_id,
            "tier": tier,
            "company_name": company_name,
            "email": email,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=365)).isoformat(),
            "usage_limit": self._get_tier_limit(tier),
            "usage_count": 0,
            "active": True,
            "last_used": None
        }
        
        print(f"✓ API key generated for {client_id} ({tier} tier)")
        return api_key
    
    def validate_key(self, api_key: str) -> Tuple[bool, Optional[Dict]]:
        """
        Validate API key and return client info
        
        Args:
            api_key: API key to validate
            
        Returns:
            tuple: (is_valid, client_info or error_info)
        """
        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Check if key exists
        if key_hash not in self.keys:
            return False, {"error": "Invalid API key", "code": "INVALID_KEY"}
        
        key_info = self.keys[key_hash]
        
        # Check if active
        if not key_info["active"]:
            return False, {"error": "API key has been deactivated", "code": "KEY_DEACTIVATED"}
        
        # Check expiration
        expires_at = datetime.fromisoformat(key_info["expires_at"])
        if datetime.utcnow() > expires_at:
            return False, {"error": "API key has expired", "code": "KEY_EXPIRED"}
        
        # Check usage limits
        if key_info["usage_count"] >= key_info["usage_limit"]:
            return False, {
                "error": f"Monthly limit of {key_info['usage_limit']} messages exceeded",
                "code": "LIMIT_EXCEEDED"
            }
        
        # Valid key - increment usage
        key_info["usage_count"] += 1
        key_info["last_used"] = datetime.utcnow().isoformat()
        
        # Log usage
        self.usage_logs.append({
            "client_id": key_info["client_id"],
            "timestamp": datetime.utcnow().isoformat(),
            "action": "message_sent"
        })
        
        return True, key_info
    
    def get_client_stats(self, api_key: str) -> Optional[Dict]:
        """Get statistics for a client"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        if key_hash not in self.keys:
            return None
        
        key_info = self.keys[key_hash]
        
        return {
            "client_id": key_info["client_id"],
            "tier": key_info["tier"],
            "usage_count": key_info["usage_count"],
            "usage_limit": key_info["usage_limit"],
            "usage_percentage": (key_info["usage_count"] / key_info["usage_limit"]) * 100,
            "created_at": key_info["created_at"],
            "last_used": key_info["last_used"],
            "days_until_expiry": (
                datetime.fromisoformat(key_info["expires_at"]) - datetime.utcnow()
            ).days
        }
    
    def deactivate_key(self, api_key: str) -> bool:
        """Deactivate an API key"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        if key_hash in self.keys:
            self.keys[key_hash]["active"] = False
            return True
        return False
    
    def _get_tier_limit(self, tier: str) -> int:
        """Get monthly message limit for tier"""
        limits = {
            "free": 1000,
            "startup": 100000,
            "business": 1000000,
            "enterprise": 999999999  # Effectively unlimited
        }
        return limits.get(tier.lower(), 1000)


# Global instance
api_key_manager = APIKeyManager()


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("QALDRON API Key Manager - Demo")
    print("=" * 70)
    print()
    
    # Generate keys for different tiers
    print("📍 Generating API keys for different tiers...\n")
    
    free_key = api_key_manager.generate_key(
        "client_001",
        tier="free",
        company_name="Startup Inc",
        email="dev@startup.com"
    )
    print(f"   Free Key: {free_key[:20]}...\n")
    
    business_key = api_key_manager.generate_key(
        "client_002",
        tier="business",
        company_name="Corp Ltd",
        email="it@corp.com"
    )
    print(f"   Business Key: {business_key[:20]}...\n")
    
    # Test validation
    print("📍 Validating keys...\n")
    
    valid, info = api_key_manager.validate_key(free_key)
    print(f"   Free Key Valid: {valid}")
    if valid:
        print(f"   Client: {info['client_id']}")
        print(f"   Tier: {info['tier']}")
        print(f"   Usage: {info['usage_count']}/{info['usage_limit']}")
    print()
    
    # Test invalid key
    valid, info = api_key_manager.validate_key("sk-fake-invalid-key")
    print(f"   Invalid Key Valid: {valid}")
    print(f"   Error: {info.get('error')}")
    print()
    
    # Get stats
    print("📍 Client statistics...\n")
    stats = api_key_manager.get_client_stats(free_key)
    if stats:
        print(f"   Client ID: {stats['client_id']}")
        print(f"   Tier: {stats['tier']}")
        print(f"   Usage: {stats['usage_count']}/{stats['usage_limit']}")
        print(f"   Usage %: {stats['usage_percentage']:.1f}%")
        print(f"   Days until expiry: {stats['days_until_expiry']}")
    print()
    
    print("=" * 70)
    print("✅ API Key Manager Demo Complete!")
    print("=" * 70)
