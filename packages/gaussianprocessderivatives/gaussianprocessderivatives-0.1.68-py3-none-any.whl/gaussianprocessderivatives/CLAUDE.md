# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python package for smoothing data and estimating first- and second-order derivatives using Gaussian processes. The package implements various covariance functions based on Rasmussen and Williams (2006).

## Development Commands

### Testing
```bash
python ../test_gp.py
```
The test file demonstrates basic functionality with synthetic sine wave data.

### Code Formatting
```bash
poetry run black --line-length 79 .
```
Black formatting is configured with 79-character line length in pyproject.toml.

### Building and Distribution
```bash
poetry build
```
Poetry is used for package management and building. The dist/ folder contains built packages.

## Architecture and Key Components

### Core Base Class
- `gaussianprocess.py` - Contains the base `gaussianprocess` class that all GP implementations inherit from
- Implements core GP functionality including hyperparameter optimization, prediction, and sampling
- Uses scipy.optimize.minimize for hyperparameter optimization
- Handles measurement noise as the final hyperparameter

### Covariance Function Implementations
Each covariance function is implemented as a separate class inheriting from `gaussianprocess`:

- `maternGP.py` - Twice differentiable Matern kernel (3 hyperparameters: amplitude, stiffness, measurement error)
- `sqexpGP.py` - Squared exponential kernel
- `sqexplinGP.py` - Squared exponential with linear trend
- `linGP.py` - Linear covariance function
- `nnGP.py` - Neural network-like kernel
- `periodicGP.py` - Periodic covariance function
- `localperiodicGP.py` - Locally periodic kernel
- `spectralmixingGP.py` - Spectral mixing kernel

Each class implements:
- `covfn(x, xp, lth)` method returning kernel values and Jacobians
- `info` property explaining hyperparameters
- `noparams` class attribute specifying number of hyperparameters

### Key Methods and Workflow
1. Instantiate GP with hyperparameter bounds: `g = gp.maternGP({0: (-4, 4), 1: (-4, 4), 2: (-4, -2)}, x, y)`
2. Optimize hyperparameters: `g.findhyperparameters()`
3. Display results: `g.results()`  
4. Make predictions: `g.predict(x, derivs=2)` (derivs=0,1,2 for function, 1st, 2nd derivatives)
5. Visualize: `g.sketch('.')` with optional `derivs` parameter

### Data Access
After prediction:
- `g.f`, `g.fvar` - smoothed function and variance
- `g.df`, `g.dfvar` - first derivative and variance  
- `g.ddf`, `g.ddfvar` - second derivative and variance

### Hyperparameter Specification
- Bounds specified in log10 space as dictionary: `{param_index: (lower_bound, upper_bound)}`
- Example: `{0: (-4, 4)}` means parameter bounds are 1e-4 to 1e4
- Final parameter is always measurement noise variance

### Exception Handling
- `gaussianprocessException` is available for GP-specific errors