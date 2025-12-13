# ═══════════════════════════════════════════════════════════════════════════════
# d10z/core/constants.py
# FUNDAMENTAL CONSTANTS OF THE D10Z FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════════
"""
D10Z Fundamental Constants

These constants are AXIOMATIC - they are not derived from human physics.
Human physics (G, ℏ, c) are EMERGENT from these constants, not the reverse.

WARNING: Do not attempt to "derive" these from Planck units or any human
framework. That would be epistemological contamination.
"""

import numpy as np

# ═══════════════════════════════════════════════════════════════════════════════
# PRIMARY CONSTANTS (AXIOMATIC)
# ═══════════════════════════════════════════════════════════════════════════════

# The Infifotón: Quantum of all transformation
EPSILON_IFI = 1e-51  # Joules
"""
The infifotón is the fundamental quantum of transformation.
ALL energy in the universe is quantized in units of ε_ifi.
E = N_ifi × ε_ifi, where N_ifi ∈ ℕ
"""

# Geometric scale (Mandelshtam scale)
GM_SCALE = 1e-51  # meters
L_IFI = GM_SCALE
"""
The fundamental geometric scale of the nodal network.
Replaces the Planck length as the true quantum of space.
"""

# Critical coherence (golden ratio inverse)
PHI_CRITICAL = (np.sqrt(5) - 1) / 2  # ≈ 0.618033988749895
"""
The critical coherence threshold.
Below this, systems become unstable.
Equal to 1/φ where φ is the golden ratio.
"""

# Minimum coherence (singularity prevention)
PHI_MIN = 1e-10
"""
The minimum possible coherence.
Φ ≥ Φ_min > 0 ALWAYS.
This prevents singularities - there is no "zero coherence" state.
"""

# Ignition coherence (Big Start threshold)
PHI_IGNITION = 1.0
"""
The coherence threshold for Big Start.
When Φ → 1 globally, a universe ignites.
"""

# Sahana damping coefficient
GAMMA_SAHANA = 0.02  # s⁻¹
"""
The fundamental damping rate in Sahana's Law.
Controls the relaxation of nodes toward coherence.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TTA STRUCTURE CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Filament thickness (frequency filament and vibration filament)
FILAMENT_THICKNESS_FACTOR = 1e-7  # 0.0000001% of GM
FILAMENT_THICKNESS = FILAMENT_THICKNESS_FACTOR * GM_SCALE

# Filament separation
FILAMENT_SEPARATION_FACTOR = 1e-13  # 0.0000000000001%
FILAMENT_SEPARATION = FILAMENT_SEPARATION_FACTOR * GM_SCALE

# Flower of Life nodes (sacred geometry)
FLOWER_OF_LIFE_NODES = 19
"""
The initial geometry of Big Start.
19 nodes arranged in the Flower of Life pattern.
NOT arbitrary - this is the natural geometry of coherence.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# GM TABLE (SCALE-DEPENDENT PARAMETERS)
# ═══════════════════════════════════════════════════════════════════════════════

GM_TABLE = {
    # Scale Zn (m) : {parameters}
    "1e-51": {
        "ICGM": -99.93,
        "f": 2.998e59,  # Hz
        "T": 3.336e-60,  # s
        "kappa": 1e51,
        "description": "Sub-Planckian / Big Start scale"
    },
    "1e-35": {
        "ICGM": -67.93,
        "f": 2.998e43,
        "T": 3.336e-44,
        "kappa": 1e35,
        "description": "Planck scale (human artifact)"
    },
    "1e-15": {
        "ICGM": -27.93,
        "f": 2.998e23,
        "T": 3.336e-24,
        "kappa": 1e15,
        "description": "Nuclear scale"
    },
    "1e-9": {
        "ICGM": -15.93,
        "f": 2.998e17,
        "T": 3.336e-18,
        "kappa": 1e9,
        "description": "DNA / Biological coherence"
    },
    "1e0": {
        "ICGM": 6.07,
        "f": 2.998e8,
        "T": 3.336e-9,
        "kappa": 1e0,
        "description": "Human scale"
    },
    "1e22": {
        "ICGM": 4.07,
        "f": 2.998e-14,
        "T": 3.336e13,
        "kappa": 1e-22,
        "description": "Cosmological scale"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# DERIVED CONSTANTS (for compatibility, NOT fundamental)
# ═══════════════════════════════════════════════════════════════════════════════

# These are what human physics THINKS are fundamental.
# In D10Z, they EMERGE from nodal dynamics.

# Speed of light (emergent from coherence propagation)
C_EMERGENT = 2.998e8  # m/s

# Planck constant (emergent from infifotón statistics)
HBAR_EMERGENT = 1.054e-34  # J·s

# Gravitational constant (emergent from coherence gradients)
G_EMERGENT = 6.674e-11  # m³/(kg·s²)

# Boltzmann constant (emergent from nodal statistics)
KB_EMERGENT = 1.381e-23  # J/K


def get_gm_parameters(scale):
    """
    Get GM parameters for a given scale.
    
    Parameters
    ----------
    scale : str or float
        The scale in meters (e.g., "1e-51" or 1e-51)
    
    Returns
    -------
    dict
        GM parameters for that scale, or None if not found
    """
    key = str(scale) if isinstance(scale, str) else f"{scale:.0e}"
    return GM_TABLE.get(key)


def infifoton_count(energy):
    """
    Convert energy to infifotón count.
    
    Parameters
    ----------
    energy : float
        Energy in Joules
    
    Returns
    -------
    int
        Number of infifotóns (rounded to nearest integer)
    """
    return int(round(energy / EPSILON_IFI))


def infifoton_energy(n_ifi):
    """
    Convert infifotón count to energy.
    
    Parameters
    ----------
    n_ifi : int
        Number of infifotóns
    
    Returns
    -------
    float
        Energy in Joules
    """
    return n_ifi * EPSILON_IFI


# Export all constants
__all__ = [
    'EPSILON_IFI', 'GM_SCALE', 'L_IFI',
    'PHI_CRITICAL', 'PHI_MIN', 'PHI_IGNITION',
    'GAMMA_SAHANA',
    'FILAMENT_THICKNESS', 'FILAMENT_SEPARATION',
    'FLOWER_OF_LIFE_NODES',
    'GM_TABLE',
    'C_EMERGENT', 'HBAR_EMERGENT', 'G_EMERGENT', 'KB_EMERGENT',
    'get_gm_parameters', 'infifoton_count', 'infifoton_energy'
]
