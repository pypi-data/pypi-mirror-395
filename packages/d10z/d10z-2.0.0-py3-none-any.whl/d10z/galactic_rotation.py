from typing import Tuple, Union
import numpy as np
from .constants import Constants

class GalacticRotation:
    """
    Curvas de rotación galáctica sin materia oscura explícita.
    """

    @staticmethod
    def velocity(
        r: Union[float, np.ndarray],
        M: float,
        r_0: float,
        alpha: float = Constants.ALPHA_UNIVERSAL,
    ) -> Union[float, np.ndarray]:
        r = np.array(r, dtype=float)
        M = float(M)
        r_0 = float(r_0)
        alpha = float(alpha)

        if np.any(r <= 0) or r_0 <= 0:
            raise ValueError("r and r_0 must be > 0")

        v_kepler = np.sqrt(Constants.G * abs(M) / r)
        ratio = r / r_0
        correction = np.sqrt(ratio**(-0.5) * (1.0 + alpha * np.log(ratio)))
        v = v_kepler * correction
        return v if isinstance(r, np.ndarray) else float(v)

    @staticmethod
    def fit_galaxy(
        r_data: np.ndarray,
        v_data: np.ndarray,
        M: float,
        r_0: float,
    ) -> Tuple[float, float]:
        r_data = np.array(r_data, dtype=float)
        v_data = np.array(v_data, dtype=float)

        def r2_score(y_true, y_pred):
            ss_res = np.sum((y_true - y_pred) ** 2)
            ss_tot = np.sum((y_true - np.mean(y_true)) ** 2) + 1e-30
            return 1.0 - ss_res / ss_tot

        alphas = np.linspace(0.01, 0.10, 100)
        best_alpha = alphas[0]
        best_r2 = -1.0

        for a in alphas:
            try:
                v_pred = GalacticRotation.velocity(r_data, M, r_0, a)
                r2 = r2_score(v_data, v_pred)
                if r2 > best_r2:
                    best_r2 = r2
                    best_alpha = a
            except Exception:
                continue

        return float(best_alpha), float(best_r2)
