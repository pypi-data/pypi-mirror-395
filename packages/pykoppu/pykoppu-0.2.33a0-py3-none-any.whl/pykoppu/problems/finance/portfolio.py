"""
Portfolio Optimization Module.

Implements Portfolio Optimization as a QUBO.
"""

import numpy as np
from typing import Any
from ..base import PUBOProblem

class PortfolioOptimization(PUBOProblem):
    """
    Portfolio Optimization Problem.
    
    Minimize risk and maximize return.
    H = q * sum sigma_ij x_i x_j - sum mu_i x_i
    """
    
    def __init__(self, expected_returns: list, covariance_matrix: np.ndarray, risk_aversion: float):
        """
        Initialize Portfolio Optimization.
        
        Args:
            expected_returns (list): List of expected returns (mu).
            covariance_matrix (np.ndarray): Covariance matrix (sigma).
            risk_aversion (float): Risk aversion coefficient (q).
        """
        super().__init__()
        self.mu = np.array(expected_returns)
        self.sigma = np.array(covariance_matrix)
        self.q = risk_aversion
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert to Hamiltonian.
        
        H = q * x^T Sigma x - mu^T x
        
        Map to E = -0.5 x^T J x - h^T x
        
        -0.5 J = q * Sigma  => J = -2 * q * Sigma
        -h = -mu            => h = mu
        """
        self.J = -2 * self.q * self.sigma
        self.h = self.mu

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize Portfolio Optimization solution.
        """
        import matplotlib.pyplot as plt
        
        x = (result.solution >= threshold).astype(int)
        n_assets = len(self.mu)
        
        # Calculate portfolio metrics
        selected_indices = [i for i in range(n_assets) if x[i] == 1]
        
        if not selected_indices:
            print("No assets selected.")
            return
            
        # Pie chart of selected assets (equal weight assumption for binary selection)
        # Or bar chart of returns vs risk for selected assets
        
        plt.figure(figsize=(10, 6))
        
        # Plot Risk vs Return for all assets
        plt.scatter(np.diag(self.sigma), self.mu, c='gray', label='Not Selected', alpha=0.5)
        
        # Highlight selected assets
        selected_risks = np.diag(self.sigma)[selected_indices]
        selected_returns = self.mu[selected_indices]
        plt.scatter(selected_risks, selected_returns, c='green', label='Selected', s=100)
        
        plt.xlabel('Risk (Variance)')
        plt.ylabel('Expected Return')
        plt.title(f'Portfolio Selection (Risk Aversion q={self.q})')
        plt.legend()
        plt.grid(True)
        plt.show()
