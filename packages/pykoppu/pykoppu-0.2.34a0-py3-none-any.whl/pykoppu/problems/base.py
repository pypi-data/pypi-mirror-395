"""
Problem Base Module.

Defines the interface for problems solvable by KOPPU.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np

class PUBOProblem(ABC):
    """
    Polynomial Unconstrained Binary Optimization (PUBO) Problem.
    """
    
    def __init__(self):
        self.J: np.ndarray = np.array([])
        self.h: np.ndarray = np.array([])
        self.offset: float = 0.0
        
    @abstractmethod
    def to_hamiltonian(self) -> None:
        """
        Convert the problem to Hamiltonian form (J, h).
        Must be implemented by subclasses.
        """
        raise NotImplementedError
        
    def evaluate(self, solution: Any) -> Dict[str, Any]:
        """
        Evaluate the quality of a solution.
        
        Args:
            solution: The solution vector.
            
        Returns:
            Dict[str, Any]: Metrics dictionary.
        """
        # Default implementation returns empty metrics
        return {}

    @abstractmethod
    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize the solution.
        
        Args:
            result: The simulation result object.
            threshold (float): Threshold for binarizing the solution. Defaults to 0.5.
        """
        raise NotImplementedError
