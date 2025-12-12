"""
Well Placement Optimization Module.

Implements the Well Placement problem for the Energy sector.
"""

import numpy as np
import math
from typing import Any, Dict, List, Optional
from ..base import PUBOProblem

class WellPlacement(PUBOProblem):
    """
    Well Placement Optimization Problem.
    
    Selects optimal well locations from a set of candidates to maximize production value
    while respecting budget and minimum distance constraints.
    """
    
    def __init__(
        self, 
        locations: List[Dict[str, Any]], 
        budget: float, 
        min_dist: float, 
        penalty_budget: float = 10.0,
        penalty_dist: float = 10.0
    ):
        """
        Initialize Well Placement problem.
        
        Args:
            locations (List[Dict]): List of candidate locations. Each dict must have:
                - 'id': int/str identifier
                - 'x': float x-coordinate
                - 'y': float y-coordinate
                - 'value': float estimated production value
                - 'cost': float drilling cost
            budget (float): Total available budget.
            min_dist (float): Minimum required distance between any two wells.
            penalty_budget (float): Penalty strength for budget constraint.
            penalty_dist (float): Penalty strength for distance constraint.
        """
        super().__init__()
        self.locations = locations
        self.budget = budget
        self.min_dist = min_dist
        self.penalty_budget = penalty_budget
        self.penalty_dist = penalty_dist
        
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert to Hamiltonian.
        
        Variables: x_i = 1 if well i is selected, 0 otherwise.
        
        H = H_value + H_budget + H_dist
        
        1. H_value (Maximize value => Minimize negative value):
           H_value = sum (-v_i * x_i)
           
        2. H_budget (Constraint: sum c_i x_i <= B):
           Modeled as equality penalty (sum c_i x_i - B)^2 for simplicity, 
           assuming we want to utilize the budget.
           = (sum c_i x_i)^2 - 2B sum c_i x_i + B^2
           = sum c_i^2 x_i + sum_{i!=j} c_i c_j x_i x_j - 2B sum c_i x_i + B^2
           
        3. H_dist (Constraint: dist(i, j) >= min_dist):
           Penalty if both x_i and x_j are selected and dist(i, j) < min_dist.
           H_dist = sum_{i<j, incompatible} P_dist * x_i * x_j
        """
        n = len(self.locations)
        self.J = np.zeros((n, n))
        self.h = np.zeros(n)
        self.offset = 0.0
        
        # Extract values and costs
        values = np.array([loc['value'] for loc in self.locations])
        costs = np.array([loc['cost'] for loc in self.locations])
        
        P_budget = self.penalty_budget
        P_dist = self.penalty_dist
        B = self.budget
        
        # 1. H_value
        # h_i += -v_i
        # Remember solver minimizes E = -0.5 x J x - h x
        # We want H = ... + sum (-v_i) x_i
        # So -h_i_solver = -v_i => h_i_solver = v_i
        self.h += values
        
        # 2. H_budget
        # Constant: P * B^2
        self.offset += P_budget * (B**2)
        
        # Linear: P * (c_i^2 - 2B c_i)
        # -h_i_solver += P * (c_i^2 - 2B c_i)
        # h_i_solver -= P * (c_i^2 - 2B c_i)
        self.h -= P_budget * (costs**2 - 2 * B * costs)
        
        # Quadratic: P * c_i c_j (for i != j)
        # -0.5 J_ij_solver = P * c_i c_j
        # J_ij_solver = -2 * P * c_i c_j
        for i in range(n):
            for j in range(i + 1, n):
                val = -2 * P_budget * costs[i] * costs[j]
                self.J[i, j] += val
                self.J[j, i] += val
                
        # 3. H_dist
        # For incompatible pairs (i, j): + P_dist * x_i * x_j
        # -0.5 J_ij_solver = P_dist
        # J_ij_solver = -2 * P_dist
        
        # Precompute distances
        coords = [(loc['x'], loc['y']) for loc in self.locations]
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = math.sqrt((coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2)
                if dist < self.min_dist:
                    # Violation if both selected
                    val = -2 * P_dist
                    self.J[i, j] += val
                    self.J[j, i] += val
                    
    def evaluate(self, solution: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate solution.
        """
        x = (solution > 0.5).astype(int)
        
        total_value = 0.0
        total_cost = 0.0
        selected_indices = []
        
        for i, val in enumerate(x):
            if val == 1:
                total_value += self.locations[i]['value']
                total_cost += self.locations[i]['cost']
                selected_indices.append(i)
                
        # Check constraints
        budget_ok = (total_cost <= self.budget) # Relaxed check (inequality)
        
        dist_ok = True
        min_dist_found = float('inf')
        coords = [(self.locations[i]['x'], self.locations[i]['y']) for i in selected_indices]
        
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                d = math.sqrt((coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2)
                if d < min_dist_found:
                    min_dist_found = d
                if d < self.min_dist:
                    dist_ok = False
                    
        valid = budget_ok and dist_ok
        
        return {
            "valid": valid,
            "total_value": total_value,
            "total_cost": total_cost,
            "budget": self.budget,
            "budget_ok": budget_ok,
            "dist_ok": dist_ok,
            "min_dist_found": min_dist_found if len(coords) > 1 else None,
            "selected_count": len(selected_indices)
        }

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize Well Placement.
        """
        import matplotlib.pyplot as plt
        
        x_sol = (result.solution >= threshold).astype(int)
        
        # Prepare data
        x_coords = [loc['x'] for loc in self.locations]
        y_coords = [loc['y'] for loc in self.locations]
        values = [loc['value'] for loc in self.locations]
        
        # Plot
        plt.figure(figsize=(10, 8))
        
        # Plot all candidates as small circles, size proportional to value?
        # Or color proportional to value.
        plt.scatter(x_coords, y_coords, c=values, cmap='viridis', s=100, alpha=0.6, label='Candidates')
        plt.colorbar(label='Potential Value')
        
        # Highlight selected
        selected_x = [x_coords[i] for i, val in enumerate(x_sol) if val == 1]
        selected_y = [y_coords[i] for i, val in enumerate(x_sol) if val == 1]
        
        if selected_x:
            plt.scatter(selected_x, selected_y, color='red', s=200, marker='*', label='Selected Well')
            
            # Draw radius circles?
            # for sx, sy in zip(selected_x, selected_y):
            #     circle = plt.Circle((sx, sy), self.min_dist/2, color='red', fill=False, linestyle='--')
            #     plt.gca().add_patch(circle)
        
        metrics = self.evaluate(result.solution)
        title = f"Well Placement (Value: {metrics['total_value']:.1f} | Cost: {metrics['total_cost']:.1f}/{self.budget})"
        if not metrics['valid']:
            title += f"\nINVALID: Budget={metrics['budget_ok']}, Dist={metrics['dist_ok']}"
            
        plt.title(title)
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.show()
