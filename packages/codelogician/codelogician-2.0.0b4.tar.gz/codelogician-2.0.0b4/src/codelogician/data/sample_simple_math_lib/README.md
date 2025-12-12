# Sample Simple Math Library

A minimal pure Python mathematical computation library with simple directory structure.

## Structure

```
sample_simple_math_lib/
├── __init__.py
├── basic.py          # Level 1: Basic arithmetic (no dependencies)
├── math_ops.py       # Level 2: Math operations (depends on basic.py)
└── utils/            # Package for utilities
    ├── __init__.py
    └── helpers.py     # Level 2: Helper functions (depends on basic.py, math_ops.py)
```

## Dependency Hierarchy

**Level 1: Basic Operations**
- `basic.py` - No dependencies
  - Functions: `add()`, `subtract()`, `multiply()`, `divide()`, `is_positive()`, `absolute()`

**Level 2: Mathematical Operations & Utilities**
- `math_ops.py` - Depends on: `basic.py`
  - Functions: `square()`, `power()`, `sqrt_approx()`, `distance()`, `average()`

- `utils/helpers.py` - Depends on: `basic.py`, `math_ops.py`
  - Functions: `sum_three()`, `max_of_three()`, `circle_area()`, `cube_volume()`, `is_even()`

## Features

- **Simple Structure**: Minimal directory hierarchy with only one subpackage
- **Pure Functions**: All functions are simple and mathematically pure
- **Clear Dependencies**: Two-level dependency hierarchy
- **No Third-Party Dependencies**: Only uses built-in Python features
- **Easy to Understand**: Simple functions, mostly 3-5 lines each

## Usage

```python
# Import from modules
from basic import add, multiply, divide
from math_ops import square, power, sqrt_approx, distance
from utils.helpers import sum_three, circle_area, cube_volume

# Basic usage
result = add(5, 3)                    # 8
squared = square(4)                   # 16
power_result = power(2, 3)            # 8
distance_2d = distance(0, 0, 3, 4)    # 5.0

# Utility functions
total = sum_three(1, 2, 3)            # 6
area = circle_area(5)                 # ~78.54
volume = cube_volume(3)               # 27
```

This library serves as a simple test case for dependency analysis tools with minimal complexity.