import numpy as np

class Constants:
    """Constantes fundamentales del framework D10Z."""

    # Escala GM (fundamental)
    GM_SCALE = 1e-51  # metros
    GM_TIME = GM_SCALE / 2.99792458e8  # s

    # Constantes físicas estándar
    G = 6.67430e-11          # m^3 / (kg s^2)
    c = 2.99792458e8         # m/s
    hbar = 1.054571817e-34   # J·s

    # TTA Mesh
    RHO_0 = 1e-60      # kg/m^3
    RHO_1 = 1e-67      # kg/m^3
    PLANCK_D10Z = 1e-102

    # Resonancia planetaria
    SCHUMANN_BASE = 7.83  # Hz

    # Coherencia / leyes
    GAMMA_SAHANA = 0.1
    LAMBDA_MAX = 1.0
    LAMBDA_OPTIMAL = 0.81

    # Cosmología
    ALPHA_UNIVERSAL = 0.042
    ALPHA_STD = 0.003
