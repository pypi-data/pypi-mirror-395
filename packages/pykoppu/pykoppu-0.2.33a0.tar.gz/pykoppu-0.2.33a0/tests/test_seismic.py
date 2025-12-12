import sys
import os
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pykoppu.problems.energy.seismic import SeismicFeatureSelection

def test_seismic_feature_selection():
    print("Testing Seismic Feature Selection...")
    
    # 5 Features
    # F0: High Relevance (1.0), Low Redundancy
    # F1: High Relevance (0.9), High Redundancy with F0
    # F2: Med Relevance (0.5), Low Redundancy
    # F3: Low Relevance (0.1), Low Redundancy
    # F4: High Relevance (0.8), Low Redundancy
    
    relevance = np.array([1.0, 0.9, 0.5, 0.1, 0.8])
    
    # Redundancy Matrix (Symmetric)
    # F0 and F1 are highly correlated (0.9)
    redundancy = np.zeros((5, 5))
    redundancy[0, 1] = redundancy[1, 0] = 0.9
    
    # Scenario 1: Select k=2
    # Option A: {F0, F1} -> Rel=1.9, Red=0.9. Score = 1.9 - 0.9 = 1.0
    # Option B: {F0, F4} -> Rel=1.8, Red=0.0. Score = 1.8 - 0.0 = 1.8 (BETTER)
    # Option C: {F1, F4} -> Rel=1.7, Red=0.0. Score = 1.7
    
    print("\nScenario 1: k=2, alpha=1, beta=1")
    problem = SeismicFeatureSelection(relevance, redundancy, k=2, alpha=1.0, beta=1.0)
    
    # Test Option A (0, 1)
    sol_a = np.array([1, 1, 0, 0, 0])
    metrics_a = problem.evaluate(sol_a)
    print(f"Option A (0,1): Score={metrics_a['mrmr_score']:.2f}, Valid={metrics_a['valid']}")
    
    # Test Option B (0, 4)
    sol_b = np.array([1, 0, 0, 0, 1])
    metrics_b = problem.evaluate(sol_b)
    print(f"Option B (0,4): Score={metrics_b['mrmr_score']:.2f}, Valid={metrics_b['valid']}")
    
    if metrics_b['mrmr_score'] > metrics_a['mrmr_score']:
        print("SUCCESS: Algorithm prefers low redundancy (Option B > Option A).")
    else:
        print("FAILURE: Algorithm failed to penalize redundancy.")
        
    # Scenario 2: Cardinality Check
    # Select k=3
    print("\nScenario 2: k=3")
    problem2 = SeismicFeatureSelection(relevance, redundancy, k=3)
    
    # Test valid k=3
    sol_valid = np.array([1, 0, 1, 0, 1]) # 0, 2, 4
    metrics_valid = problem2.evaluate(sol_valid)
    print(f"Solution (0,2,4) Valid? {metrics_valid['valid']}")
    
    # Test invalid k=2
    sol_invalid = np.array([1, 0, 0, 0, 1]) # 0, 4
    metrics_invalid = problem2.evaluate(sol_invalid)
    print(f"Solution (0,4) Valid? {metrics_invalid['valid']} (Should be False)")
    
    if metrics_valid['valid'] and not metrics_invalid['valid']:
        print("SUCCESS: Cardinality constraint works.")
    else:
        print("FAILURE: Cardinality constraint failed.")

if __name__ == "__main__":
    test_seismic_feature_selection()
