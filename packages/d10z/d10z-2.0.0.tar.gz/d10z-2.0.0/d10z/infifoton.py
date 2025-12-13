import numpy as np
from typing import Optional
from .constants import Constants

class Infifoton:
    """
    Partícula fundamental del Omniverso.

    Unidad discreta de información-energía en el TTA mesh a escala GM.
    """

    def __init__(
        self,
        frequency: float = 1.0,
        phase: float = 0.0,
        position: Optional[np.ndarray] = None,
    ):
        self.frequency = float(frequency)
        self.phase = float(phase)
        self.position = (
            np.array(position, dtype=float)
            if position is not None
            else np.zeros(10, dtype=float)
        )

    def energy(self) -> float:
        """E ~ ħ·f en escala efectiva GM."""
        return Constants.hbar * self.frequency

    def wavefunction(self, t: float) -> complex:
        """ψ(t) = exp(i(2π f t + φ))."""
        return np.exp(1j * (2 * np.pi * self.frequency * t + self.phase))

    def couple(self, other: "Infifoton") -> float:
        """
        Acoplamiento C_ij = cos(2πΔf) · exp(-|r_i - r_j|/λ_GM).
        """
        delta_f = abs(self.frequency - other.frequency)
        distance = np.linalg.norm(self.position - other.position)
        coupling = np.cos(2 * np.pi * delta_f) * np.exp(-distance / Constants.GM_SCALE)
        return float(coupling)
