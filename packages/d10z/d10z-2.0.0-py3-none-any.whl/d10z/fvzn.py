import numpy as np
from .constants import Constants

def f_from_frequency(frequency: float) -> float:
    """Identidad: f es la frecuencia característica [Hz]."""
    return float(frequency)

def v_from_zn(Zn: float, icgm: float = 1.0) -> float:
    """
    v(Zn): velocidad efectiva ligada a la escala Zn.
    Modelo simple: v = c · tanh(icgm · Zn / L_GM)
    """
    Zn = float(Zn)
    arg = icgm * Zn / (Constants.GM_SCALE + 1e-60)
    return float(Constants.c * np.tanh(arg))

def fv_universal(frequency: float, Zn: float, icgm: float = 1.0) -> float:
    """
    Pilar F = f·v(Zn) (magnitud adimensionalizada / J escalares).
    """
    f = f_from_frequency(frequency)
    v = v_from_zn(Zn, icgm=icgm)
    return float(f * v)
