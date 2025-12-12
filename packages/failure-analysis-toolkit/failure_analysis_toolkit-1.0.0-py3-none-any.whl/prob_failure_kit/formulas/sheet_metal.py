import numpy as np

def shearing_force(shear_strength: float, perimeter: float, thickness: float) -> float:
    """
    Calculate force required to shear sheet metal.
    F = S * L * t
    
    Args:
        shear_strength (float): Shear strength of material (Pa)
        perimeter (float): Length of cut (m)
        thickness (float): Thickness of sheet (m)
        
    Returns:
        float: Shearing force (N)
    """
    return shear_strength * perimeter * thickness

def bending_force_v_die(tensile_strength: float, width: float, thickness: float, die_opening: float, k_factor: float = 1.33) -> float:
    """
    Calculate bending force for V-die.
    F = (k * UTS * L * t^2) / W
    
    Args:
        tensile_strength (float): Ultimate Tensile Strength (Pa)
        width (float): Width of the bend (Length of bend) (m)
        thickness (float): Thickness of sheet (m)
        die_opening (float): Width of die opening (m)
        k_factor (float): Die opening factor (typically 1.33 for V-die)
        
    Returns:
        float: Bending force (N)
    """
    return (k_factor * tensile_strength * width * thickness**2) / die_opening
