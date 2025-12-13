import numpy as np
from scipy.integrate import quad
from typing import Callable, Tuple

def Z_pillar(
    x: float,
    t: float,
    Z0: complex,
    omega: Callable[[float], float],
    psi_n: Callable[[float], float],
    gamma: Tuple[float, float],
) -> complex:
    """
    Pilar Z – Dimensional Connectivity

    Z(x,t) = Z0 · exp(i ∫_γ ω(τ)dτ) · Ψ_n(x)
    """
    phase, _ = quad(omega, gamma[0], gamma[1])
    return Z0 * np.exp(1j * phase) * psi_n(x)
