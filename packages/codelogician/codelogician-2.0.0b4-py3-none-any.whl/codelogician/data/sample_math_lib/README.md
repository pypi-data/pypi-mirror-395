# Sample Math Library

A pure Python mathematical computation library with complex package structure and clear dependency hierarchy.

## Package Structure

```
sample_math_lib/
├── __init__.py
├── core/                          # Level 1: Core operations
│   ├── __init__.py
│   ├── arithmetic.py              # Basic arithmetic (no deps)
│   ├── comparison.py              # Comparison ops (no deps)  
│   └── advanced.py                # Advanced ops (deps: arithmetic, comparison)
├── stats/                         # Level 2: Statistical operations
│   ├── __init__.py
│   ├── basic.py                   # Basic stats (deps: core.arithmetic, core.comparison)
│   └── measures.py                # Statistical measures (deps: stats.basic, core.advanced)
├── analysis/                      # Level 3: Analysis package
│   ├── __init__.py
│   ├── numerical/                 # Numerical analysis subpackage
│   │   ├── __init__.py
│   │   ├── derivatives.py         # Derivatives (deps: core.arithmetic, core.comparison)
│   │   └── integration.py         # Integration (deps: core.arithmetic, stats.basic)
│   └── optimization/              # Optimization subpackage
│       ├── __init__.py
│       └── root_finding.py        # Root finding (deps: core, stats.measures, analysis.numerical)
└── utils.py                       # Level 3: Utilities (deps: core, stats)
```

## Dependency Hierarchy

**Level 1: Core Package**
- `core/arithmetic.py` - No dependencies
- `core/comparison.py` - No dependencies  
- `core/advanced.py` - Depends on: `core.arithmetic`, `core.comparison`

**Level 2: Stats Package**
- `stats/basic.py` - Depends on: `core.arithmetic`, `core.comparison`
- `stats/measures.py` - Depends on: `stats.basic`, `core.advanced`

**Level 3: Analysis Package & Utils**
- `analysis/numerical/derivatives.py` - Depends on: `core.arithmetic`, `core.comparison`
- `analysis/numerical/integration.py` - Depends on: `core.arithmetic`, `stats.basic`
- `analysis/optimization/root_finding.py` - Depends on: `core`, `stats.measures`, `analysis.numerical.derivatives`
- `utils.py` - Depends on: `core.arithmetic`, `core.advanced`, `stats.basic`, `stats.measures`

## Features

- **Complex Package Structure**: Multiple levels of nested packages with proper `__init__.py` files
- **Pure Functions**: All functions are simple and mathematically pure
- **Clear Dependencies**: Three-level dependency hierarchy across packages
- **No Third-Party Dependencies**: Only uses built-in Python features
- **Realistic Structure**: Mimics real-world Python package organization

## Usage

```python
# Import from packages
from core.arithmetic import add, multiply
from core.advanced import square_root, factorial
from stats.basic import mean, sum_list
from stats.measures import variance, standard_deviation
from analysis.numerical.derivatives import numerical_derivative
from analysis.optimization.root_finding import bisection_method
from utils import polynomial_evaluate, normalize_data

# Usage examples
result = add(5, 3)                    # 8
sqrt_val = square_root(16)            # 4.0
avg = mean([1, 2, 3, 4, 5])          # 3.0
std_dev = standard_deviation([1, 2, 3, 4, 5])
```

This library serves as a comprehensive test case for dependency analysis tools with realistic package structure and cross-package dependencies.