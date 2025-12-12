"""
TSP Problem Module.

Implements the Traveling Salesperson Problem (TSP) and its conversion to Hamiltonian.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Any, Dict, List
from ..base import PUBOProblem

class TSP(PUBOProblem):
    """
    Traveling Salesperson Problem (TSP).
    
    Finds the shortest route visiting each city exactly once and returning to the origin.
    """
    
    def __init__(self, distance_matrix: np.ndarray, penalty: float = 10.0):
        """
        Initialize TSP problem.
        
        Args:
            distance_matrix (np.ndarray): NxN matrix of distances between cities.
            penalty (float): Penalty strength for constraints.
        """
        super().__init__()
        self.distance_matrix = np.array(distance_matrix)
        self.n_cities = self.distance_matrix.shape[0]
        self.penalty = penalty
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert TSP to Hamiltonian.
        
        Variables: x_{i,t} = 1 if city i is visited at step t.
        Total variables: N^2.
        
        Constraints:
        1. Each city visited exactly once: sum_t x_{i,t} = 1 for all i.
        2. Each step has exactly one city: sum_i x_{i,t} = 1 for all t.
        
        Objective:
        Minimize distance: sum_{i,j} sum_t d_{ij} x_{i,t} x_{j,t+1}
        
        Hamiltonian:
        H = A * sum_i (sum_t x_{i,t} - 1)^2  (Row constraints)
          + A * sum_t (sum_i x_{i,t} - 1)^2  (Column constraints)
          + sum_{i,j} sum_t d_{ij} x_{i,t} x_{j,t+1} (Distance)
        """
        N = self.n_cities
        A = self.penalty
        
        # Total variables = N * N
        n_vars = N * N
        self.J = np.zeros((n_vars, n_vars))
        self.h = np.zeros(n_vars)
        
        # Helper to get index of x_{i,t}
        def idx(i, t):
            return i * N + t
            
        # 1. Constraint: Each city visited once (Row sum = 1)
        # H_row = A * sum_i (sum_t x_{i,t} - 1)^2
        #       = A * sum_i [ (sum_t x_{i,t})^2 - 2 sum_t x_{i,t} + 1 ]
        #       = A * sum_i [ sum_t x_{i,t}^2 + sum_{t!=t'} x_{i,t} x_{i,t'} - 2 sum_t x_{i,t} + 1 ]
        # Since x^2 = x for binary variables:
        #       = A * sum_i [ sum_t x_{i,t} + sum_{t!=t'} x_{i,t} x_{i,t'} - 2 sum_t x_{i,t} ]
        #       = A * sum_i [ sum_{t!=t'} x_{i,t} x_{i,t'} - sum_t x_{i,t} ]
        
        for i in range(N):
            for t in range(N):
                # Linear term: -A in Hamiltonian => +A in Bias (since E = -h^T x)
                u = idx(i, t)
                self.h[u] += A
                
                # Quadratic term: A for all pairs (t, t') with t != t'
                for t_prime in range(N):
                    if t != t_prime:
                        v = idx(i, t_prime)
                        self.J[u, v] += A
                        
        # 2. Constraint: Each step has one city (Column sum = 1)
        # H_col = A * sum_t (sum_i x_{i,t} - 1)^2
        # Similar derivation:
        #       = A * sum_t [ sum_{i!=j} x_{i,t} x_{j,t} - sum_i x_{i,t} ]
        
        for t in range(N):
            for i in range(N):
                # Linear term: -A in Hamiltonian => +A in Bias
                u = idx(i, t)
                self.h[u] += A
                
                # Quadratic term: A for all pairs (i, j) with i != j
                for j in range(N):
                    if i != j:
                        v = idx(j, t)
                        self.J[u, v] += A
                        
        # 3. Objective: Minimize Distance
        # H_dist = sum_{i,j} d_{ij} sum_t x_{i,t} x_{j,t+1}
        # Note: t+1 is modulo N (closed loop)
        
        for i in range(N):
            for j in range(N):
                if i == j: continue
                dist = self.distance_matrix[i, j]
                
                for t in range(N):
                    u = idx(i, t)
                    v = idx(j, (t + 1) % N)
                    
                    # Add distance to coupling
                    # Note: J is symmetric in our storage, but here we add directed term.
                    # Since x_u x_v = x_v x_u, we add to J[u,v] and J[v,u] carefully.
                    # Usually we just add to J[u,v] and let the symmetry handle it or add half.
                    # Let's add full value to J[u,v] and assume J is treated as sum J_uv x_u x_v
                    # If J is symmetric matrix in energy calculation 0.5 xJx, then we need to add to both?
                    # My previous logic (MaxCut) used J[i,j] = val; J[j,i] = val.
                    # Here u != v always (different time steps).
                    
                    self.J[u, v] += dist
                    # self.J[v, u] += dist # Don't double count if we iterate all pairs?
                    # Wait, the loop iterates all i,j. So it will encounter (j,i) later.
                    # But (j,i) term is x_{j,t} x_{i,t+1}. This is DIFFERENT from x_{i,t} x_{j,t+1}.
                    # So these are distinct terms in the Hamiltonian sum.
                    # So we just add to J[u,v].
                    # However, if the solver expects a symmetric J, we should ensure J[u,v] == J[v,u].
                    # But x_u x_v is the same as x_v x_u.
                    # So term d_{ij} x_{i,t} x_{j,t+1} contributes to interaction between u and v.
                    # We should add d_{ij} to the interaction strength.
                    # If we enforce symmetry, we can add d_{ij} to J[u,v] and J[v,u] ?
                    # Or just J[u,v] += d_{ij} and rely on solver to symmetrize?
                    # Let's add to J[u,v] and J[v,u] to be safe and explicit about the undirected interaction between variables.
                    # But wait, d_{ij} might not be equal to d_{ji} (asymmetric TSP).
                    # But x_{i,t} x_{j,t+1} connects u=(i,t) and v=(j,t+1).
                    # The reverse interaction is v=(j,t+1) and u=(i,t).
                    # This is the SAME pair of variables.
                    # So the coefficient for x_u x_v is d_{ij}.
                    # If we want symmetric J, we set J[u,v] = J[v,u] = d_{ij}.
                    # Wait, if we do that, the energy term 0.5 * (J[u,v]x_u x_v + J[v,u]x_v x_u) = d_{ij} x_u x_v.
                    # Correct.
                    
                    self.J[v, u] += dist
                    
        # 4. Enforce Start at City 0 (Time 0)
        # We add a strong bias to x_{0,0} to encourage it to be 1.
        # The constraints will then force x_{0,t}=0 for t>0 and x_{i,0}=0 for i>0.
        # Bias should be strong enough to overcome other terms.
        # A simple heuristic is -2 * A (since A is penalty for constraints).
        # Actually, since we use +A for inhibition in J, and +A for linear penalty in h (from (sum x - 1)^2 = sum x^2 - 2 sum x + 1 => -2A linear + A quadratic),
        # Wait, my previous derivation:
        # H_row = A * (sum x - 1)^2 = A * (sum x^2 + cross_terms - 2 sum x + 1)
        # Linear term was -A (derived from A * x^2 - 2A * x = -A * x).
        # Wait, A * x^2 - 2A * x = A * x - 2A * x = -A * x. Correct.
        # But I changed it to +A in the previous step because I thought "E = -h^T x".
        # If H_linear = -A * x, and E = -h * x, then h = A. Correct.
        # So to encourage x_{0,0}=1, we need to lower the energy for x_{0,0}=1.
        # Current linear energy contribution is -h_{0,0} * 1 = -A.
        # We want to make it even lower.
        # Let's add a large value to h_{0,0}.
        # self.h[idx(0,0)] += A * 2
        
        self.h[idx(0, 0)] += A * 2

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize TSP solution.
        """
        import networkx as nx
        
        N = self.n_cities
        x = (result.solution >= threshold).astype(int)
        
        # Decode solution
        tour_order = {}
        tour_sequence = []
        
        valid = True
        for t in range(N):
            cities = [i for i in range(N) if x[i*N + t] == 1]
            if len(cities) == 1:
                city = cities[0]
                tour_order[city] = t
                tour_sequence.append(city)
            else:
                valid = False
                # print(f"Step {t}: Invalid number of cities {cities}")
                
        # Create Graph for visualization
        G = nx.Graph()
        G.add_nodes_from(range(N))
        
        # Add edges from distance matrix (only "finite" ones)
        # We assume large values (> mean + 3std or fixed threshold) are missing edges
        # Or we just plot all edges with transparency?
        # User said: "If no edge, distance is infinite".
        # Let's infer "infinite" as > 50 (based on notebook example where max random weight is 10)
        # Or better, just use the weights provided.
        
        edge_labels = {}
        for i in range(N):
            for j in range(i + 1, N):
                w = self.distance_matrix[i, j]
                if w < 50.0: # Heuristic threshold
                    G.add_edge(i, j, weight=w)
                    edge_labels[(i, j)] = f"{w:.1f}"
                    
        pos = nx.spring_layout(G, seed=42)
        
        plt.figure(figsize=(8, 8))
        
        # Draw base graph
        nx.draw(G, pos, with_labels=False, node_color='lightgray', node_size=500, alpha=0.5)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, alpha=0.5)
        
        if valid and len(set(tour_sequence)) == N:
            # Calculate Cost
            cost = 0
            tour_edges = []
            for t in range(N):
                u = tour_sequence[t]
                v = tour_sequence[(t+1)%N]
                d = self.distance_matrix[u, v]
                cost += d
                if G.has_edge(u, v):
                    tour_edges.append((u, v))
                else:
                    # Virtual edge for visualization if missing
                    tour_edges.append((u, v))
            
            # Draw Tour
            nx.draw_networkx_edges(G, pos, edgelist=tour_edges, edge_color='red', width=2)
            
            # Labels: City ID + Order
            node_labels = {i: f"{i}\\n({tour_order.get(i, '?')})" for i in range(N)}
            nx.draw_networkx_labels(G, pos, labels=node_labels)
            
            plt.title(f"TSP Tour (Cost: {cost:.1f})\nStart: City 0")
        else:
            nx.draw_networkx_labels(G, pos)
            plt.title(f"Invalid Tour Found\nValid Steps: {len(tour_sequence)}/{N}")
            
        plt.axis('off')
        plt.show()
