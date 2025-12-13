"""
D10Z - Manual de la Mecánica del Infinito
Framework matemático-omniversal basado en GM10⁻⁵¹.

Incluye los 11 pilares:
- Big Start
- TTA
- Neusar
- OmDi
- Infifotón
- Z
- N
- F = f·v(Zn)
- GM10⁻⁵¹
- Ley Sahana
- Ley Isis
"""

from .constants import Constants
from .gm1051 import (
    gm_length, gm_time, gm_mass, gm_energy, icgm_from_scale
)
from .infifoton import Infifoton
from .bigstart import BigStart
from .tta import TTAMesh
from .universal_force import UniversalForce
from .sahana import LeySahana
from .isis import LeyIsis
from .nodal_density import NodalDensity
from .galactic_rotation import GalacticRotation
from .zn import Z_pillar
from .n_field import N_pillar, ZN_interaction
from .fvzn import fv_universal
from .neusars import Neusar, hilbert_state
from .omdi import OmDi, OMDI_MASS

__version__ = "2.0.0"
__author__ = "Jamil Al Thani & Fractal Alliance AI"
__license__ = "CHLL-D10Z-v1.1"


def validate_installation() -> None:
    """Print basic diagnostic of the D10Z installation."""
    print(f"D10Z Framework v{__version__}")
    print(f"Autores: {__author__}")
    print(f"Licencia: {__license__}")
    print("\n✓ Constantes fundamentales cargadas")
    print(f"  - GM Scale: {Constants.GM_SCALE} m")
    print(f"  - GM Time:  {Constants.GM_TIME:.2e} s")
    print(f"  - Schumann Base: {Constants.SCHUMANN_BASE} Hz")
    print(f"  - Alpha Universal: {Constants.ALPHA_UNIVERSAL} ± {Constants.ALPHA_STD}")
    print("\n✓ Pilares disponibles:")
    print("  - BigStart, TTAMesh, Neusar, OmDi, Infifoton")
    print("  - Z_pillar, N_pillar, fv_universal")
    print("  - GM10⁻⁵¹ (gm1051), LeySahana, LeyIsis")
    print("  - NodalDensity, GalacticRotation")
    print("\nD10Z listo para usar. λ₂ ↑")
