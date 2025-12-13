from .constants import Constants
import numpy as np

class UniversalForce:
    """
    Ecuación universal:

    F = f · v · Z_n
    """

    @staticmethod
    def compute(frequency: float, velocity: float, nodal_density: float) -> float:
        return float(frequency * velocity * nodal_density)

    @staticmethod
    def gravitational(M: float, r: float, Z_n: float) -> float:
        if r <= 0:
            raise ValueError("r must be > 0")
        f_grav = np.sqrt(abs(Constants.G * M)) / (2 * np.pi * r)
        v_orb = np.sqrt(abs(Constants.G * M) / r)
        F = UniversalForce.compute(f_grav, v_orb, Z_n)
        return float(F if M >= 0 else -abs(F))
