"""
Electrophysiology Base Module.

Defines the interface for interacting with the biological or simulated hardware.
"""

from abc import ABC, abstractmethod
from typing import List, Any
from ..biocompiler.isa import Instruction

class ElectrophysiologyDriver(ABC):
    """
    Abstract Base Class for Electrophysiology Drivers.
    """
    
    @abstractmethod
    def connect(self):
        """Establish connection to the device."""
        pass
        
    @abstractmethod
    def execute(self, instructions: List[Instruction]) -> Any:
        """
        Execute a sequence of BioASM instructions.
        
        Args:
            instructions (List[Instruction]): The instructions to execute.
            
        Returns:
            Any: The result of the execution (e.g., final state).
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close connection to the device."""
        pass
