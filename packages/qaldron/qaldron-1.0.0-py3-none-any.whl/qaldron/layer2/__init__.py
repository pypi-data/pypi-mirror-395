"""
Layer 2: Secure Communication & Encryption

Provides secure messaging framework with quantum hash signatures,
encryption, and tamper-evident message envelopes.
"""

from qaldron.layer2.message_envelope import MessageEnvelope
from qaldron.layer2.crypto import CryptoEngine
from qaldron.layer2.entropy import EntropyManager

__all__ = [
    "MessageEnvelope",
    "CryptoEngine",
    "EntropyManager",
]
