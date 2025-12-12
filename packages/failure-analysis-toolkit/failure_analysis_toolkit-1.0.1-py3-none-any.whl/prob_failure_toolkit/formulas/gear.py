import numpy as np

def lewis_bending_stress(tangential_load: float, diametral_pitch: float, face_width: float, lewis_form_factor: float) -> float:
    """
    Calculate gear bending stress using Lewis formula.
    sigma = (Wt * P) / (F * Y)
    
    Args:
        tangential_load (float): Tangential load (N) (Wt)
        diametral_pitch (float): Diametral pitch (1/m) (P) - Note: Standard Lewis uses P in 1/in, be careful with units. 
                                 If using SI, usually module 'm' is used: sigma = Wt / (F * m * Y).
                                 Let's assume SI inputs and standard formula sigma = Wt / (F * m * Y) where m = 1/P.
                                 Wait, standard SI form is sigma = Ft / (b * m * Y).
                                 Let's stick to a generic form: sigma = Load / (FaceWidth * Module * FormFactor)
    
    Let's refine to: sigma = Wt / (F * m * Y)
    
    Args:
        tangential_load (float): Tangential load (N)
        module (float): Gear module (m)
        face_width (float): Face width (m)
        lewis_form_factor (float): Lewis form factor (Y)
        
    Returns:
        float: Bending stress (Pa)
    """
    return tangential_load / (face_width * module * lewis_form_factor)

def contact_stress(tangential_load: float, face_width: float, pinion_diameter: float, elastic_coefficient: float, geometry_factor: float) -> float:
    """
    Calculate contact stress (Hertzian stress) in gears.
    sigma_c = Cp * sqrt(Wt / (F * d * I))
    
    Args:
        tangential_load (float): Tangential load (N)
        face_width (float): Face width (m)
        pinion_diameter (float): Pitch diameter of pinion (m)
        elastic_coefficient (float): Elastic coefficient (Cp) (sqrt(Pa))
        geometry_factor (float): Geometry factor (I)
        
    Returns:
        float: Contact stress (Pa)
    """
    return elastic_coefficient * np.sqrt(tangential_load / (face_width * pinion_diameter * geometry_factor))
