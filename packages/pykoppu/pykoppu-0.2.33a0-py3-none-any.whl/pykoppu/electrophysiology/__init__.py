"""
Electrophysiology Package Initialization.
"""

from .base import ElectrophysiologyDriver
from .cpu import CPUDriver
from .gpu import GPUDriver
from .intan import INTANDriver
from .cloud import CLOUDDriver

from typing import Any, Optional

def connect(driver_name: str = "cpu", opu: Optional[Any] = None, **kwargs: Any) -> ElectrophysiologyDriver:
    """
    Factory function to connect to a driver.
    
    Args:
        driver_name (str): Name of the driver ("cpu", "gpu", "intan", "cloud").
        opu (OPU): The OPU instance.
        **kwargs: Arguments for the driver constructor.
        
    Returns:
        ElectrophysiologyDriver: The connected driver.
    """
    from ..opu.device import OPU
    if opu is None:
        opu = kwargs.get("opu", OPU())

    if driver_name == "cpu":
        driver = CPUDriver(opu=opu)
    elif driver_name == "gpu":
        driver = GPUDriver(opu=opu)
    elif driver_name == "intan":
        driver = INTANDriver(opu=opu)
    elif driver_name == "cloud":
        driver = CLOUDDriver(opu=opu)
    else:
        raise ValueError(f"Unknown driver: {driver_name}")
    
    driver.connect()
    return driver

__all__ = ["ElectrophysiologyDriver", "CPUDriver", "GPUDriver", "INTANDriver", "CLOUDDriver", "connect"]
