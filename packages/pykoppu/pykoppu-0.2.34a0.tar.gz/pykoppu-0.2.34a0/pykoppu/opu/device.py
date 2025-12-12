"""
OPU (Organoid Processing Unit) Device Module.

This module defines the physical specifications and interface for the OPU.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BioSpecs:
    """
    Physical specifications for the biological substrate.
    
    Attributes:
        R (float): Membrane resistance in Ohms.
        tau (float): Membrane time constant in seconds.
        El (float): Leak reversal potential in Volts.
        Vt (float): Threshold potential in Volts.
        Vr (float): Reset potential in Volts.
        I_offset (float): Offset current in Amperes.
        sigma (float): Noise standard deviation in Volts.
    """
    R: float
    tau: float
    El: float
    Vt: float
    Vr: float
    I_offset: float
    sigma: float

class OPU:
    """
    Organoid Processing Unit (OPU) Device Class.
    
    Represents the physical cartridge containing the organoid and MEA interface.
    """
    
    def __init__(self, model: str = "lif_critical", capacity: int = 100):
        """
        Initialize the OPU device.
        
        Args:
            model (str): The biological model to use. Defaults to "lif_critical".
            capacity (int): The number of neurons/channels available. Defaults to 100.
        """
        self.model = model
        self.capacity = capacity
        self.specs = self._load_bio_specs(model)
        
    def _load_bio_specs(self, model: str) -> BioSpecs:
        """
        Load biological specifications for the given model.
        
        Args:
            model (str): The model name.
            
        Returns:
            BioSpecs: The physical specifications.
            
        Raises:
            ValueError: If the model is unknown.
        """
        if model == "lif_critical":
            # Parameters for critical regime
            # R=50*Mohm, tau=20*ms, El=-70*mV, Vt=-50*mV, Vr=-70*mV
            # I_offset=0.36*nA, sigma=2.0*mV
            return BioSpecs(
                R=50e6,       # 50 MOhm
                tau=20e-3,    # 20 ms
                El=-70e-3,    # -70 mV
                Vt=-50e-3,    # -50 mV
                Vr=-70e-3,    # -70 mV
                I_offset=0.39e-9, # 0.39 nA (Increased for higher activity)
                sigma=2.0e-3  # 2.0 mV
            )
        else:
            raise ValueError(f"Unknown model: {model}")

    def get_specs_dict(self) -> Dict[str, Any]:
        """
        Get specifications as a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary of specifications.
        """
        return self.specs.__dict__
