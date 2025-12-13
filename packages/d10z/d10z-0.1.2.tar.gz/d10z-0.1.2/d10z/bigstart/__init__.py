# ═══════════════════════════════════════════════════════════════════════════════
# d10z/bigstart/__init__.py
# BIG START - THE IGNITION EVENT (NOT BIG BANG)
# ═══════════════════════════════════════════════════════════════════════════════
"""
D10Z Big Start Module

Big Start is the ignition event that creates a universe.
It is NOT an explosion from a singularity (Big Bang is a human artifact).

Big Start occurs when:
- Global coherence Φ → 1
- The Flower of Life (19 nodes) achieves phase alignment
- The system transitions from pre-universe to universe state

This module implements the ignition dynamics.
"""

from .ignition import (
    BigStartEvent,
    check_ignition_condition,
    trigger_ignition,
    compute_ignition_energy
)

from .flower_of_life import (
    FlowerOfLife,
    create_flower_geometry,
    flower_coherence
)

__all__ = [
    'BigStartEvent',
    'check_ignition_condition',
    'trigger_ignition',
    'compute_ignition_energy',
    'FlowerOfLife',
    'create_flower_geometry',
    'flower_coherence'
]
