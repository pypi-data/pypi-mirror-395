"""
Message Envelope Format

Defines the standardized message structure for secure agent communication
with quantum hash signatures and encryption.
"""

import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class MessageEnvelope:
    """
    Standardized message format for QALDRON communication
    
    All messages between agents must follow this structure to ensure
    security, authenticity, and tamper-evidence.
    
    Attributes:
        payload (dict): Actual message content
        signature (str): Quantum hash signature
        entropy (str): Quantum entropy stamp (time-based)
        timestamp (int): Unix timestamp of message creation
        sender_id (str): Unique identifier of sending agent
        receiver_id (str): Unique identifier of receiving agent
        message_id (str): Unique message identifier
        encrypted (bool): Whether payload is encrypted
    """
    
    payload: Dict[str, Any]
    signature: str
    entropy: str
    timestamp: int
    sender_id: str
    receiver_id: str
    message_id: str
    encrypted: bool = False
    
    def to_json(self) -> str:
        """Serialize envelope to JSON string"""
        return json.dumps(asdict(self))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert envelope to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MessageEnvelope':
        """Deserialize envelope from JSON string"""
        data = json.loads(json_str)
        return cls(**data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageEnvelope':
        """Create envelope from dictionary"""
        return cls(**data)
    
    @classmethod
    def create(
        cls,
        payload: Dict[str, Any],
        signature: str,
        entropy: str,
        sender_id: str,
        receiver_id: str,
        message_id: str,
        encrypted: bool = False
    ) -> 'MessageEnvelope':
        """
        Factory method to create a new message envelope
        
        Args:
            payload: Message content
            signature: Quantum hash signature
            entropy: Entropy stamp
            sender_id: Sender agent ID
            receiver_id: Receiver agent ID
            message_id: Unique message ID
            encrypted: Whether payload is encrypted
            
        Returns:
            MessageEnvelope: New message envelope instance
        """
        return cls(
            payload=payload,
            signature=signature,
            entropy=entropy,
            timestamp=int(time.time()),
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_id=message_id,
            encrypted=encrypted
        )
