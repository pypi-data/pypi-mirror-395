"""
Pobit (Probabilistic Organoid Bit) Module.

This module defines the logical unit of information in the KOPPU architecture.
"""

from typing import Optional

class Pobit:
    """
    Probabilistic Organoid Bit (Pobit).
    
    Represents a stochastic binary unit implemented by neuronal ensembles.
    """
    
    def __init__(self, index: int, label: Optional[str] = None):
        """
        Initialize a Pobit.
        
        Args:
            index (int): The physical index of the pobit on the MEA.
            label (Optional[str]): A human-readable label.
        """
        self.index = index
        self.label = label if label else f"q{index}"
        
    def __repr__(self) -> str:
        return f"Pobit(index={self.index}, label='{self.label}')"
