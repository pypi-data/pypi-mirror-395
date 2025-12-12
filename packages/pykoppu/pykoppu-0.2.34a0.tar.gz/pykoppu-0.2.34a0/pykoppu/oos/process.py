"""
OOS Process Module.

This module defines the Process class which manages the execution lifecycle.
"""

from typing import Any, Optional
import numpy as np
from ..biocompiler.compiler import BioCompiler
from ..electrophysiology import connect
from .result import SimulationResult

class Process:
    """
    Represents a computing process on the OPU.
    """
    
    def __init__(self, problem: Any, backend: str = "cpu", t: float = 1000.0):
        """
        Initialize a process.
        
        Args:
            problem: The problem instance to solve.
            backend (str): The backend driver to use. Defaults to "cpu".
            t (float): Total simulation duration in milliseconds. Defaults to 1000.0.
        """
        self.problem = problem
        self.backend = backend
        self.t = t
        self.compiler = BioCompiler()
        self.driver = connect(backend)
        
    def run(self, backend: Optional[str] = None) -> SimulationResult:
        """
        Run the process.
        
        Args:
            backend (Optional[str]): Override the backend driver for this run.
        
        Returns:
            SimulationResult: The result of the computation.
        """
        # 0. Handle Backend Override
        if backend is not None and backend != self.backend:
            self.driver.disconnect()
            self.backend = backend
            self.driver = connect(self.backend)
        # 1. Compile
        instructions = self.compiler.compile(self.problem, duration=self.t)
        
        # 2. Execute
        try:
            # Driver now returns (state, energy, spikes)
            raw_result = self.driver.execute(instructions)
            
            # Handle different return types for backward compatibility or different drivers
            if isinstance(raw_result, tuple) and len(raw_result) == 3:
                final_state, energy_trace, spike_data = raw_result
            elif isinstance(raw_result, dict) and 'state' in raw_result:
                # Legacy fallback
                final_state = raw_result['state']
                energy_trace = []
                spike_data = ([], [])
            else:
                # Fallback for unknown format
                final_state = np.array([])
                energy_trace = []
                spike_data = ([], [])
        
            # Apply problem-specific energy offset
            offset = getattr(self.problem, 'offset', 0.0)
            if len(energy_trace) > 0:
                energy_trace = np.array(energy_trace) + offset
                
                # Normalize energy to [0, 1]
                e_min = np.min(energy_trace)
                e_max = np.max(energy_trace)
                if e_max > e_min:
                    energy_trace = (energy_trace - e_min) / (e_max - e_min)
                else:
                    energy_trace = np.zeros_like(energy_trace)
                
        finally:
            self.driver.disconnect()
            
        # 3. Evaluate Metrics
        metrics = {}
        if hasattr(self.problem, 'evaluate'):
            metrics = self.problem.evaluate(final_state)
            
        # 4. Construct Result
        return SimulationResult(
            solution=final_state,
            energy_history=energy_trace,
            spikes=spike_data,
            metrics=metrics,
            metadata={"backend": self.backend}
        )
