"""
Knapsack Problem Module.

Implements the Knapsack problem as a QUBO.
"""

from typing import List, Dict, Any
import numpy as np
from ..base import PUBOProblem

class Knapsack(PUBOProblem):
    """
    Knapsack Problem.
    
    Maximize sum v_i x_i subject to sum w_i x_i <= C.
    Implemented as QUBO with penalty for equality constraint (slack variables omitted for simplicity
    or assuming exact capacity match if that's the prompt's implication, 
    but usually Knapsack is inequality. The prompt formula uses (sum w_i x_i - C)^2 
    which enforces equality sum w_i x_i = C).
    """
    
    def __init__(self, items: List[Dict[str, float]], capacity: float, penalty: float):
        """
        Initialize Knapsack problem.
        
        Args:
            items (List[Dict]): List of items with 'value' and 'weight'.
            capacity (float): Target capacity.
            penalty (float): Penalty coefficient (P).
        """
        super().__init__()
        self.items = items
        self.capacity = capacity
        self.penalty = penalty
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert to Hamiltonian.
        
        H = - sum v_i x_i + P (sum w_i x_i - C)^2
        
        Expand squared term:
        (sum w_i x_i - C)^2 = (sum w_i x_i)^2 - 2C sum w_i x_i + C^2
        (sum w_i x_i)^2 = sum w_i^2 x_i^2 + sum_{i!=j} w_i w_j x_i x_j
        Since x_i is binary, x_i^2 = x_i.
        = sum w_i^2 x_i + sum_{i!=j} w_i w_j x_i x_j
        
        Combine linear terms (x_i):
        H_linear = - v_i + P(w_i^2 - 2C w_i)
        
        Combine quadratic terms (x_i x_j):
        H_quad = P w_i w_j
        
        We want to minimize H.
        E = -0.5 x^T J x - h^T x
        
        So we need to map H coefficients to J and h.
        H = sum_{i<j} 2 * (P w_i w_j) x_i x_j + sum (coeff_i) x_i
        (The 2 is because sum_{i!=j} includes both ij and ji).
        
        Map to E:
        -0.5 * J_ij = P w_i w_j  => J_ij = -2 P w_i w_j
        -h_i = -v_i + P(w_i^2 - 2C w_i) => h_i = v_i - P(w_i^2 - 2C w_i)
        """
        n = len(self.items)
        weights = np.array([item['weight'] for item in self.items])
        values = np.array([item['value'] for item in self.items])
        P = self.penalty
        C = self.capacity
        
        self.J = np.zeros((n, n))
        self.h = np.zeros(n)
        
        # Linear terms
        # h_i = v_i - P * w_i^2 + 2 * P * C * w_i
        self.h = values - P * (weights**2) + 2 * P * C * weights
        
        # Constant term (offset)
        # H_const = P * C^2
        self.offset = P * (C**2)
        
        # Quadratic terms
        # J_ij = -2 * P * w_i * w_j
        for i in range(n):
            for j in range(i + 1, n):
                val = -2 * P * weights[i] * weights[j]
                self.J[i, j] = val
                self.J[j, i] = val

    def evaluate(self, solution: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate Knapsack solution.
        """
        # Binarize solution
        x = (solution > 0.5).astype(int)
        
        total_weight = 0.0
        total_value = 0.0
        
        for i, item in enumerate(self.items):
            if x[i] == 1:
                total_weight += item['weight']
                total_value += item['value']
                
        valid = total_weight <= self.capacity
        
        return {
            "valid": valid,
            "total_value": total_value,
            "total_weight": total_weight,
            "capacity": self.capacity
        }

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize Knapsack solution.
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Identify selected items based on threshold
        x = (result.solution >= threshold).astype(int)
        selected_indices = [i for i, val in enumerate(x) if val == 1]
        
        if not selected_indices:
            print(f"No items selected (Threshold: {threshold}).")
            return

        selected_items = [self.items[i] for i in selected_indices]
        names = [item['name'] for item in selected_items]
        weights = [item['weight'] for item in selected_items]
        values = [item['value'] for item in selected_items]
        
        # Recalculate metrics
        total_weight = sum(weights)
        total_value = sum(values)
        valid = total_weight <= self.capacity
        status = "VALID" if valid else "INVALID (Over Capacity)"
        
        # Create a figure with 2 subplots
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot Weights
        sns.barplot(x=names, y=weights, ax=axes[0], palette="Blues_d", hue=names, legend=False)
        axes[0].axhline(y=self.capacity, color='r', linestyle='--', label='Capacity')
        axes[0].set_title("Selected Items: Weights")
        axes[0].set_ylabel("Weight")
        
        # Plot Values
        sns.barplot(x=names, y=values, ax=axes[1], palette="Greens_d", hue=names, legend=False)
        axes[1].set_title("Selected Items: Values")
        axes[1].set_ylabel("Value")
        
        plt.suptitle(f"Knapsack Solution: {status}\nThreshold: {threshold} | Total Value: {total_value} | Total Weight: {total_weight}/{self.capacity}")
        plt.tight_layout()
        plt.show()
