# PyHUBO

**A Python package for resource-efficient quantum optimization**

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.1-green.svg)](https://pypi.org/project/pyhubo/)

PyHUBO provides an elegant mathematical framework for designing Higher-order Unconstrained Binary Optimization (HUBO) Hamiltonians for combinatorial optimization problems. Unlike traditional QUBO formulations, PyHUBO enables natural representation of complex constraints and objectives through higher-order interactions\.

## Why HUBO over QUBO?

Traditional QUBO (Quadratic Unconstrained Binary Optimization) formulations often require auxiliary variables and penalty methods limiting parameter optimization for example in QAOA, resulting in suboptimal solutions and extensive quantum resources. HUBO models can circumvent these limitations, enabling:

- **Natural problem representation** without penalty terms
- **Reduced quantum resource requirements** through more efficient encodings
- **Direct modeling** of multi-variable constraints and higher-order relationships
- **Seamless integration** with quantum annealers and classical optimization solvers

## Key Features

- **Intuitive Mathematical Interface**: Build optimization problems using natural mathematical expressions
- **Automatic Constraint Handling**: Built-in conflict resolution and validation
- **Flexible Variable Domains**: Support for discrete variables with arbitrary value sets
- **Quantum Integration**: Direct conversion to quantum Hamiltonian representations
- **Multiple Solver Examples**: Openjij and pennylane implementations are shown in [example](#examples) scripts

## Installation

Install PyHUBO from PyPI:

```bash
pip install pyhubo
```

## Examples
We illustrate the usage of Pyhubo on three distinct combinatorial optimization problems:

- [Gate Assignment Problem](./examples/gap.ipynb)
- [Integer Programming](./examples/ip.ipynb)
- [Maximum k-colorable Subgraph Problem](./examples/mkcs.ipynb)

An example for dealing with problems where the domain size is not to the power of two is also given in the [Maximum k-colorable Subgraph Problem](./examples/mkcs.ipynb) script.

## Issues
Please email me (frederik.koch@uni-hamburg.de) in case you spot any issues or if you have any suggestions to improve pyhubo.

## Citation
Citation for this work is provided in the GitHub repository ("About > Cite this repository").