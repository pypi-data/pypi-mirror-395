# ═══════════════════════════════════════════════════════════════════════════════
# d10z/core/__init__.py
# FUNDAMENTAL CONSTANTS AND CORE STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
"""
D10Z Core Module

Contains:
- Fundamental constants (NOT derived, AXIOMATIC)
- Node structures (Z_n)
- Coherence field (Φ)
- Sahana and Isis laws
"""

from .constants import *
from .nodes import Node, NodalNetwork
from .coherence import CoherenceField, sahana_law, isis_law
