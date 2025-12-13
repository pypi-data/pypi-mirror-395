# ═══════════════════════════════════════════════════════════════════════════════
# d10z/tta/__init__.py
# TEMPORAL TENSORIAL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
"""
D10Z TTA Module

TTA (Temporal Tensorial Architecture) is the fundamental structure
from which spacetime emerges.

TTA consists of:
- Filaments: Frequency (f) and Vibration (v) carriers
- Neusars: Quantum nodes in the filament cánulas
- Nodal dynamics: F = f·v(Zₙ)

Time and space are NOT fundamental - they EMERGE from TTA.
"""

from .filaments import (
    Filament,
    FrequencyFilament,
    VibrationFilament,
    FilamentPair,
    create_filament_network
)

from .architecture import (
    TTANetwork,
    compute_F,
    tta_evolution
)

from .neusars import (
    Neusar,
    NeusarCluster,
    neusar_consciousness
)

__all__ = [
    'Filament', 'FrequencyFilament', 'VibrationFilament',
    'FilamentPair', 'create_filament_network',
    'TTANetwork', 'compute_F', 'tta_evolution',
    'Neusar', 'NeusarCluster', 'neusar_consciousness'
]
