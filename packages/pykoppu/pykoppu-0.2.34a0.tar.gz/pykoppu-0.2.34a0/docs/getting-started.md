# Getting Started

This guide will help you set up PyKoppu and run your first simulation.

## Installation

PyKoppu requires Python 3.8 or later. Install it via pip:

```bash
pip install pykoppu
```

## Core Concepts

PyKoppu follows a simple 3-step workflow:

1.  **Define a Problem**: Instantiate a problem class (e.g., `Factorization`, `TSP`, `MaxCut`).
2.  **Create a Process**: Wrap the problem in a `Process` to manage compilation and execution.
3.  **Run & Analyze**: Execute the process to get a `SimulationResult`, then visualize it.

## Hello World: Factoring 15

Let's solve a classic integer factorization problem: finding the prime factors of 15.

```python
import pykoppu as pk

# 1. Define the Problem
# We want to find p, q such that p * q = 15
problem = pk.problems.math.Factorization(target=15)

# 2. Create a Process
# We use the CPU backend for simulation
process = pk.oos.Process(problem, backend='cpu', t=1000)

# 3. Run the Simulation
result = process.run()

# 4. Visualize Results
problem.plot(result, threshold=0.5)

# 5. Inspect Solution
metrics = problem.evaluate(result.solution)
print(f"Factors: {metrics['p']} * {metrics['q']} = {metrics['product']}")
```

## Next Steps

Explore specific problem domains in the User Guide:

- [Math Problems](user-guide/math.md) (Factorization, SAT)
- [Graph Problems](user-guide/graph.md) (MaxCut)
- [Logistics](user-guide/logistics.md) (TSP, Knapsack)
- [Finance](user-guide/finance.md) (Portfolio Optimization)
- [Energy](user-guide/energy.md) (Well Placement, Seismic Feature Selection)
