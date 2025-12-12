# Math Problems

PyKoppu supports solving fundamental mathematical problems using QUBO formulations.

## Integer Factorization

Decompose a composite number $N$ into its prime factors $p$ and $q$.

```python
from pykoppu.problems.math import Factorization
from pykoppu.oos import Process

# Factor 15
problem = Factorization(target=15)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

# Visualize
problem.plot(result, threshold=0.5)
```

## 3-SAT (Boolean Satisfiability)

Find a satisfying assignment for a boolean formula in Conjunctive Normal Form (CNF).

```python
from pykoppu.problems.math import SAT3
from pykoppu.oos import Process

# Define clauses: (x0 OR x1 OR NOT x2) AND ...
clauses = [
    (0, 1, -2),
    (-0, -1, 2)
]
problem = SAT3(clauses)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

# Visualize
problem.plot(result, threshold=0.5)
```
