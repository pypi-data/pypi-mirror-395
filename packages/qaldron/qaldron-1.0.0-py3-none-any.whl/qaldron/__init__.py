"""
QALDRON - Quantum-Assisted Ledger for Distributed Autonomous Networks

A military-grade security system for autonomous AI agents using quantum-inspired
cryptographic hashing and tamper-evident communication protocols.

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "QALDRON Team"

from qaldron.layer1 import MarkBluHasher
from qaldron.layer2 import MessageEnvelope

__all__ = [
    "MarkBluHasher",
    "MessageEnvelope",
]
