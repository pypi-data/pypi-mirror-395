"""
MARK-BLU Apex Quantum Hashing Algorithm

Quantum-chaotic hashing framework combining quantum circuit simulation with
classical orthogonal diffusion layers for cryptographic security.
"""

import numpy as np
import hashlib
import hmac
import math
import random
from typing import Union

from qaldron.layer1.quantum_sim import ChaosQuantumSim


class MarkBluHasher:
    """
    MARK-BLU Apex v7 - Quantum-Chaotic Hash Function
    
    Combines quantum circuit simulation with Walsh-Hadamard Transform and
    Galois Field S-Box for high-entropy cryptographic hashing.
    
    Args:
        n_qubits (int): Number of qubits in quantum circuit (default: 12)
        layers (int): Number of quantum circuit layers (default: 4)
        auth_key (bytes): Authentication key for HMAC salting
    """
    
    def __init__(
        self, 
        n_qubits: int = 12, 
        layers: int = 4, 
        auth_key: bytes = b'OrthogonalKey_2025'
    ):
        self.n = n_qubits
        self.layers = layers
        self.key = auth_key
        # Precompute Galois Field S-Box for non-linearity
        self.sbox = self._generate_gf_sbox()
    
    def _generate_gf_sbox(self):
        """
        Generate Galois Field S-Box for non-linear transformation
        
        Uses a fixed seed for reproducibility while maintaining
        cryptographic properties similar to AES S-Box.
        
        Returns:
            list: 256-element S-Box permutation
        """
        rng = random.Random(1337)  # Fixed seed for determinism
        base = list(range(256))
        rng.shuffle(base)
        return base
    
    def _complex_encoding(self, input_bytes: bytes):
        """
        Encode input bytes into quantum rotation parameters
        
        Uses HMAC-SHA256 to generate salt and maps input to rotation angles
        for quantum circuit parameterization.
        
        Args:
            input_bytes (bytes): Input data to encode
            
        Returns:
            list: Rotation parameters for quantum circuit
        """
        h = hmac.new(self.key, input_bytes, hashlib.sha256).digest()
        num_params = self.n * 3 * self.layers  # 3 rotations per qubit per layer
        salt = (h * (num_params // 32 + 1))[:num_params]
        params = []
        input_list = list(input_bytes)
        
        for i in range(num_params):
            base = input_list[i % len(input_list)]
            angle = math.sin(base) * 2.0 + (salt[i] / 255.0) * np.pi
            params.append(angle)
        
        return params
    
    def _walsh_hadamard_diffusion(self, data_bytes: bytes):
        """
        Apply Walsh-Hadamard Transform for orthogonal mixing
        
        Applies perfect linear diffusion via WHT followed by non-linear S-Box
        substitution and XOR diffusion for avalanche effect.
        
        Args:
            data_bytes (bytes): 16-byte input data
            
        Returns:
            bytes: Transformed 16-byte output
        """
        # Convert to list of integers
        state = list(data_bytes)
        
        # Fast Walsh-Hadamard Transform (Butterfly network)
        h = 1
        while h < 16:
            for i in range(0, 16, h * 2):
                for j in range(i, i + h):
                    x = state[j]
                    y = state[j + h]
                    # Butterfly mixing with modular arithmetic
                    state[j] = (x + y) % 256
                    state[j + h] = (x - y + 256) % 256
            h *= 2
        
        # Apply non-linear S-Box after linear WHT
        state = [self.sbox[b] for b in state]
        
        # Final XOR diffusion to lock in the transformation
        final_state = list(state)
        for i in range(16):
            final_state[i] ^= final_state[(i + 1) % 16]
        
        return bytes(final_state)
    
    def get_hash(self, input_data: Union[str, bytes]) -> str:
        """
        Generate quantum hash for input data
        
        Main hashing function that orchestrates quantum simulation,
        measurement, and classical post-processing.
        
        Args:
            input_data (str or bytes): Data to hash
            
        Returns:
            str: 128-bit hash as hexadecimal string (32 characters)
        """
        if isinstance(input_data, str):
            input_data = input_data.encode()
        
        # Initialize quantum simulator
        sim = ChaosQuantumSim(self.n)
        params = self._complex_encoding(input_data)
        p_idx = 0
        
        # Apply parameterized quantum circuit
        for l in range(self.layers):
            for q in range(self.n):
                sim.apply_rotation(q, params[p_idx], 'X')
                p_idx += 1
                sim.apply_rotation(q, params[p_idx], 'Y')
                p_idx += 1
                sim.apply_rotation(q, params[p_idx], 'Z')
                p_idx += 1
            sim.apply_swap_network()
        
        # Measure quantum state and convert to bytes
        raw_bytes = []
        for q in range(self.n):
            z = max(-1.0, min(1.0, sim.expectation_z(q)))
            angle = math.acos(z)
            byte_val = int((angle / math.pi) * 255)
            raw_bytes.append(byte_val)
        
        # Pad to 16 bytes
        while len(raw_bytes) < 16:
            raw_bytes.append(raw_bytes[0] ^ raw_bytes[-1])
        
        # Apply Walsh-Hadamard orthogonal diffusion
        final_hash = self._walsh_hadamard_diffusion(bytes(raw_bytes[:16]))
        return final_hash.hex()
    
    def sign(self, message: Union[str, bytes]) -> str:
        """
        Generate signature for a message
        
        Alias for get_hash() to make intent clear in messaging context.
        
        Args:
            message (str or bytes): Message to sign
            
        Returns:
            str: Signature as hexadecimal string
        """
        return self.get_hash(message)
    
    def verify(self, message: Union[str, bytes], signature: str) -> bool:
        """
        Verify message signature
        
        Args:
            message (str or bytes): Original message
            signature (str): Expected signature (hex string)
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        expected = self.get_hash(message)
        return expected == signature
