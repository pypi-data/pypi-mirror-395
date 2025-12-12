# Graph Problems

Solve combinatorial optimization problems on graphs.

## MaxCut

Partition the nodes of a graph into two sets to maximize the number of edges between them.

```python
import networkx as nx
from pykoppu.problems.graph import MaxCut
from pykoppu.oos import Process

# Create a graph
G = nx.erdos_renyi_graph(n=10, p=0.5)

# Define problem
problem = MaxCut(G)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

# Visualize
problem.plot(result, threshold=0.5)
```
