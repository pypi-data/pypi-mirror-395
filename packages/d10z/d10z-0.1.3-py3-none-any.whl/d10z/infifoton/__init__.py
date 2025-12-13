# ═══════════════════════════════════════════════════════════════════════════════
# d10z/infifoton/__init__.py
# THE INFIFOTÓN - QUANTUM OF TRANSFORMATION
# ═══════════════════════════════════════════════════════════════════════════════
"""
D10Z Infifotón Module

ε_ifi = 10⁻⁵¹ J

The infifotón is the fundamental quantum of transformation.
ALL energy exchanges are quantized in infifotón units.

This module provides:
- Quantum state representation
- Creation/annihilation operators
- Conservation law implementation
- Energy-infifotón conversion
"""

# Fundamental constant
EPSILON_IFI = 1e-51  # Joules (EXACT, BY AXIOM)


def infifoton_count(energy: float) -> int:
    """Convert energy to infifotón count: N = E / ε_ifi"""
    return int(round(energy / EPSILON_IFI))


def infifoton_energy(n_ifi: int) -> float:
    """Convert infifotón count to energy: E = N × ε_ifi"""
    return n_ifi * EPSILON_IFI


class InfifotonState:
    """
    Quantum state in infifotón basis.
    
    |n⟩ = state with n infifotóns
    """
    def __init__(self, n: int = 0):
        self.n = max(0, int(n))
    
    @property
    def energy(self) -> float:
        return self.n * EPSILON_IFI
    
    def create(self, n: int = 1) -> 'InfifotonState':
        """Apply creation operator: a†|n⟩ = √(n+1)|n+1⟩"""
        return InfifotonState(self.n + n)
    
    def annihilate(self, n: int = 1) -> 'InfifotonState':
        """Apply annihilation operator: a|n⟩ = √n|n-1⟩"""
        return InfifotonState(max(0, self.n - n))
    
    def __repr__(self):
        return f"|{self.n}⟩ (E = {self.energy:.2e} J)"


def creation_operator(state: InfifotonState) -> InfifotonState:
    """a†|n⟩ = |n+1⟩"""
    return state.create()


def annihilation_operator(state: InfifotonState) -> InfifotonState:
    """a|n⟩ = |n-1⟩"""
    return state.annihilate()


def number_operator(state: InfifotonState) -> int:
    """N̂|n⟩ = n|n⟩"""
    return state.n


__all__ = [
    'EPSILON_IFI',
    'infifoton_count', 'infifoton_energy',
    'InfifotonState',
    'creation_operator', 'annihilation_operator', 'number_operator'
]
