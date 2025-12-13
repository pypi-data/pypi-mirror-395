"""
Secure Messenger for QALDRON

Orchestrates all Layer 2 components to provide complete secure messaging:
- Quantum hash signatures
- Time-based entropy stamps  
- AES-GCM encryption
- Replay attack prevention
- Message verification
"""

import uuid
import json
from typing import Dict, Any, Optional, Set
from datetime import datetime

from qaldron.layer1 import MarkBluHasher
from qaldron.layer2.message_envelope import MessageEnvelope
from qaldron.layer2.crypto import CryptoEngine
from qaldron.layer2.entropy import EntropyManager


class SecureMessenger:
    """
    Secure messaging system integrating all QALDRON Layer 2 components
    
    Handles the complete lifecycle of secure messages:
    - Signing with quantum hashes
    - Adding entropy stamps
    - Encrypting payloads
    - Creating message envelopes
    - Verifying incoming messages
    - Detecting replay attacks
    
    Args:
        agent_id: Unique identifier for this agent
        hasher: MarkBluHasher instance for signatures
        rotation_interval: Entropy rotation interval in seconds (default: 300)
        enable_encryption: Whether to encrypt payloads (default: True)
        replay_cache_size: Max number of message IDs to track (default: 10000)
    """
    
    def __init__(
        self,
        agent_id: str,
        hasher: Optional[MarkBluHasher] = None,
        rotation_interval: int = 300,
        enable_encryption: bool = True,
        replay_cache_size: int = 10000
    ):
        self.agent_id = agent_id
        self.hasher = hasher if hasher is not None else MarkBluHasher()
        self.rotation_interval = rotation_interval
        self.enable_encryption = enable_encryption
        self.replay_cache_size = replay_cache_size
        
        # Initialize components
        self.entropy_manager = EntropyManager(
            self.hasher,
            rotation_interval=rotation_interval
        )
        
        # Initialize crypto engine with quantum hash key
        system_crypto_key = self.hasher.get_hash("qaldron_system_encrypt_key")  # Shared key for all agents
        self.crypto_engine = CryptoEngine(quantum_hash=system_crypto_key)
        
        # Replay protection cache (set of seen message IDs)
        self.seen_message_ids: Set[str] = set()
    
    def create_message(
        self,
        payload: Dict[str, Any],
        receiver_id: str,
        message_id: Optional[str] = None,
        encrypt: Optional[bool] = None
    ) -> MessageEnvelope:
        """
        Create a secure message with signature, entropy, and optional encryption
        
        Args:
            payload: Message content (dictionary)
            receiver_id: Target agent ID
            message_id: Optional custom message ID (auto-generated if None)
            encrypt: Override encryption setting (uses instance default if None)
            
        Returns:
            MessageEnvelope: Complete secure message envelope
        """
        # Generate unique message ID if not provided
        if message_id is None:
            message_id = self.generate_message_id()
        
        # Determine encryption
        should_encrypt = encrypt if encrypt is not None else self.enable_encryption
        
        # Generate entropy stamp
        entropy_stamp = self.entropy_manager.generate_entropy_stamp()
        
        # Prepare payload for signing (include metadata)
        signing_data = {
            "payload": payload,
            "sender_id": self.agent_id,
            "receiver_id": receiver_id,
            "message_id": message_id,
            "entropy": entropy_stamp["entropy"],
            "timestamp": entropy_stamp["timestamp"]
        }
        
        # Sign the complete data
        signature = self.hasher.sign(json.dumps(signing_data, sort_keys=True))
        
        # Encrypt payload if enabled
        if should_encrypt:
            encrypted_payload = self.crypto_engine.encrypt(payload)
            final_payload = {"encrypted": encrypted_payload}
        else:
            final_payload = payload
        
        # Create message envelope
        envelope = MessageEnvelope.create(
            payload=final_payload,
            signature=signature,
            entropy=entropy_stamp["entropy"],
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_id=message_id,
            encrypted=should_encrypt
        )
        
        return envelope
    
    def verify_message(
        self,
        envelope: MessageEnvelope,
        check_replay: bool = True
    ) -> tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Verify and decrypt a received message
        
        Performs comprehensive verification:
        1. Entropy freshness check
        2. Signature verification
        3. Replay attack detection
        4. Payload decryption (if encrypted)
        
        Args:
            envelope: Message envelope to verify
            check_replay: Whether to check for replay attacks (default: True)
            
        Returns:
            tuple: (is_valid: bool, reason: str, decrypted_payload: dict or None)
        """
        # Check if message is for us
        if envelope.receiver_id != self.agent_id:
            return False, f"Message not for this agent (for {envelope.receiver_id})", None
        
        # Verify entropy freshness
        entropy_stamp = {
            "entropy": envelope.entropy,
            "timestamp": envelope.timestamp,
            "time_slot": self.entropy_manager.get_time_slot(envelope.timestamp)
        }
        is_fresh, entropy_reason = self.entropy_manager.validate_entropy_stamp(entropy_stamp)
        if not is_fresh:
            return False, f"Entropy validation failed: {entropy_reason}", None
        
        # Check for replay attack
        if check_replay:
            if envelope.message_id in self.seen_message_ids:
                return False, f"Replay attack detected (message_id {envelope.message_id} already seen)", None
        
        # Decrypt payload if encrypted
        if envelope.encrypted:
            try:
                decrypted_payload = self.crypto_engine.decrypt_to_dict(envelope.payload["encrypted"])
            except Exception as e:
                return False, f"Decryption failed: {e}", None
        else:
            decrypted_payload = envelope.payload
        
        # Reconstruct signing data for verification
        signing_data = {
            "payload": decrypted_payload,
            "sender_id": envelope.sender_id,
            "receiver_id": envelope.receiver_id,
            "message_id": envelope.message_id,
            "entropy": envelope.entropy,
            "timestamp": envelope.timestamp
        }
        
        # Verify signature
        is_valid_sig = self.hasher.verify(
            json.dumps(signing_data, sort_keys=True),
            envelope.signature
        )
        
        if not is_valid_sig:
            return False, "Invalid signature (message may be tampered)", None
        
        # Add to replay protection cache if verification passed
        if check_replay:
            self._add_to_replay_cache(envelope.message_id)
        
        return True, "Valid", decrypted_payload
    
    def send_message(
        self,
        payload: Dict[str, Any],
        receiver_id: str,
        **kwargs
    ) -> dict:
        """
        Send a secure message and return serialized envelope
        
        Args:
            payload: Message content
            receiver_id: Target agent ID
            **kwargs: Additional arguments for create_message
            
        Returns:
            dict: Serialized message envelope
        """
        envelope = self.create_message(payload, receiver_id, **kwargs)
        return envelope.to_dict()
    
    def receive_message(
        self,
        message_data: dict,
        **kwargs
    ) -> tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Receive and verify a message from serialized data
        
        Args:
            message_data: Serialized message envelope (dict)
            **kwargs: Additional arguments for verify_message
            
        Returns:
            tuple: (is_valid, reason, payload)
        """
        try:
            envelope = MessageEnvelope.from_dict(message_data)
            return self.verify_message(envelope, **kwargs)
        except Exception as e:
            return False, f"Failed to parse message: {e}", None
    
    def _add_to_replay_cache(self, message_id: str):
        """Add message ID to replay protection cache with size limit"""
        self.seen_message_ids.add(message_id)
        
        # Limit cache size (remove oldest if exceeds limit)
        if len(self.seen_message_ids) > self.replay_cache_size:
            # Remove random 10% when limit exceeded (simple eviction)
            to_remove = len(self.seen_message_ids) // 10
            for _ in range(to_remove):
                self.seen_message_ids.pop()
    
    def clear_replay_cache(self):
        """Clear replay protection cache"""
        self.seen_message_ids.clear()
    
    @staticmethod
    def generate_message_id() -> str:
        """Generate unique message ID"""
        return str(uuid.uuid4())
    
    def get_stats(self) -> dict:
        """Get messenger statistics"""
        return {
            "agent_id": self.agent_id,
            "encryption_enabled": self.enable_encryption,
            "rotation_interval": self.rotation_interval,
            "replay_cache_size": len(self.seen_message_ids),
            "current_entropy": self.entropy_manager.get_current_entropy(),
            "time_until_rotation": self.entropy_manager.get_time_until_rotation()
        }
