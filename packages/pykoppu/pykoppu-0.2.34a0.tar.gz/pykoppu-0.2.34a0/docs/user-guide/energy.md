# Energy Problems

Optimize operations in the Energy and Oil & Gas sector.

## Well Placement

Select optimal oil well locations to maximize production value under budget and distance constraints.

```python
from pykoppu.problems.energy import WellPlacement
from pykoppu.oos import Process

locations = [
    {'id': 0, 'x': 0, 'y': 0, 'value': 10, 'cost': 5},
    {'id': 1, 'x': 0, 'y': 1, 'value': 20, 'cost': 5},
    # ...
]

problem = WellPlacement(locations, budget=50, min_dist=1.5)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

problem.plot(result, threshold=0.5)
```

## Seismic Feature Selection

Select optimal seismic attributes for reservoir characterization (mRMR).

```python
from pykoppu.problems.energy import SeismicFeatureSelection
from pykoppu.oos import Process

relevance = [1.0, 0.9, 0.5]
redundancy = [[1.0, 0.9, 0.1], [0.9, 1.0, 0.2], [0.1, 0.2, 1.0]]

# Select k=2 features
problem = SeismicFeatureSelection(relevance, redundancy, k=2)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

problem.plot(result, threshold=0.5)
```
