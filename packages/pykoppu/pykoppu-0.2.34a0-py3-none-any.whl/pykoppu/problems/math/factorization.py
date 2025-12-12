"""
Integer Factorization Problem Module.

Implements the Integer Factorization problem as a QUBO.
"""

import numpy as np
from typing import Any, Dict, List, Tuple, Optional
from ..base import PUBOProblem

class Factorization(PUBOProblem):
    """
    Integer Factorization Problem.
    
    Factors a number N into two integers p and q such that N = p * q.
    Uses a multiplication circuit reduction to QUBO.
    """
    
    def __init__(self, target: int, p_bits: Optional[int] = None, q_bits: Optional[int] = None, penalty: float = 10.0):
        """
        Initialize Factorization problem.
        
        Args:
            target (int): The number to factor (N).
            p_bits (int): Number of bits for the first factor p.
            q_bits (int): Number of bits for the second factor q.
            penalty (float): Penalty strength for consistency constraints.
        """
        super().__init__()
        self.target = target
        
        # Estimate bits if not provided
        # For N, we roughly need log2(N) bits total.
        # Split roughly half-half.
        n_bits_total = target.bit_length()
        if p_bits is None:
            p_bits = (n_bits_total + 1) // 2
        if q_bits is None:
            q_bits = n_bits_total - p_bits + 1 # Add a bit of slack
            
        self.n = p_bits
        self.m = q_bits
        self.penalty = penalty
        
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert Factorization to Hamiltonian.
        
        Variables:
        - x_i: bits of p (0..n-1)
        - y_j: bits of q (0..m-1)
        - z_{ij}: auxiliary variables for x_i * y_j
        
        Hamiltonian H = H_fact + H_cons
        
        H_fact = (N - sum_{i,j} 2^{i+j} z_{ij})^2
               = (N - P)^2 where P is the product constructed from z
        
        H_cons = sum_{i,j} P_penalty * (3 z_{ij} + x_i y_j - 2 x_i z_{ij} - 2 y_j z_{ij})
        This penalty enforces z_{ij} = x_i AND y_j.
        """
        n = self.n
        m = self.m
        N = self.target
        P_penalty = self.penalty
        
        # Total variables: n (x) + m (y) + n*m (z)
        num_vars = n + m + n * m
        
        self.J = np.zeros((num_vars, num_vars))
        self.h = np.zeros(num_vars)
        self.offset = 0.0
        
        # Helper to get index
        def idx_x(i): return i
        def idx_y(j): return n + j
        def idx_z(i, j): return n + m + i * m + j
        
        # 1. Consistency Hamiltonian (H_cons)
        # P * (3 z - 2 x z - 2 y z + x y)
        # Linear parts: 3 P z
        # Quadratic parts: -2 P x z, -2 P y z, + P x y
        
        for i in range(n):
            for j in range(m):
                u = idx_x(i)
                v = idx_y(j)
                w = idx_z(i, j)
                
                # Linear term for z
                self.h[w] += 3 * P_penalty
                
                # Quadratic terms
                # x * y
                self.J[u, v] += P_penalty
                self.J[v, u] += P_penalty
                
                # x * z
                self.J[u, w] -= 2 * P_penalty
                self.J[w, u] -= 2 * P_penalty
                
                # y * z
                self.J[v, w] -= 2 * P_penalty
                self.J[w, v] -= 2 * P_penalty
                
        # 2. Factorization Hamiltonian (H_fact)
        # (N - S)^2 where S = sum_{i,j} C_{ij} z_{ij} with C_{ij} = 2^{i+j}
        # = N^2 - 2 N S + S^2
        # S^2 = (sum C z)^2 = sum C^2 z^2 + sum_{k!=l} C_k C_l z_k z_l
        # Since z is binary, z^2 = z.
        # S^2 = sum C^2 z + sum_{k!=l} C_k C_l z_k z_l
        
        # Constant term
        self.offset += N**2
        
        coeffs = {} # Map z_idx -> coefficient 2^{i+j}
        for i in range(n):
            for j in range(m):
                coeffs[idx_z(i, j)] = 2**(i + j)
                
        # Linear term from -2 N S
        for w, coeff in coeffs.items():
            self.h[w] -= 2 * N * coeff
            
        # Quadratic term from S^2
        # Diagonal part (z^2 = z)
        for w, coeff in coeffs.items():
            self.h[w] += coeff**2
            
        # Off-diagonal part
        z_indices = list(coeffs.keys())
        for idx1 in range(len(z_indices)):
            for idx2 in range(idx1 + 1, len(z_indices)):
                w1 = z_indices[idx1]
                w2 = z_indices[idx2]
                c1 = coeffs[w1]
                c2 = coeffs[w2]
                
                val = 2 * c1 * c2 # 2 because J_ij and J_ji
                self.J[w1, w2] += val/2 # Symmetric matrix, add half to each?
                self.J[w2, w1] += val/2 # Wait, my convention in other files:
                # Knapsack: J[i,j] = val; J[j,i] = val where val = -2 P w_i w_j
                # The formula was -0.5 x J x.
                # Here I am constructing H directly.
                # Let's stick to the convention: E = -0.5 x^T J x - h^T x
                # So if H has term +A x_i x_j, then -0.5 J_ij = A/2 (if J symmetric) => J_ij = -A.
                # Wait, let's check Knapsack again.
                # H_quad = P w_i w_j x_i x_j
                # J_ij = -2 P w_i w_j.
                # -0.5 * (-2 P) = P. Correct.
                
                # So if I have term +C x_i x_j in H, I need J_ij = -2 * C.
                
        # Let's re-apply the mapping to J and h
        # Current self.J and self.h are accumulating coefficients of H.
        # We need to negate them and multiply J by 2 for the solver format?
        # Solver expects: E = -0.5 x J x - h x
        # My H = 0.5 x J_H x + h_H x + offset
        # So J_solver = - J_H
        # h_solver = - h_H
        # But wait, J_H usually has 2*coeff for off-diagonal if we sum over i<j.
        # Let's just build H coefficients first, then convert.
        
        pass # Logic continues below
        
        # Let's restart the J/h population with the correct sign for the solver.
        # We want to MINIMIZE H.
        # Solver MINIMIZES E = -0.5 x J x - h x.
        # So we want E ~ H.
        # H = sum Q_{ij} x_i x_j + sum L_i x_i
        # J_{ij} = -2 * Q_{ij} (for i != j)
        # h_i = -L_i - Q_{ii} (if we treat x^2 as x in Q) -- wait.
        # Usually Q matrix format: x^T Q x.
        # x_i^2 = x_i. So diagonal Q_{ii} adds to linear term.
        # H = sum_{i<j} 2 Q_{ij} x_i x_j + sum (L_i + Q_{ii}) x_i
        # Match with -0.5 sum J_{ij} x_i x_j - sum h_i x_i
        # -0.5 J_{ij} = Q_{ij} (for symmetric J, i!=j, effectively sum over all i!=j is sum_{i<j} 2...)
        # Actually: sum_{i!=j} (-0.5 J_{ij}) x_i x_j = sum_{i<j} (- J_{ij}) x_i x_j
        # We want this to equal sum_{i<j} 2 Q_{ij} x_i x_j (if Q is symmetric? No, usually Q is upper triangular in QUBO).
        # Let's assume H terms are accumulated.
        
        # Let's reset and do it cleanly.
        self.J.fill(0)
        self.h.fill(0)
        
        # We will accumulate terms into a temporary Q matrix (upper triangular) and linear L vector.
        Q = {} # (i, j) -> val with i < j
        L = np.zeros(num_vars)
        
        def add_quad(i, j, val):
            if i == j:
                L[i] += val
            else:
                if i > j: i, j = j, i
                Q[(i, j)] = Q.get((i, j), 0.0) + val
                
        def add_linear(i, val):
            L[i] += val
            
        # 1. Consistency
        # P * (3 z - 2 x z - 2 y z + x y)
        for i in range(n):
            for j in range(m):
                u = idx_x(i)
                v = idx_y(j)
                w = idx_z(i, j)
                
                add_linear(w, 3 * P_penalty)
                add_quad(u, v, P_penalty)     # + x y
                add_quad(u, w, -2 * P_penalty) # -2 x z
                add_quad(v, w, -2 * P_penalty) # -2 y z
                
        # 2. Factorization
        # (N - S)^2 = N^2 - 2 N S + S^2
        # S = sum C_{ij} z_{ij}
        
        # Linear: -2 N C_{ij} z_{ij}
        for i in range(n):
            for j in range(m):
                w = idx_z(i, j)
                c = 2**(i + j)
                add_linear(w, -2 * N * c)
                
        # Quadratic: S^2 = (sum C z)^2 = sum C_k C_l z_k z_l
        z_vars = []
        for i in range(n):
            for j in range(m):
                z_vars.append((idx_z(i, j), 2**(i + j)))
                
        for idx1 in range(len(z_vars)):
            for idx2 in range(len(z_vars)):
                u, c1 = z_vars[idx1]
                v, c2 = z_vars[idx2]
                # Term c1 * c2 * z_u * z_v
                add_quad(u, v, c1 * c2)
                
        # Convert Q and L to J and h for the solver
        # Solver E = -0.5 x J x - h x
        # We want H = x Q x + L x
        # Terms match:
        # x_i x_j (i<j): H has Q_{ij}. Solver has -J_{ij} (since symmetric J contributes twice -0.5).
        # So -J_{ij} = Q_{ij} => J_{ij} = -Q_{ij}.
        # x_i: H has L_i. Solver has -h_i.
        # So h_i = -L_i.
        
        self.h = -L
        for (u, v), val in Q.items():
            self.J[u, v] = -val
            self.J[v, u] = -val
            
    def evaluate(self, solution: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate Factorization solution.
        """
        x_sol = (solution > 0.5).astype(int)
        
        n = self.n
        m = self.m
        
        # Decode p
        p = 0
        for i in range(n):
            if x_sol[i] == 1:
                p += 2**i
                
        # Decode q
        q = 0
        for j in range(m):
            if x_sol[n + j] == 1:
                q += 2**j
                
        product = p * q
        valid = (product == self.target)
        
        return {
            "valid": valid,
            "p": p,
            "q": q,
            "product": product,
            "target": self.target,
            "diff": abs(product - self.target)
        }

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize Factorization result.
        """
        import matplotlib.pyplot as plt
        metrics = self.evaluate(result.solution)
        
        p = metrics['p']
        q = metrics['q']
        prod = metrics['product']
        target = metrics['target']
        valid = metrics['valid']
        
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.7, f"{target}", fontsize=40, ha='center', va='center', fontweight='bold')
        plt.text(0.5, 0.5, "=", fontsize=30, ha='center', va='center')
        
        color = 'green' if valid else 'red'
        plt.text(0.3, 0.3, f"{p}", fontsize=30, ha='center', va='center', color='blue')
        plt.text(0.5, 0.3, "x", fontsize=20, ha='center', va='center')
        plt.text(0.7, 0.3, f"{q}", fontsize=30, ha='center', va='center', color='blue')
        
        plt.text(0.5, 0.1, f"Result: {prod} ({'VALID' if valid else 'INVALID'})", 
                 ha='center', va='center', color=color, fontsize=12)
        
        plt.axis('off')
        plt.title(f"Factorization of {target}")
        plt.show()
