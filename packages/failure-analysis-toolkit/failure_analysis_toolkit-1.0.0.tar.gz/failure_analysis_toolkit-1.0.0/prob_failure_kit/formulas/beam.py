import numpy as np

def bending_stress(moment: float, y: float, I: float) -> float:
    """
    Calculate bending stress in a beam.
    sigma = (M * y) / I
    
    Args:
        moment (float): Bending moment (N*m)
        y (float): Distance from neutral axis (m)
        I (float): Moment of inertia (m^4)
        
    Returns:
        float: Bending stress (Pa)
    """
    return (moment * y) / I

def deflection_cantilever_end_load(force: float, length: float, E: float, I: float) -> float:
    """
    Calculate maximum deflection of a cantilever beam with end load.
    delta = (F * L^3) / (3 * E * I)
    
    Args:
        force (float): Load at the end (N)
        length (float): Length of the beam (m)
        E (float): Modulus of Elasticity (Pa)
        I (float): Moment of inertia (m^4)
        
    Returns:
        float: Maximum deflection (m)
    """
    return (force * length**3) / (3 * E * I)

def rectangular_moment_of_inertia(width: float, height: float) -> float:
    """
    Calculate moment of inertia for a rectangular section.
    I = (b * h^3) / 12
    
    Args:
        width (float): Width of the section (m)
        height (float): Height of the section (m)
        
    Returns:
        float: Moment of inertia (m^4)
    """
    return (width * height**3) / 12
