"""
3-SAT Problem Module.

Implements the 3-Satisfiability (3-SAT) problem and its conversion to Hamiltonian.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from typing import Any, Dict, List, Tuple
from ..base import PUBOProblem

class SAT3(PUBOProblem):
    """
    3-SAT Problem.
    
    Determines if there exists an interpretation that satisfies a given Boolean formula.
    """
    
    def __init__(self, clauses: List[Tuple[int, int, int]], n_vars: int, penalty: float = 2.0):
        """
        Initialize 3-SAT problem.
        
        Args:
            clauses (List[Tuple[int, int, int]]): List of clauses. 
                Each clause is a tuple of 3 literals.
                Positive int k means variable x_k.
                Negative int -k means NOT x_k.
                Variables are 1-indexed (1 to n_vars).
            n_vars (int): Number of variables.
            penalty (float): Penalty strength for constraints.
        """
        super().__init__()
        self.clauses = clauses
        self.n_vars = n_vars
        self.penalty = penalty
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert 3-SAT to Hamiltonian via Maximum Independent Set (MIS).
        
        Reduction:
        1. Construct a graph G where each node represents a literal in a clause.
           Total nodes = 3 * num_clauses.
        2. Add edges between literals in the same clause (triangle/clique).
           This ensures at most one literal per clause is selected in MIS.
        3. Add edges between conflicting literals (x and NOT x) across clauses.
           This ensures consistency.
           
        We want to find an Independent Set of size equal to num_clauses.
        If such a set exists, we pick one true literal from each clause, and no conflicts exist.
        
        Hamiltonian for MIS:
        Maximize size of independent set: Minimize H = - sum y_i + P * sum_{(i,j) in E} y_i y_j
        Where y_i is binary variable for node i.
        """
        M = len(self.clauses)
        n_nodes = 3 * M
        
        self.J = np.zeros((n_nodes, n_nodes))
        self.h = np.zeros(n_nodes)
        
        # Build the graph
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(n_nodes))
        
        # Store literal info for each node: (variable_index, is_negated)
        self.node_info = {}
        
        # 1. Edges within clauses (Cliques)
        for m, clause in enumerate(self.clauses):
            # Nodes for this clause are 3*m, 3*m+1, 3*m+2
            nodes = [3*m, 3*m+1, 3*m+2]
            
            for k in range(3):
                lit = clause[k]
                var_idx = abs(lit)
                is_negated = (lit < 0)
                self.node_info[nodes[k]] = (var_idx, is_negated)
            
            # Add edges between them
            self.graph.add_edge(nodes[0], nodes[1])
            self.graph.add_edge(nodes[1], nodes[2])
            self.graph.add_edge(nodes[2], nodes[0])
            
        # 2. Edges between conflicting literals
        for i in range(n_nodes):
            var_i, neg_i = self.node_info[i]
            for j in range(i + 1, n_nodes):
                var_j, neg_j = self.node_info[j]
                
                # Conflict if same variable but opposite sign
                if var_i == var_j and neg_i != neg_j:
                    self.graph.add_edge(i, j)
                    
        # Construct Hamiltonian
        # H = - sum y_i + P * sum_{(i,j) in E} y_i y_j
        P = self.penalty
        
        # Linear term: -1 for each node in Hamiltonian => +1 in Bias
        self.h[:] = 1.0
        
        # Quadratic term: P for each edge (penalty for selecting connected nodes)
        for u, v in self.graph.edges:
            self.J[u, v] = P
            self.J[v, u] = P
            
    def decode_solution(self, result: Any, threshold: float = 0.5) -> Dict[int, bool]:
        """
        Decode solution from MIS to Truth Assignment.
        """
        y = (result.solution >= threshold).astype(int)
        assignment = {}
        
        for i in range(len(y)):
            if y[i] == 1:
                var_idx, is_negated = self.node_info[i]
                # If node is selected, the literal is TRUE.
                # If literal is x, then x=True.
                # If literal is NOT x, then x=False.
                val = not is_negated
                
                # Check for consistency
                if var_idx in assignment and assignment[var_idx] != val:
                    # Conflict in solution (should be prevented by P)
                    print(f"Warning: Inconsistent assignment for variable {var_idx}")
                assignment[var_idx] = val
                
        # Fill missing variables with False (default)
        for v in range(1, self.n_vars + 1):
            if v not in assignment:
                assignment[v] = False
                
        return assignment

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize SAT graph and solution.
        """
        y = (result.solution >= threshold).astype(int)
        
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph, seed=42)
        
        node_colors = ['green' if val == 1 else 'lightgray' for val in y]
        
        # Labels: Show literal (e.g., "x1", "-x2")
        labels = {}
        for i in range(len(y)):
            var_idx, is_negated = self.node_info[i]
            sign = "-" if is_negated else ""
            labels[i] = f"{sign}x{var_idx}"
            
        nx.draw(
            self.graph, 
            pos, 
            with_labels=True, 
            labels=labels,
            node_color=node_colors, 
            edge_color='gray', 
            node_size=600, 
            font_color='black'
        )
        
        # Check if solution is valid (Independent Set)
        is_independent = True
        for u, v in self.graph.edges:
            if y[u] == 1 and y[v] == 1:
                is_independent = False
                break
                
        # Check clause satisfaction
        satisfied_clauses = 0
        total_clauses = len(self.clauses)
        # We need to sum selected nodes per clause. Ideally exactly 1.
        # But for SAT, we just need >= 1 true literal.
        # Wait, the MIS reduction ensures exactly one literal per clause is selected?
        # Yes, because of the clique constraints.
        # If MIS size = M, then exactly one per clause.
        
        selected_count = sum(y)
        
        title = f"SAT3 Solution (Green = Selected)\n"
        title += f"Selected Nodes: {selected_count}/{total_clauses} | Independent: {is_independent}"
        plt.title(title)
        plt.show()
