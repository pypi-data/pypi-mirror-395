# Probabilistic Failure Analysis Toolkit

A Python toolkit for performing probabilistic failure analysis on mechanical components. This tool allows engineers to simulate component behavior under various uncertain conditions (forces, dimensions, material properties) using Monte Carlo simulations.

## Features

*   **Monte Carlo Simulation**: Run thousands of simulations to understand the probability of failure.
*   **Sensitivity Analysis**: Identify which input variables have the biggest impact on your results using Spearman rank correlation.
*   **Engineering Formulas**: Built-in formulas for common mechanical elements:
    *   **Shafts**: Torsional shear stress, Von Mises stress.
    *   **Beams**: Bending stress, deflection.
    *   **Gears**: Lewis bending stress, contact stress.
    *   **Sheet Metal**: Shearing force, bending force.
*   **Visualization**: Generate plots for stress distributions and sensitivity analysis.

## Installation

1.  Clone the repository.
2.  Install the required dependencies:

```bash
pip install numpy matplotlib scipy
```

## Usage

The `demo.py` file contains a complete example of how to use the toolkit to analyze a cantilever beam.

To run the demo:

```bash
python demo.py
```

### Example Code Snippet

```python
from prob_failure_kit.statistical_methods.monte_carlo import MonteCarloSimulation
import numpy as np


# 1. Define your model
def my_stress_model(force, area):
    return force / area


# 2. Setup Simulation
mc = MonteCarloSimulation(my_stress_model)
mc.add_input('force', 'normal', loc=1000, scale=100)
mc.add_input('area', 'normal', loc=0.01, scale=0.001)

# 3. Run
results = mc.run()
print(f"Mean Stress: {np.mean(results)} Pa")
```

## Project Structure

*   `prob_failure/`: Main package directory.
    *   `formulas/`: Engineering formulas for different components.
    *   `statistical_methods/`: Monte Carlo and sensitivity analysis logic.
    *   `plotting/`: Visualization utilities.
*   `demo.py`: Example usage script.
