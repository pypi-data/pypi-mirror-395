import numpy as np
from .constants import Constants

class LeySahana:
    """
    Ley de Sahana – re-equilibrio local:

    dZ/dt = -γ (Z - Z_hat)
    """

    @staticmethod
    def apply(
        Z: np.ndarray,
        C_ij: np.ndarray,
        gamma: float = Constants.GAMMA_SAHANA,
        dt: float = 0.01,
    ) -> np.ndarray:
        Z = np.array(Z, dtype=float)
        C_ij = np.array(C_ij, dtype=float)
        weights = np.sum(C_ij, axis=1) + 1e-10
        Z_hat = (C_ij @ Z) / weights
        dZ_dt = -gamma * (Z - Z_hat)
        return Z + dZ_dt * dt

    @staticmethod
    def equilibrium_time(
        Z0: np.ndarray,
        Z_target: np.ndarray,
        gamma: float = Constants.GAMMA_SAHANA,
    ) -> float:
        Z0 = np.array(Z0, dtype=float)
        Z_target = np.array(Z_target, dtype=float)
        delta = np.linalg.norm(Z0 - Z_target)
        epsilon = 1e-3
        if delta < epsilon:
            return 0.0
        return float((1.0 / gamma) * np.log(delta / epsilon))
