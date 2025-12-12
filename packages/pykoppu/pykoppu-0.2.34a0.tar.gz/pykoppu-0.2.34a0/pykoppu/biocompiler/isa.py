"""
Instruction Set Architecture (ISA) Module.

This module defines the low-level instructions (BioASM) used to control the OPU.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Union

class OpCode(Enum):
    """
    BioASM Operation Codes.
    """
    ALC = auto()  # Allocate resources
    LDJ = auto()  # Load Coupling Matrix (J)
    LDH = auto()  # Load Bias Vector (h)
    SIG = auto()  # Set Noise Level (Sigma)
    RUN = auto()  # Run Simulation
    RST = auto()  # Reset State
    RD  = auto()  # Read State

@dataclass
class Instruction:
    """
    A single BioASM instruction.
    """
    opcode: OpCode
    operands: List[Union[int, float, str, list]]
    
    def __repr__(self) -> str:
        ops = ", ".join(map(str, self.operands))
        return f"{self.opcode.name} {ops}"
