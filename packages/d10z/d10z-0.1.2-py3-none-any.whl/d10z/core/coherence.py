# ═══════════════════════════════════════════════════════════════════════════════
# d10z/core/coherence.py
# COHERENCE FIELD AND FUNDAMENTAL LAWS
# ═══════════════════════════════════════════════════════════════════════════════
"""
D10Z Coherence Module

The coherence field Φ is the master field from which time, space, and
causality emerge. This module implements:

- CoherenceField: The Φ field structure
- Sahana Law: Nodal convergence toward coherence
- Isis Law: Structural tension dynamics
"""

import numpy as np
from typing import Optional, Tuple
from .constants import (
    PHI_CRITICAL, PHI_MIN, PHI_IGNITION,
    GAMMA_SAHANA, EPSILON_IFI
)


class CoherenceField:
    """
    The coherence field Φ defined over a spatial domain.
    
    Φ: M → [0, 1]
    
    where M is the nodal manifold.
    
    Attributes
    ----------
    grid : np.ndarray
        Spatial grid
    phi : np.ndarray
        Coherence values at each grid point
    """
    
    def __init__(self, 
                 shape: Tuple[int, ...] = (64, 64),
                 initial_value: float = PHI_CRITICAL,
                 seed: Optional[int] = None):
        """
        Initialize coherence field.
        
        Parameters
        ----------
        shape : tuple
            Shape of the field grid
        initial_value : float
            Initial coherence value
        seed : int, optional
            Random seed
        """
        self.shape = shape
        self.rng = np.random.default_rng(seed)
        
        # Initialize field with small fluctuations around initial value
        self.phi = np.ones(shape) * initial_value
        fluctuations = self.rng.normal(0, 0.05, shape)
        self.phi += fluctuations
        
        # Enforce bounds
        self.phi = np.clip(self.phi, PHI_MIN, 1.0)
    
    @property
    def mean_coherence(self) -> float:
        """Mean coherence ⟨Φ⟩"""
        return np.mean(self.phi)
    
    @property
    def max_coherence(self) -> float:
        """Maximum coherence"""
        return np.max(self.phi)
    
    @property
    def min_coherence(self) -> float:
        """Minimum coherence (should always be > PHI_MIN)"""
        return np.max(np.min(self.phi), PHI_MIN)
    
    @property
    def coherence_gradient(self) -> np.ndarray:
        """
        Compute gradient of coherence field.
        
        This gradient is the source of "curvature" in emergent spacetime.
        """
        gradients = np.gradient(self.phi)
        return gradients
    
    @property
    def coherence_laplacian(self) -> np.ndarray:
        """
        Compute Laplacian of coherence field.
        
        ∇²Φ appears in the emergent Einstein equations.
        """
        laplacian = np.zeros_like(self.phi)
        for grad in self.coherence_gradient:
            laplacian += np.gradient(grad, axis=0) if grad.ndim > 0 else 0
        return laplacian
    
    def is_ignition_ready(self) -> bool:
        """Check if field is ready for Big Start (Φ → 1)"""
        return self.mean_coherence > 0.99
    
    def is_critical(self) -> bool:
        """Check if any region is below critical coherence"""
        return np.any(self.phi < PHI_CRITICAL)
    
    def evolve(self, dt: float = 0.01, diffusion: float = 0.1):
        """
        Evolve coherence field according to diffusion equation.
        
        ∂Φ/∂t = D∇²Φ + source_terms
        
        Parameters
        ----------
        dt : float
            Time step
        diffusion : float
            Diffusion coefficient
        """
        laplacian = self.coherence_laplacian
        self.phi += dt * diffusion * laplacian
        
        # Enforce bounds
        self.phi = np.clip(self.phi, PHI_MIN, 1.0)
    
    def add_source(self, position: Tuple[int, ...], strength: float = 0.1):
        """
        Add a coherence source at given position.
        
        Parameters
        ----------
        position : tuple
            Grid position
        strength : float
            Source strength
        """
        self.phi[position] = min(self.phi[position] + strength, 1.0)
    
    def compute_metric_perturbation(self) -> np.ndarray:
        """
        Compute metric perturbation from coherence field.
        
        h_μν = α(∂_μΦ ∂_νΦ - ½η_μν(∂Φ)²)
        
        This is how gravity EMERGES from coherence.
        
        Returns
        -------
        np.ndarray
            Metric perturbation (simplified, diagonal components)
        """
        grad = self.coherence_gradient
        grad_squared = sum(g**2 for g in grad)
        
        # Simplified: return h_00 component
        # Full implementation would return tensor
        alpha = 1e51  # G/c⁴ × 10⁵¹ (coupling constant)
        h_00 = -alpha * grad_squared / 2
        
        return h_00
    
    def __repr__(self):
        return (f"CoherenceField(shape={self.shape}, "
                f"⟨Φ⟩={self.mean_coherence:.4f}, "
                f"Φ_min={self.min_coherence:.4f})")


