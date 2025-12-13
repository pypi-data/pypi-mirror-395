import numpy as np
from .constants import Constants
from .infifoton import Infifoton

class TTAMesh:
    """
    TTA (Trama Tejido Tela de Araña) - malla vibracional fundamental.
    """

    def __init__(
        self,
        N: int = 1000,
        dimension: int = 10,
        resolution: float = Constants.GM_SCALE,
    ):
        self.N = int(N)
        self.dimension = int(dimension)
        self.resolution = float(resolution)

        self.nodes = [
            Infifoton(
                frequency=Constants.SCHUMANN_BASE * np.random.rand(),
                position=np.random.rand(dimension) * self.resolution,
            )
            for _ in range(self.N)
        ]

        self.C_ij = self._compute_connectivity()

    def _compute_connectivity(self) -> np.ndarray:
        if self.N == 0:
            return np.zeros((0, 0), dtype=float)
        positions = np.array([n.position for n in self.nodes])
        diff = positions[:, None, :] - positions[None, :, :]
        distances = np.linalg.norm(diff, axis=2)
        return np.exp(-distances / self.resolution)

    def density(self, position: np.ndarray) -> float:
        position = np.array(position, dtype=float)
        if self.N == 0:
            return 0.0
        val = 0.0
        for node in self.nodes:
            d = np.linalg.norm(position - node.position)
            val += np.exp(-d / self.resolution) * node.frequency
        return float(val)

    def lambda2(self) -> float:
        """Segundo eigenvalor del Laplaciano (coherencia algebraica)."""
        if self.N == 0:
            return 0.0
        degrees = np.sum(self.C_ij, axis=1)
        D = np.diag(degrees)
        L = D - self.C_ij
        eigenvalues = np.linalg.eigvalsh(L)
        if len(eigenvalues) < 2:
            return 0.0
        return float(eigenvalues[1])
