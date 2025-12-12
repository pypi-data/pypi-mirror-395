"""
Result Module.

This module defines the SimulationResult class for rich telemetry and visualization.
"""

import numpy as np
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

class SimulationResult:
    """
    Rich result object for KOPPU simulations.
    
    Attributes:
        solution (np.ndarray): The final state vector.
        energy_history (np.ndarray): The energy evolution over time.
        spikes (Tuple[np.ndarray, np.ndarray]): Tuple of (spike_times, neuron_indices).
        metrics (Dict[str, Any]): Evaluation metrics (validity, etc.).
        metadata (Dict[str, Any]): Simulation metadata.
    """
    
    def __init__(
        self,
        solution: np.ndarray,
        energy_history: List[float],
        spikes: Tuple[np.ndarray, np.ndarray],
        metrics: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.solution = np.array(solution)
        self.energy_history = np.array(energy_history)
        self.spikes = spikes
        self.metrics = metrics or {}
        self.metadata = metadata or {}
        
    def plot(self):
        """
        Generate a 3-panel visualization of the simulation.
        
        1. Temporal Evolution (Raster Plot)
        2. Final State (Heatmap/Bar)
        3. System Energy (Time Series)
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=False)
        
        # 1. Raster Plot
        spike_times, neuron_indices = self.spikes
        if len(spike_times) > 0:
            axes[0].scatter(spike_times, neuron_indices, s=2, c='black', alpha=0.6)
            axes[0].set_ylabel("Neuron Index")
            axes[0].set_title("Temporal Evolution (Spike Raster)")
        else:
            axes[0].text(0.5, 0.5, "No Spikes Recorded", ha='center', va='center')
            
        # 2. Final State
        # Visualize as a bar chart or heatmap depending on size
        n = len(self.solution)
        if n <= 50:
            sns.barplot(x=list(range(n)), y=self.solution, hue=list(range(n)), ax=axes[1], palette="viridis", legend=False)
            axes[1].set_ylabel("Excitability Probability")
            axes[1].set_xlabel("Neuron Index")
            axes[1].set_title("Final State")
        else:
            sns.heatmap(self.solution.reshape(1, -1), ax=axes[1], cmap="viridis", cbar=True)
            axes[1].set_title("Final State (Heatmap)")
            axes[1].set_yticks([])
            
        # 3. System Energy
        if len(self.energy_history) > 0:
            # Plot Energy Trace
            axes[2].plot(self.energy_history, color='red', linewidth=1.5, label='Energy Trace')
            
            # Calculate Statistics
            e_max = np.max(self.energy_history)
            e_min = np.min(self.energy_history)
            e_mean = np.mean(self.energy_history)
            e_final = self.energy_history[-1]
            
            # Linear Regression
            x = np.arange(len(self.energy_history))
            y = self.energy_history
            slope, intercept = np.polyfit(x, y, 1)
            trend_line = slope * x + intercept
            
            # Plot Trend Line
            axes[2].plot(x, trend_line, color='blue', linestyle='--', linewidth=1.5, label=f'Trend (slope={slope:.2e})')
            
            # Display Stats
            stats_text = (
                f"Max: {e_max:.4f}\n"
                f"Min: {e_min:.4f}\n"
                f"Mean: {e_mean:.4f}\n"
                f"Final: {e_final:.4f}"
            )
            
            # Legend in upper right
            axes[2].legend(loc='upper right', bbox_to_anchor=(1.0, 1.0))
            
            # Place text box below the legend (approx y=0.78)
            axes[2].text(1.0, 0.78, stats_text, transform=axes[2].transAxes, 
                         fontsize=10, verticalalignment='top', horizontalalignment='right',
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            axes[2].set_ylabel("Energy (H)")
            axes[2].set_xlabel("Time Step")
            axes[2].set_title("System Energy Evolution")
        else:
            axes[2].text(0.5, 0.5, "No Energy Data", ha='center', va='center')
            
        plt.tight_layout()
        plt.show()
        
    def __repr__(self):
        return f"SimulationResult(metrics={self.metrics})"
