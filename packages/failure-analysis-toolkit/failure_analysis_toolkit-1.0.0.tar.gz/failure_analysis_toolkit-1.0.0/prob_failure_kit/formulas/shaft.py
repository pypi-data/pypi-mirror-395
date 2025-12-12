import numpy as np

def torsional_shear_stress(torque: float, radius: float, J: float) -> float:
    """
    Calculate torsional shear stress in a shaft.
    tau = (T * r) / J
    
    Args:
        torque (float): Torque applied (N*m)
        radius (float): Radius of the shaft (m)
        J (float): Polar moment of inertia (m^4)
        
    Returns:
        float: Torsional shear stress (Pa)
    """
    return (torque * radius) / J

def polar_moment_of_inertia_solid(diameter: float) -> float:
    """
    Calculate polar moment of inertia for a solid shaft.
    J = (pi * d^4) / 32
    
    Args:
        diameter (float): Diameter of the shaft (m)
        
    Returns:
        float: Polar moment of inertia (m^4)
    """
    return (np.pi * diameter**4) / 32

def von_mises_stress(sigma: float, tau: float) -> float:
    """
    Calculate Von Mises stress for combined loading (simplified).
    sigma_v = sqrt(sigma^2 + 3*tau^2)
    
    Args:
        sigma (float): Normal stress (Pa)
        tau (float): Shear stress (Pa)
        
    Returns:
        float: Von Mises stress (Pa)
    """
    return np.sqrt(sigma**2 + 3 * tau**2)
