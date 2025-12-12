"""
BioCompiler Module.

This module compiles high-level problem descriptions into BioASM instructions.
"""

from typing import List, Any
from .isa import OpCode, Instruction

class BioCompiler:
    """
    Compiler for translating problems into BioASM instructions.
    """
    
    def __init__(self):
        pass
        
    def compile(self, problem: Any, strategy: str = "annealing", duration: float = 1000.0) -> List[Instruction]:
        """
        Compile a problem into a sequence of instructions.
        
        Args:
            problem: The problem instance (must have J and h attributes).
            strategy (str): The compilation strategy. Defaults to "annealing".
            duration (float): Total simulation duration in milliseconds. Defaults to 1000.0.
            
        Returns:
            List[Instruction]: The sequence of BioASM instructions.
        """
        instructions = []
        
        # 1. Allocate resources
        # Assuming problem has 'num_variables' or we infer from J
        num_vars = problem.J.shape[0]
        instructions.append(Instruction(OpCode.ALC, [num_vars]))
        
        # 2. Load Hamiltonian (J and h)
        # We pass the raw data as operands (simplified for this implementation)
        instructions.append(Instruction(OpCode.LDJ, [problem.J.tolist()]))
        instructions.append(Instruction(OpCode.LDH, [problem.h.tolist()]))
        
        # 3. Apply Strategy
        # Convert duration from ms to seconds
        total_duration_sec = duration / 1000.0
        
        if strategy == "annealing":
            # Generate SIG instructions: High -> Medium -> Low
            # Increased noise levels to promote activity and break symmetry
            noise_schedule = [10.0e-3, 5.0e-3, 2.0e-3] # 10mV, 5mV, 2mV
            
            # Divide total duration equally among steps
            step_duration = total_duration_sec / len(noise_schedule)
            
            for sigma in noise_schedule:
                instructions.append(Instruction(OpCode.SIG, [sigma]))
                instructions.append(Instruction(OpCode.RUN, [step_duration]))
                
        else:
            # Default single run
            instructions.append(Instruction(OpCode.SIG, [2.0e-3]))
            instructions.append(Instruction(OpCode.RUN, [total_duration_sec]))
            
        # 4. Read Result
        instructions.append(Instruction(OpCode.RD, []))
        
        return instructions
