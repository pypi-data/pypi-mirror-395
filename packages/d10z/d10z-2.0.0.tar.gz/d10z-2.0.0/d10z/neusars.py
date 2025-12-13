import numpy as np
from scipy.linalg import expm
from typing import Optional

def hilbert_state(n: int, seed: Optional[int] = None) -> np.ndarray:
    """Estado cuántico aleatorio normalizado en C^n."""
    if seed is not None:
        np.random.seed(seed)
    psi = np.random.rand(n) + 1j * np.random.rand(n)
    return psi / np.linalg.norm(psi)

class Neusar:
    """
    Neusar: operador de procesamiento cuántico no local.
    """

    def __init__(self, state: np.ndarray):
        self.state = state / np.linalg.norm(state)

    def operator(self) -> np.ndarray:
        """Proyector |ψ><ψ|."""
        psi = self.state
        return np.outer(psi, psi.conj())

    def process(self, psi_in: np.ndarray) -> np.ndarray:
        """
        |ψ_out> = (|ψ_neusar| / ||ψ_neusar||) · |ψ_in>
        Aquí modelado como proyección:
        """
        P = self.operator()
        out = P @ psi_in
        norm = np.linalg.norm(out)
        return out / norm if norm > 0 else out

    @staticmethod
    def evolve_state(psi: np.ndarray, H: np.ndarray, dt: float) -> np.ndarray:
        U = expm(-1j * H * dt)
        return U @ psi
