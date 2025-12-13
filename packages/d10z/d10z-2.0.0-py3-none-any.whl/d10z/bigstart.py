import numpy as np
from .constants import Constants
from .infifoton import Infifoton

class BigStart:
    """
    Big Start - activación del nodo Z₀.
    Marca t=0 en escala de coherencia medible.
    """

    @staticmethod
    def initialize_node_zero(dimension: int = 10) -> Infifoton:
        return Infifoton(
            frequency=Constants.SCHUMANN_BASE,
            phase=0.0,
            position=np.zeros(dimension, dtype=float),
        )

    @staticmethod
    def time_since_big_start(current_time: float) -> float:
        """
        Tiempo transcurrido desde Big Start en unidades de ciclos GM.
        """
        if current_time < 0:
            raise ValueError("current_time must be >= 0")
        return float(current_time / Constants.GM_TIME)
