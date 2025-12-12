"""
Seismic Feature Selection Module.

Implements the Seismic Feature Selection problem using mRMR approach.
"""

import numpy as np
from typing import Any, Dict, List, Optional, Union
from ..base import PUBOProblem

class SeismicFeatureSelection(PUBOProblem):
    """
    Seismic Feature Selection Problem.
    
    Selects optimal subset of seismic attributes to maximize relevance to a target
    while minimizing redundancy between selected attributes (mRMR).
    Subject to a cardinality constraint (select exactly k attributes).
    """
    
    def __init__(
        self, 
        relevance: Union[List[float], np.ndarray], 
        redundancy: Union[List[List[float]], np.ndarray], 
        k: int, 
        alpha: float = 1.0, 
        beta: float = 1.0,
        penalty_k: float = 10.0
    ):
        """
        Initialize Seismic Feature Selection problem.
        
        Args:
            relevance (Array-like): Vector of relevance scores for each attribute (R).
            redundancy (Array-like): Matrix of redundancy/correlation between attributes (C).
            k (int): Number of attributes to select.
            alpha (float): Weight for relevance term.
            beta (float): Weight for redundancy term.
            penalty_k (float): Penalty strength for cardinality constraint.
        """
        super().__init__()
        self.relevance = np.array(relevance)
        self.redundancy = np.array(redundancy)
        self.k = k
        self.alpha = alpha
        self.beta = beta
        self.penalty_k = penalty_k
        
        self.n_features = len(self.relevance)
        if self.redundancy.shape != (self.n_features, self.n_features):
            raise ValueError("Redundancy matrix shape must match number of features.")
            
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert to Hamiltonian.
        
        Variables: x_i = 1 if attribute i is selected, 0 otherwise.
        
        H = H_rel + H_red + H_card
        
        1. H_rel (Maximize relevance => Minimize negative):
           H_rel = sum (-alpha * R_i * x_i)
           
        2. H_red (Minimize redundancy):
           H_red = sum_{i,j} beta * C_{ij} * x_i * x_j
           
        3. H_card (Select exactly k):
           H_card = P * (sum x_i - k)^2
                  = P * (sum x_i^2 + sum_{i!=j} x_i x_j - 2k sum x_i + k^2)
                  = P * (sum x_i + sum_{i!=j} x_i x_j - 2k sum x_i + k^2)  (since x^2=x)
                  = P * (sum (1-2k) x_i + sum_{i!=j} x_i x_j + k^2)
        """
        n = self.n_features
        self.J = np.zeros((n, n))
        self.h = np.zeros(n)
        self.offset = 0.0
        
        P = self.penalty_k
        k = self.k
        
        # 1. H_rel
        # h_i_solver += alpha * R_i
        # (Since H term is -alpha R_i x_i, and solver is -h x)
        self.h += self.alpha * self.relevance
        
        # 2. H_red
        # Term: beta * C_{ij} * x_i * x_j
        # J_ij_solver = -2 * beta * C_{ij}
        # Note: Usually redundancy matrix is symmetric. We iterate i!=j.
        # If C_{ij} is stored for both i,j and j,i, we handle carefully.
        # Let's iterate all pairs.
        
        # 3. H_card
        # Constant: P * k^2
        self.offset += P * (k**2)
        
        # Linear: P * (1 - 2k) * x_i
        # h_i_solver -= P * (1 - 2k)
        self.h -= P * (1 - 2 * k)
        
        # Quadratic: P * x_i * x_j (for i != j)
        # J_ij_solver -= 2 * P
        
        # Combine Quadratic Terms
        for i in range(n):
            for j in range(i + 1, n):
                # Redundancy term (beta * C_ij)
                # We assume C is symmetric or we take average? Usually symmetric.
                c_val = self.redundancy[i, j]
                
                # Cardinality term (P)
                
                # Total coeff in H for x_i x_j is (beta * c_val + P)
                # Solver J_ij = -2 * (beta * c_val + P)
                
                val = -2 * (self.beta * c_val + P)
                self.J[i, j] += val
                self.J[j, i] += val
                
    def evaluate(self, solution: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate solution.
        """
        x = (solution > 0.5).astype(int)
        
        selected_indices = [i for i, val in enumerate(x) if val == 1]
        count = len(selected_indices)
        
        total_relevance = 0.0
        total_redundancy = 0.0
        
        for i in selected_indices:
            total_relevance += self.relevance[i]
            for j in selected_indices:
                if i != j:
                    total_redundancy += self.redundancy[i, j]
                    
        # Redundancy is usually summed over pairs, so if we double count (i,j) and (j,i), 
        # it matches the H formulation sum_{i,j}.
        
        valid = (count == self.k)
        
        # mRMR score = Rel - Red (or Rel / Red depending on formulation, here diff)
        # We used alpha*Rel - beta*Red in Hamiltonian (minimized negative Rel + pos Red)
        score = self.alpha * total_relevance - self.beta * total_redundancy
        
        return {
            "valid": valid,
            "selected_count": count,
            "target_k": self.k,
            "total_relevance": total_relevance,
            "total_redundancy": total_redundancy,
            "mrmr_score": score,
            "selected_indices": selected_indices
        }

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize Feature Selection.
        """
        import matplotlib.pyplot as plt
        
        x_sol = (result.solution >= threshold).astype(int)
        selected_indices = [i for i, val in enumerate(x_sol) if val == 1]
        
        # Calculate average redundancy for each feature (to plot against relevance)
        # Avg redundancy with ALL other features? Or just general "redundancy score"?
        # Let's plot Relevance vs Avg Correlation with others.
        avg_redundancy = np.mean(self.redundancy, axis=1)
        
        plt.figure(figsize=(10, 6))
        
        # Plot all features
        plt.scatter(avg_redundancy, self.relevance, c='gray', alpha=0.5, label='Ignored Features')
        
        # Highlight selected
        if selected_indices:
            sel_rel = self.relevance[selected_indices]
            sel_red = avg_redundancy[selected_indices]
            plt.scatter(sel_red, sel_rel, c='red', s=100, label='Selected Features')
            
            for i, txt in enumerate(selected_indices):
                plt.annotate(f"F{txt}", (sel_red[i], sel_rel[i]), xytext=(5, 5), textcoords='offset points')
        
        metrics = self.evaluate(result.solution)
        title = f"Seismic Feature Selection (k={self.k})\nSelected: {metrics['selected_count']} | Valid: {metrics['valid']}"
        
        plt.title(title)
        plt.xlabel("Average Redundancy (Correlation)")
        plt.ylabel("Relevance")
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.show()
