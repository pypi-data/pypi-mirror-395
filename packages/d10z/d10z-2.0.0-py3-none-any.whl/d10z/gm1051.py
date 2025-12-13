"""
Pilar GM10⁻⁵¹: sistema de unidades y escala fundamental.
"""

from .constants import Constants

def gm_length() -> float:
    """Longitud GM básica [m]."""
    return Constants.GM_SCALE

def gm_time() -> float:
    """Tiempo GM básico [s]."""
    return Constants.GM_TIME

def gm_mass() -> float:
    """Masa GM efectiva (escala) [kg]."""
    # m ~ ħ / (c·GM)
    return Constants.hbar / (Constants.c * Constants.GM_SCALE)

def gm_energy() -> float:
    """Energía GM básica [J]."""
    m = gm_mass()
    return m * Constants.c**2

def icgm_from_scale(log10_Zn: int) -> float:
    """
    ICGM aproximado según escala log10(Zn) (jerarquía fractal).
    Tabla simbólica; ajusta con tus valores reales.
    """
    table = {
        -51: -50.20,
        -35: -20.15,
        -15: 93.80,
        -10: 102.40,
        -7: 125.80,
         0: 142.30,
         7: 163.70,
        13: 189.20,
        21: 224.60,
        26: 241.80,
    }
    return table.get(int(log10_Zn), 0.0)
