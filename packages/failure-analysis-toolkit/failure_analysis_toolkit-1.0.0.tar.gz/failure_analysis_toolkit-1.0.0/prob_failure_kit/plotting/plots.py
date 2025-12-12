import matplotlib.pyplot as plt
import numpy as np

def plot_distribution(data: np.ndarray, title: str = "Distribution", xlabel: str = "Value", ylabel: str = "Frequency", save_path: str = None):
    """
    Plot histogram of the data.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def plot_sensitivity(sensitivity_dict: dict, title: str = "Sensitivity Analysis", save_path: str = None):
    """
    Plot bar chart of sensitivity indices.
    """
    names = list(sensitivity_dict.keys())
    values = list(sensitivity_dict.values())
    
    # Sort by absolute value
    sorted_indices = np.argsort(np.abs(values))
    names = [names[i] for i in sorted_indices]
    values = [values[i] for i in sorted_indices]
    
    plt.figure(figsize=(10, 6))
    plt.barh(names, values, color='green')
    plt.title(title)
    plt.xlabel("Spearman Correlation Coefficient")
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
