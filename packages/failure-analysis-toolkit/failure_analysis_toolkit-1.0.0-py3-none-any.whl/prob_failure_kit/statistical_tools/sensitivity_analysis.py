import numpy as np
from scipy.stats import spearmanr

def calculate_sensitivity(inputs: dict, outputs: np.ndarray) -> dict:
    """
    Calculate sensitivity using Spearman rank correlation.
    
    Args:
        inputs (dict): Dictionary of input arrays used in simulation.
        outputs (np.ndarray): Array of simulation results.
        
    Returns:
        dict: Dictionary mapping input names to correlation coefficients.
    """
    sensitivity = {}
    for name, values in inputs.items():
        # Calculate Spearman correlation
        corr, _ = spearmanr(values, outputs)
        sensitivity[name] = corr
        
    return sensitivity

# Note: To use this effectively, we need to access the generated input arrays from the simulation.
# We might need to modify MonteCarloSimulation to store or return the input arrays.