def sahana_law(Z: np.ndarray, 
               connectivity: np.ndarray, 
               gamma: float = GAMMA_SAHANA) -> np.ndarray:
    """
    Sahana's Law of Nodal Convergence.
    
    dZ_n/dt = -γ(Z_n - Σ_j C_nj Z_j / k_n)
    
    Nodes evolve toward the weighted average of their neighbors,
    driving the system toward coherence.
    
    Parameters
    ----------
    Z : np.ndarray
        Array of nodal values Z_n
    connectivity : np.ndarray
        Connectivity matrix C_ij
    gamma : float
        Damping coefficient
    
    Returns
    -------
    np.ndarray
        Time derivative dZ/dt
    """
    n = len(Z)
    k = np.sum(connectivity, axis=1)  # degree of each node
    k[k == 0] = 1  # avoid division by zero
    
    # Weighted average of neighbors
    Z_avg = connectivity @ Z / k
    
    # Sahana evolution
    dZ_dt = -gamma * (Z - Z_avg)
    
    return dZ_dt


def isis_law(Z: np.ndarray, 
             connectivity: np.ndarray) -> float:
    """
    Isis Law of Structural Tension.
    
    T = Σ_n |∇Z_n|² ≈ Σ_{ij} C_ij |Z_i - Z_j|²
    
    The structural tension measures resistance to deformation.
    Mass and inertia EMERGE from this tension.
    
    Parameters
    ----------
    Z : np.ndarray
        Array of nodal values Z_n
    connectivity : np.ndarray
        Connectivity matrix C_ij
    
    Returns
    -------
    float
        Total structural tension T
    """
    n = len(Z)
    tension = 0.0
    
    for i in range(n):
        for j in range(i + 1, n):
            if connectivity[i, j] > 0:
                dz = Z[i] - Z[j]
                tension += connectivity[i, j] * abs(dz) ** 2
    
    return tension


def compute_coherence(Z: np.ndarray) -> float:
    """
    Compute global coherence from nodal array.
    
    Φ = |Σ_n e^(iθ_n)| / N
    
    Parameters
    ----------
    Z : np.ndarray
        Array of complex nodal values
    
    Returns
    -------
    float
        Global coherence Φ ∈ [0, 1]
    """
    phases = np.angle(Z)
    phase_sum = np.sum(np.exp(1j * phases))
    return abs(phase_sum) / len(Z)


def compute_local_coherence(Z: np.ndarray, 
                            connectivity: np.ndarray) -> np.ndarray:
    """
    Compute local coherence for each node.
    
    Φ_n = |Σ_j C_nj e^(iθ_j)| / Σ_j C_nj
    
    Parameters
    ----------
    Z : np.ndarray
        Array of complex nodal values
    connectivity : np.ndarray
        Connectivity matrix
    
    Returns
    -------
    np.ndarray
        Local coherence for each node
    """
    n = len(Z)
    local_phi = np.zeros(n)
    phases = np.angle(Z)
    
    for i in range(n):
        weights = connectivity[i]
        total_weight = np.sum(weights)
        if total_weight > 0:
            weighted_sum = np.sum(weights * np.exp(1j * phases))
            local_phi[i] = abs(weighted_sum) / total_weight
    
    return local_phi


def emergent_time(phi: float, tau: float) -> float:
    """
    Compute emergent time from proper time and coherence.
    
    dt = dτ / Φ(τ)
    
    Time emerges from coherence - it is NOT fundamental.
    
    Parameters
    ----------
    phi : float
        Local coherence
    tau : float
        Proper time interval
    
    Returns
    -------
    float
        Emergent time interval
    """
    phi_safe = max(phi, PHI_MIN)  # Prevent division by zero
    return tau / phi_safe


def emergent_temperature(phi: float) -> float:
    """
    Compute emergent temperature from coherence.
    
    T = ε_ifi / (k_B × ln(Φ_max/Φ))
    
    Parameters
    ----------
    phi : float
        Local coherence
    
    Returns
    -------
    float
        Emergent temperature in natural units
    """
    from .constants import KB_EMERGENT
    
    phi_safe = max(phi, PHI_MIN)
    if phi_safe >= 1.0:
        return 0.0  # Absolute zero at perfect coherence
    
    return EPSILON_IFI / (KB_EMERGENT * np.log(1.0 / phi_safe))


__all__ = [
    'CoherenceField',
    'sahana_law', 'isis_law',
    'compute_coherence', 'compute_local_coherence',
    'emergent_time', 'emergent_temperature'
]
