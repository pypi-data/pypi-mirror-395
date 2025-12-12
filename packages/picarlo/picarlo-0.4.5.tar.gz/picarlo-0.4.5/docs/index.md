# Welcome to Picarlo

**Picarlo** is a high-performance Python library for estimating the value of $\pi$ using the [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method).

It features a hybrid architecture:
- **Python** for flexibility and ease of use.
- **Rust** (via PyO3) for computational speed.

## Features

- 🚀 **Fast**: Core simulation implemented in Rust.
- ⚡ **Parallel**: Multi-process support for utilizing all CPU cores.
- 🐍 **Pythonic**: Easy to use API and CLI.

## Installation

```bash
pip install picarlo
```

## Quick Start

### Command Line

```bash
picarlo --help
picarlo --samples 1000000 --parallel
```

### Python API

```python
from picarlo.sim import monte_carlo_pi

# Estimate Pi with 1 million samples
pi_approx = monte_carlo_pi(1_000_000)
print(f"Pi is approximately {pi_approx}")
```
