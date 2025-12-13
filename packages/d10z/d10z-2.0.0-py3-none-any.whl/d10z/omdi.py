from dataclasses import dataclass

OMDI_MASS = 7.95e-36  # kg, valor simbólico

@dataclass
class OmDi:
    """
    Entidad OmDi: bloque fundamental de masa-información en D10Z.
    """
    count: int = 1

    @property
    def mass(self) -> float:
        return self.count * OMDI_MASS
