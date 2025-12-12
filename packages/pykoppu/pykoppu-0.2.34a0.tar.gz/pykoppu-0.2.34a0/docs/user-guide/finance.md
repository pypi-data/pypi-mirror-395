# Finance Problems

Optimize financial portfolios.

## Portfolio Optimization

Select assets to maximize expected return while minimizing risk (variance).

```python
import numpy as np
from pykoppu.problems.finance import PortfolioOptimization
from pykoppu.oos import Process

# Expected returns
mu = np.array([0.1, 0.2, 0.15])
# Covariance matrix (Risk)
sigma = np.array([
    [0.01, 0.001, 0.0],
    [0.001, 0.04, 0.002],
    [0.0, 0.002, 0.02]
])

problem = PortfolioOptimization(mu, sigma, risk_aversion=1.0, budget=2)
process = Process(problem, backend='cpu', t=1000)
result = process.run()

problem.plot(result, threshold=0.5)
```
