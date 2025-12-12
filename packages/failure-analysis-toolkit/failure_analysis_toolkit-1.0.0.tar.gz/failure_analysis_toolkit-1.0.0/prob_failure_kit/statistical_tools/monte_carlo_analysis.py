import numpy as np
from typing import Callable, Dict, List, Any

class MonteCarloSimulation:
    def __init__(self, function: Callable, num_simulations: int = 10000):
        """
        Initialize Monte Carlo Simulation.
        
        Args:
            function (Callable): The function to evaluate (e.g., stress calculation).
            num_simulations (int): Number of iterations.
        """
        self.function = function
        self.num_simulations = num_simulations
        self.inputs = {}
        self.results = None

    def add_input(self, name: str, distribution: str, **params):
        """
        Add an input variable with a probability distribution.
        
        Args:
            name (str): Name of the argument in the function.
            distribution (str): 'normal', 'uniform', 'triangular'.
            **params: Parameters for the distribution (e.g., loc, scale for normal).
        """
        self.inputs[name] = {'dist': distribution, 'params': params}

    def run(self) -> np.ndarray:
        """
        Run the simulation.
        
        Returns:
            np.ndarray: Array of results.
        """
        input_values = {}
        for name, config in self.inputs.items():
            dist = config['dist']
            params = config['params']
            
            if dist == 'normal':
                # loc=mean, scale=std_dev
                input_values[name] = np.random.normal(params['loc'], params['scale'], self.num_simulations)
            elif dist == 'uniform':
                # low, high
                input_values[name] = np.random.uniform(params['low'], params['high'], self.num_simulations)
            elif dist == 'triangular':
                # left, mode, right
                input_values[name] = np.random.triangular(params['left'], params['mode'], params['right'], self.num_simulations)
            else:
                raise ValueError(f"Unsupported distribution: {dist}")
        
        # Store input history for sensitivity analysis
        self.input_history = input_values
        
        # Vectorized evaluation if function supports it, otherwise loop
        # Assuming function can handle numpy arrays (vectorized)
        try:
            self.results = self.function(**input_values)
        except Exception:
            # Fallback to loop if function is not vectorized
            # This is slower but safer
            results_list = []
            for i in range(self.num_simulations):
                args = {k: v[i] for k, v in input_values.items()}
                results_list.append(self.function(**args))
            self.results = np.array(results_list)
            
        return self.results
