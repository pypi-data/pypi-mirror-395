"""
Kernel Module.

This module handles tensor math logic for the OPU.
"""

import numpy as np
from typing import Any

class Kernel:
    """
    Kernel for OPU tensor operations.
    """
    
    @staticmethod
    def compute_energy(J: np.ndarray, h: np.ndarray, state: np.ndarray) -> float:
        """
        Compute the energy of a given state for the Hamiltonian defined by J and h.
        
        E = -0.5 * x^T J x - h^T x
        
        Args:
            J (np.ndarray): Coupling matrix.
            h (np.ndarray): Bias vector.
            state (np.ndarray): State vector (binary or spin).
            
        Returns:
            float: The energy value.
        """
        # Ensure inputs are numpy arrays
        J = np.asarray(J)
        h = np.asarray(h)
        state = np.asarray(state)
        
        # Quadratic term: 0.5 * x^T J x
        # Note: Usually Ising model is -0.5 * ... but here we define generic quadratic form
        # Let's follow standard Ising: H = - sum J_ij s_i s_j - sum h_i s_i
        # In matrix form: E = -0.5 * s^T J s - h^T s
        
        quadratic = 0.5 * state.T @ J @ state
        linear = h.T @ state
        
        return -(quadratic + linear)
