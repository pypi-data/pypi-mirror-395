import numpy as np

class LeyIsis:
    """
    Ley de Isis – armonía estructural.

    W = (1/2) Σ_ij C_ij · (Z_i - Z_j)^2 / (Z_i + Z_j)
    """

    @staticmethod
    def tension(Z: np.ndarray, C_ij: np.ndarray) -> float:
        Z = np.array(Z, dtype=float)
        C_ij = np.array(C_ij, dtype=float)
        Z_i = Z[:, None]
        Z_j = Z[None, :]
        denom = Z_i + Z_j + 1e-10
        W_ij = C_ij * (Z_i - Z_j) ** 2 / denom
        return float(0.5 * np.sum(W_ij))

    @staticmethod
    def minimize_tension(
        Z: np.ndarray,
        C_ij: np.ndarray,
        iterations: int = 100,
        learning_rate: float = 0.01,
    ) -> np.ndarray:
        Z_opt = np.array(Z, dtype=float)
        C = np.array(C_ij, dtype=float)
        N = len(Z_opt)

        for _ in range(iterations):
            grad = np.zeros_like(Z_opt)
            for i in range(N):
                Zi = Z_opt[i]
                for j in range(N):
                    if i == j:
                        continue
                    Zj = Z_opt[j]
                    denom = (Zi + Zj + 1e-10) ** 2
                    grad[i] += C[i, j] * (Zi - Zj) * (Zi + Zj + 2 * Zj) / denom
            Z_opt -= learning_rate * grad

        return Z_opt

    @staticmethod
    def harmony_index(Z: np.ndarray, C_ij: np.ndarray) -> float:
        C_ij = np.array(C_ij, dtype=float)
        W = LeyIsis.tension(Z, C_ij)
        W_max = np.sum(C_ij) + 1e-10
        return float(1.0 / (1.0 + W / W_max))
