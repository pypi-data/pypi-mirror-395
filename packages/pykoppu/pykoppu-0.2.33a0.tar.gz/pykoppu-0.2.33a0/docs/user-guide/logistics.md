# Logistics Problems

Optimize logistics and resource allocation.

## Traveling Salesperson Problem (TSP)

Find the shortest route visiting a set of cities exactly once and returning to the start.

```python
import numpy as np
from pykoppu.problems.logistics import TSP
from pykoppu.oos import Process

# Distance matrix for 4 cities
distances = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

problem = TSP(distances)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

problem.plot(result, threshold=0.5)
```

## Knapsack Problem

Select items with given weights and values to maximize total value without exceeding capacity.

```python
from pykoppu.problems.logistics import Knapsack
from pykoppu.oos import Process

values = [10, 20, 30]
weights = [5, 10, 15]
capacity = 20

problem = Knapsack(values, weights, capacity)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

problem.plot(result, threshold=0.5)
```
