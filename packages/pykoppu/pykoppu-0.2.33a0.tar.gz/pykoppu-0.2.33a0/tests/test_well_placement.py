import sys
import os
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pykoppu.problems.energy.well_placement import WellPlacement

def test_well_placement():
    print("Testing Well Placement...")
    
    # Define a small grid of 4 locations
    # (0,0), (0,1), (1,0), (1,1)
    # Distance between adjacent is 1.0. Diagonal is sqrt(2) ~ 1.414.
    locations = [
        {'id': 0, 'x': 0, 'y': 0, 'value': 10, 'cost': 5},
        {'id': 1, 'x': 0, 'y': 1, 'value': 20, 'cost': 5},
        {'id': 2, 'x': 1, 'y': 0, 'value': 30, 'cost': 5},
        {'id': 3, 'x': 1, 'y': 1, 'value': 40, 'cost': 5}
    ]
    
    # Scenario 1: Budget for 2 wells (Cost=10), Min Dist = 0.9 (All compatible)
    # Should pick max value wells: 3 (40) and 2 (30). Total Value = 70.
    print("\nScenario 1: Budget=10, MinDist=0.9")
    problem1 = WellPlacement(locations, budget=10, min_dist=0.9, penalty_budget=10, penalty_dist=10)
    
    # Expected solution: x = [0, 0, 1, 1]
    sol1 = np.array([0, 0, 1, 1])
    metrics1 = problem1.evaluate(sol1)
    
    print(f"Metrics: {metrics1}")
    if metrics1['valid'] and metrics1['total_value'] == 70:
        print("SUCCESS: Scenario 1 passed.")
    else:
        print("FAILURE: Scenario 1 failed.")
        
    # Scenario 2: Budget for 2 wells, Min Dist = 1.1 (Adjacent incompatible)
    # Adjacent pairs dist=1.0 < 1.1. Diagonal dist=1.414 > 1.1.
    # Compatible pairs: (0,3) and (1,2).
    # Pair (0,3): Value 10+40=50.
    # Pair (1,2): Value 20+30=50.
    # Should pick one of these pairs.
    print("\nScenario 2: Budget=10, MinDist=1.1")
    problem2 = WellPlacement(locations, budget=10, min_dist=1.1, penalty_budget=10, penalty_dist=10)
    
    # Test valid solution (0, 3)
    sol2a = np.array([1, 0, 0, 1])
    metrics2a = problem2.evaluate(sol2a)
    print(f"Solution (0,3) Valid? {metrics2a['valid']}")
    
    # Test invalid solution (2, 3) - Adjacent, dist=1.0
    sol2b = np.array([0, 0, 1, 1])
    metrics2b = problem2.evaluate(sol2b)
    print(f"Solution (2,3) Valid? {metrics2b['valid']} (Should be False due to dist)")
    
    if metrics2a['valid'] and not metrics2b['valid']:
        print("SUCCESS: Scenario 2 passed.")
    else:
        print("FAILURE: Scenario 2 failed.")
        
    # Check Hamiltonian Energy for optimal solution in Scenario 1
    # H = -Value + H_budget + H_dist
    # Value = 70. H_value = -70.
    # Cost = 10. Budget = 10. H_budget = P * (10-10)^2 = 0.
    # Dist ok. H_dist = 0.
    # Expected H = -70 + offset?
    # My code: h += values => -h_solver = values => h_solver = -values.
    # E = -0.5 x J x - h x.
    # Let's just check if ground state is minimal.
    
    # Let's verify energy of sol1 in problem1
    J = problem1.J
    h = problem1.h
    E = -0.5 * sol1.T @ J @ sol1 - h.T @ sol1
    H_total = E + problem1.offset
    print(f"\nScenario 1 Energy: {H_total}")
    # Expected: -70 (since offset cancels constant terms in H_budget expansion?)
    # H_budget = P(C-B)^2. If C=B, H_budget=0.
    # H_value = -70.
    # Total = -70.
    
    if abs(H_total - (-70.0)) < 1e-5:
        print("SUCCESS: Energy calculation correct.")
    else:
        print(f"FAILURE: Energy {H_total} != -70.0")

if __name__ == "__main__":
    test_well_placement()
