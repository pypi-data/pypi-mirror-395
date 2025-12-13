"""
Quantum Circuit Simulator

A custom quantum simulator supporting N-qubit systems with X, Y, Z rotations
and entanglement swap networks for quantum-inspired cryptographic operations.
"""

import numpy as np


class ChaosQuantumSim:
    """
    Chaotic Quantum Circuit Simulator
    
    Simulates quantum states and operations for cryptographic hashing purposes.
    Uses complex-valued state vectors and quantum gate operations.
    
    Args:
        n_qubits (int): Number of qubits to simulate
    """
    
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.dim = 1 << n_qubits  # 2^n_qubits
        self.state = np.zeros(self.dim, dtype=np.complex128)
        self.state[0] = 1.0  # Initialize to |0...0⟩ state
    
    def apply_rotation(self, q, theta, axis):
        """
        Apply rotation gate to a specific qubit
        
        Args:
            q (int): Qubit index to rotate
            theta (float): Rotation angle in radians
            axis (str): Rotation axis - 'X', 'Y', or 'Z'
        """
        c = np.cos(theta / 2)
        s = np.sin(theta / 2)
        shape = (1 << (self.n - q - 1), 2, 1 << q)
        state_reshaped = self.state.reshape(shape)
        new_state = np.zeros_like(state_reshaped)
        
        if axis == 'X':
            # RX gate: cos(θ/2)I - i*sin(θ/2)X
            new_state[:, 0, :] = c * state_reshaped[:, 0, :] - 1j * s * state_reshaped[:, 1, :]
            new_state[:, 1, :] = -1j * s * state_reshaped[:, 0, :] + c * state_reshaped[:, 1, :]
        elif axis == 'Y':
            # RY gate: cos(θ/2)I - i*sin(θ/2)Y
            new_state[:, 0, :] = c * state_reshaped[:, 0, :] - s * state_reshaped[:, 1, :]
            new_state[:, 1, :] = s * state_reshaped[:, 0, :] + c * state_reshaped[:, 1, :]
        elif axis == 'Z':
            # RZ gate: e^(-iθ/2)|0⟩ + e^(iθ/2)|1⟩
            phase = np.exp(-1j * theta / 2)
            new_state[:, 0, :] = state_reshaped[:, 0, :] * phase
            new_state[:, 1, :] = state_reshaped[:, 1, :] * np.conj(phase)
        
        self.state = new_state.flatten()
    
    def apply_swap_network(self):
        """
        Apply SWAP network for entanglement between adjacent qubits
        
        Creates quantum entanglement by swapping states of qubit pairs,
        implementing a butterfly network pattern for maximum mixing.
        """
        indices = np.arange(self.dim)
        for q in range(0, self.n - 1, 2):
            mask1 = 1 << q
            mask2 = 1 << (q + 1)
            diff = ((indices & mask1) == 0) != ((indices & mask2) == 0)
            to_swap = indices[diff]
            partners = to_swap ^ (mask1 | mask2)
            valid = to_swap < partners
            idx_a = to_swap[valid]
            idx_b = partners[valid]
            self.state[idx_a], self.state[idx_b] = self.state[idx_b], self.state[idx_a]
    
    def expectation_z(self, q):
        """
        Measure expectation value of Pauli-Z operator on qubit q
        
        Args:
            q (int): Qubit index to measure
            
        Returns:
            float: Expectation value in range [-1, 1]
        """
        probs = np.abs(self.state)**2
        mask = 1 << q
        prob_1 = np.sum(probs[(np.arange(self.dim) & mask) != 0])
        return 1.0 - 2.0 * prob_1
