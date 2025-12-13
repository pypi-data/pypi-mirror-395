from typing import List, Callable
import numpy as np

def N_pillar(
    x: float,
    t: float,
    alphas: List[float],
    phis: List[Callable[[float], float]],
    I: Callable[[float], float],
    tis: List[float],
) -> float:
    """
    Pilar N – Nodal Intelligence

    N(x,t) = Σ α_i · φ_i(x) · I(t - t_i)
    """
    return float(
        sum(alpha * phi(x) * I(t - ti)
            for alpha, phi, ti in zip(alphas, phis, tis))
    )

def ZN_interaction(
    x: float,
    t: float,
    Z_val: complex,
    N_val: float,
    alphas,
    phis,
    I,
    tis,
    use_gradient: bool = False,
    dx: float = 1e-4,
) -> float:
    """
    Interacción Z ⊗ N.

    Opciones:
    - simple: Ω = |Z| · N
    - con gradiente: Ω = Re(Z)·N + Im(Z)·∇N
    """
    if not use_gradient:
        return abs(Z_val) * N_val

    N_plus = N_pillar(x + dx, t, alphas, phis, I, tis)
    N_minus = N_pillar(x - dx, t, alphas, phis, I, tis)
    grad_N = (N_plus - N_minus) / (2 * dx)
    return Z_val.real * N_val + Z_val.imag * grad_N
