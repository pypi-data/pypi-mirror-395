# ═══════════════════════════════════════════════════════════════════════════════
# d10z/infifoton/operators.py
# INFIFOTÓN OPERATORS
# ═══════════════════════════════════════════════════════════════════════════════
"""
Infifotón Operator Algebra

Creation and annihilation operators for infifotóns.

a†|Z⟩ = |Z + √ε_ifi × e^(iφ)⟩   (creation)
a|Z⟩  = |Z - √ε_ifi × e^(iφ)⟩   (annihilation)

Commutation relation: [a, a†] = 1
Number operator: N̂ = a†a
"""

import numpy as np
from typing import Optional, Callable
from ..core.constants import EPSILON_IFI


def creation_operator(Z: complex, 
                      phase: Optional[float] = None,
                      seed: Optional[int] = None) -> complex:
    """
    Apply creation operator a† to state Z.
    
    a†|Z⟩ = |Z + √ε_ifi × e^(iφ)⟩
    
    Parameters
    ----------
    Z : complex
        Current state
    phase : float, optional
        Phase of created infifotón (random if not specified)
    seed : int, optional
        Random seed
    
    Returns
    -------
    complex
        New state after creation
    """
    if phase is None:
        rng = np.random.default_rng(seed)
        phase = rng.uniform(0, 2*np.pi)
    
    delta = np.sqrt(EPSILON_IFI) * np.exp(1j * phase)
    return Z + delta


def annihilation_operator(Z: complex,
                          phase: Optional[float] = None,
                          seed: Optional[int] = None) -> complex:
    """
    Apply annihilation operator a to state Z.
    
    a|Z⟩ = |Z - √ε_ifi × e^(iφ)⟩
    
    Parameters
    ----------
    Z : complex
        Current state
    phase : float, optional
        Phase of annihilated infifotón
    seed : int, optional
        Random seed
    
    Returns
    -------
    complex
        New state after annihilation
    """
    if phase is None:
        rng = np.random.default_rng(seed)
        phase = rng.uniform(0, 2*np.pi)
    
    delta = np.sqrt(EPSILON_IFI) * np.exp(1j * phase)
    return Z - delta


def number_operator(Z: complex) -> float:
    """
    Apply number operator N̂ = a†a to state Z.
    
    Returns the infifotón number (energy in ε_ifi units).
    
    Parameters
    ----------
    Z : complex
        State
    
    Returns
    -------
    float
        Infifotón number
    """
    return abs(Z)**2 / EPSILON_IFI


def commutator(Z: complex, seed: Optional[int] = None) -> complex:
    """
    Compute [a, a†] applied to Z.
    
    Should give [a, a†]|Z⟩ = |Z⟩ (i.e., commutator = 1)
    
    Parameters
    ----------
    Z : complex
        State
    
    Returns
    -------
    complex
        Result of [a, a†]|Z⟩
    """
    rng = np.random.default_rng(seed)
    phase = rng.uniform(0, 2*np.pi)
    
    # aa†|Z⟩
    Z1 = creation_operator(Z, phase)
    Z2 = annihilation_operator(Z1, phase)
    
    # a†a|Z⟩
    Z3 = annihilation_operator(Z, phase)
    Z4 = creation_operator(Z3, phase)
    
    # [a, a†] = aa† - a†a
    return Z2 - Z4


def verify_commutation_relation(n_tests: int = 100,
                                seed: Optional[int] = None) -> dict:
    """
    Verify that [a, a†] = 1.
    
    Parameters
    ----------
    n_tests : int
        Number of test states
    seed : int, optional
        Random seed
    
    Returns
    -------
    dict
        Verification results
    """
    rng = np.random.default_rng(seed)
    errors = []
    
    for _ in range(n_tests):
        # Random state
        Z = rng.normal(0, 1) + 1j * rng.normal(0, 1)
        
        # Compute [a, a†]|Z⟩
        result = commutator(Z, seed=rng.integers(0, 10000))
        
        # Should be approximately Z (within numerical precision)
        # For [a, a†] = 1, we have [a, a†]|Z⟩ should give back identity effect
        # Actually [a, a†] = 1 means the operator gives 1, not |Z⟩
        # So result - Z should be small
        error = abs(result - Z)
        errors.append(error)
    
    return {
        'mean_error': np.mean(errors),
        'max_error': np.max(errors),
        'verified': np.mean(errors) < 1e-10,
        'n_tests': n_tests
    }


def coherent_state(alpha: complex, max_n: int = 50) -> np.ndarray:
    """
    Create coherent state |α⟩ in number basis.
    
    |α⟩ = e^(-|α|²/2) Σ_n (α^n/√n!) |n⟩
    
    Parameters
    ----------
    alpha : complex
        Coherent state parameter
    max_n : int
        Maximum number state to include
    
    Returns
    -------
    np.ndarray
        Coefficients c_n in number basis
    """
    from scipy.special import factorial
    
    n = np.arange(max_n)
    
    # Prefactor
    prefactor = np.exp(-abs(alpha)**2 / 2)
    
    # Coefficients
    c_n = prefactor * (alpha ** n) / np.sqrt(factorial(n))
    
    return c_n


def mean_infifoton_number(alpha: complex) -> float:
    """
    Mean infifotón number for coherent state |α⟩.
    
    ⟨N̂⟩ = |α|²
    
    Parameters
    ----------
    alpha : complex
        Coherent state parameter
    
    Returns
    -------
    float
        Mean infifotón number
    """
    return abs(alpha)**2


def infifoton_variance(alpha: complex) -> float:
    """
    Variance of infifotón number for coherent state |α⟩.
    
    ΔN = |α| (Poissonian statistics)
    
    Parameters
    ----------
    alpha : complex
        Coherent state parameter
    
    Returns
    -------
    float
        Standard deviation
    """
    return abs(alpha)


class InfifotonOperatorAlgebra:
    """
    Complete operator algebra for infifotóns.
    
    Provides a clean interface for quantum operations.
    """
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
        self.epsilon = EPSILON_IFI
    
    def create(self, state: complex, n: int = 1) -> complex:
        """Apply n creation operators"""
        for _ in range(n):
            phase = self.rng.uniform(0, 2*np.pi)
            state = creation_operator(state, phase)
        return state
    
    def annihilate(self, state: complex, n: int = 1) -> complex:
        """Apply n annihilation operators"""
        for _ in range(n):
            phase = self.rng.uniform(0, 2*np.pi)
            state = annihilation_operator(state, phase)
        return state
    
    def number(self, state: complex) -> float:
        """Get infifotón number"""
        return number_operator(state)
    
    def energy(self, state: complex) -> float:
        """Get energy"""
        return self.number(state) * self.epsilon


__all__ = [
    'creation_operator', 'annihilation_operator',
    'number_operator', 'commutator',
    'verify_commutation_relation',
    'coherent_state', 'mean_infifoton_number', 'infifoton_variance',
    'InfifotonOperatorAlgebra'
]
