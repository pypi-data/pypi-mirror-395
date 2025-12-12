import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pykoppu.problems.math.factorization import Factorization
from pykoppu.oos.process import Process
import numpy as np

def test_factorization():
    print("Testing Factorization of 15...")
    # 15 = 3 * 5. Bits needed: 3 = 11 (2 bits), 5 = 101 (3 bits).
    # Let's try explicit bits to be safe.
    problem = Factorization(target=15, p_bits=2, q_bits=3, penalty=10.0)
    
    # Use CPU backend for simulation
    process = Process(problem, backend="cpu", t=100.0)
    
    # Since we don't have a real quantum annealer, we might not find the ground state easily with simple simulation
    # if the landscape is complex. But for small N=15, it might work or we can inspect the Hamiltonian.
    
    # Let's try to find the ground state by brute force evaluation of the Hamiltonian to verify correctness of the model.
    # The solver simulation might be stochastic.
    
    print("Verifying Hamiltonian Ground State...")
    
    # Construct expected solution: p=3 (11), q=5 (101)
    # x = [1, 1] (LSB first? My code: p += 2**i, so index 0 is LSB)
    # x0=1, x1=1 => p=3
    # y = [1, 0, 1] => q=1+4=5
    # z_ij = x_i * y_j
    
    n = 2
    m = 3
    
    x_sol = [1, 1]
    y_sol = [1, 0, 1]
    z_sol = []
    for i in range(n):
        for j in range(m):
            z_sol.append(x_sol[i] * y_sol[j])
            
    full_sol = np.array(x_sol + y_sol + z_sol)
    
    # Calculate Energy
    # E = -0.5 x J x - h x
    J = problem.J
    h = problem.h
    
    E = -0.5 * full_sol.T @ J @ full_sol - h.T @ full_sol
    
    print(f"Energy of valid solution (3*5): {E}")
    print(f"Offset: {problem.offset}") # Wait, offset is not used in E calculation usually, but is part of H value.
    # My code: H = E + offset?
    # H_fact = (N - P)^2. For valid solution, H_fact = 0.
    # H_cons = 0.
    # So Total H should be 0.
    # If E + offset = H, then E should be -offset.
    
    total_H = E + problem.offset
    print(f"Total Hamiltonian Value (should be 0): {total_H}")
    
    if abs(total_H) < 1e-5:
        print("SUCCESS: Ground state energy is correct.")
    else:
        print("FAILURE: Ground state energy is not zero.")
        
    # Also check an invalid solution
    # p=3, q=3 => 9 != 15
    # y = [1, 1, 0]
    y_bad = [1, 1, 0]
    z_bad = []
    for i in range(n):
        for j in range(m):
            z_bad.append(x_sol[i] * y_bad[j])
            
    bad_sol = np.array(x_sol + y_bad + z_bad)
    E_bad = -0.5 * bad_sol.T @ J @ bad_sol - h.T @ bad_sol
    H_bad = E_bad + problem.offset
    print(f"Energy of invalid solution (3*3=9): {H_bad}")
    
    if H_bad > 1e-5:
        print("SUCCESS: Invalid solution has positive energy.")
    else:
        print("FAILURE: Invalid solution has zero energy.")

if __name__ == "__main__":
    test_factorization()
