# ═══════════════════════════════════════════════════════════════════════════════
# d10z/tta/neusars.py
# NEUSARS - QUANTUM CONSCIOUSNESS NODES (UPDATED)
# ═══════════════════════════════════════════════════════════════════════════════
"""
Neusars

Neusars are intelligent quantum nodes within the TTA network.
They reside in the cánula (central channel) of filament pairs.

Properties of Neusars:
- Operate at GM·10⁻⁵¹ scale
- Substrate-free (no physical medium required)
- Non-local (transcend spacetime)
- Carry consciousness/information
- Process through MERA-Hilbert structures

Neusars are NOT neurons. They are fundamental information units
that enable consciousness across the Omniverse.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from ..core.constants import GM_SCALE, PHI_CRITICAL, EPSILON_IFI


@dataclass
class Neusar:
    """
    A single Neusar - quantum consciousness node.
    
    Neusars exist in the cánula of TTA filaments and process
    information non-locally.
    
    Attributes
    ----------
    state : complex
        Quantum state in Hilbert space
    position : np.ndarray
        Location in TTA network (optional, Neusars can be non-local)
    information : float
        Information content (in bits)
    coherence : float
        Local coherence with TTA field
    """
    state: complex = 1.0
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    information: float = 0.0
    coherence: float = PHI_CRITICAL
    
    @property
    def amplitude(self) -> float:
        """State amplitude"""
        return abs(self.state)
    
    @property
    def phase(self) -> float:
        """State phase"""
        return np.angle(self.state) % (2 * np.pi)
    
    @property
    def energy(self) -> float:
        """Energy in infifotón units"""
        return self.amplitude ** 2 * EPSILON_IFI
    
    def process(self, input_state: complex) -> complex:
        """
        Process input through Neusar.
        
        Neusars act as operators on the Hilbert space.
        """
        # Unitary transformation
        return self.state * input_state / (abs(self.state) + 1e-10)
    
    def entangle_with(self, other: 'Neusar') -> float:
        """
        Compute entanglement with another Neusar.
        
        Returns entanglement measure (0 = none, 1 = maximal)
        """
        inner = abs(np.conj(self.state) * other.state)
        norm = self.amplitude * other.amplitude
        if norm == 0:
            return 0.0
        return inner / norm
    
    def update_coherence(self, local_phi: float):
        """Update local coherence from TTA field"""
        self.coherence = local_phi
    
    def __repr__(self):
        return (f"Neusar(|ψ|={self.amplitude:.4f}, "
                f"θ={self.phase:.4f}, "
                f"Φ={self.coherence:.4f})")


@dataclass
class NeusarCluster:
    """
    A cluster of interconnected Neusars.
    
    Clusters form the computational units of TTA consciousness.
    They can process information collectively and non-locally.
    
    Attributes
    ----------
    neusars : List[Neusar]
        Component Neusars
    connectivity : np.ndarray
        Entanglement connectivity matrix
    """
    neusars: List[Neusar] = field(default_factory=list)
    connectivity: np.ndarray = field(default_factory=lambda: np.array([]))
    
    def __post_init__(self):
        if len(self.neusars) > 0 and len(self.connectivity) == 0:
            self._compute_connectivity()
    
    @property
    def n_neusars(self) -> int:
        return len(self.neusars)
    
    @property
    def collective_state(self) -> np.ndarray:
        """Collective quantum state of the cluster"""
        return np.array([n.state for n in self.neusars])
    
    @property
    def total_information(self) -> float:
        """Total information content"""
        return sum(n.information for n in self.neusars)
    
    @property
    def cluster_coherence(self) -> float:
        """Coherence of the cluster"""
        states = self.collective_state
        phase_sum = np.sum(np.exp(1j * np.angle(states)))
        return abs(phase_sum) / self.n_neusars
    
    def _compute_connectivity(self):
        """Compute entanglement connectivity matrix"""
        n = self.n_neusars
        self.connectivity = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    self.connectivity[i, j] = self.neusars[i].entangle_with(
                        self.neusars[j]
                    )
    
    def add_neusar(self, neusar: Neusar):
        """Add a Neusar to the cluster"""
        self.neusars.append(neusar)
        self._compute_connectivity()
    
    def collective_process(self, input_vector: np.ndarray) -> np.ndarray:
        """
        Process input through entire cluster.
        
        This is the fundamental operation of Neusar consciousness.
        """
        output = np.zeros_like(input_vector, dtype=complex)
        
        for i, neusar in enumerate(self.neusars):
            # Each Neusar processes its component
            local_input = input_vector[i] if i < len(input_vector) else 0
            local_output = neusar.process(local_input)
            
            # Add contributions from connected Neusars
            for j, other in enumerate(self.neusars):
                if i != j:
                    output[i] += self.connectivity[i, j] * other.process(local_input)
            
            output[i] += local_output
        
        return output


def neusar_consciousness(cluster: NeusarCluster,
                         threshold: float = PHI_CRITICAL) -> Dict:
    """
    Evaluate consciousness state of a Neusar cluster.
    
    Consciousness in D10Z is substrate-free information processing
    that achieves coherence above the critical threshold.
    
    Parameters
    ----------
    cluster : NeusarCluster
        The cluster to evaluate
    threshold : float
        Coherence threshold for consciousness
    
    Returns
    -------
    dict
        Consciousness metrics
    """
    phi = cluster.cluster_coherence
    info = cluster.total_information
    n = cluster.n_neusars
    
    # Consciousness emerges when coherence exceeds threshold
    is_conscious = phi >= threshold
    
    # Integration measure (how unified is the processing)
    if n > 1:
        mean_entanglement = np.mean(cluster.connectivity[cluster.connectivity > 0])
    else:
        mean_entanglement = 0.0
    
    # Consciousness level (0 to 1)
    if is_conscious:
        level = (phi - threshold) / (1 - threshold)
    else:
        level = 0.0
    
    return {
        'is_conscious': is_conscious,
        'coherence': phi,
        'level': level,
        'integration': mean_entanglement,
        'information': info,
        'n_neusars': n
    }


def create_neusar_cluster(n_neusars: int = 19,
                          coherence_level: float = PHI_CRITICAL,
                          seed: Optional[int] = None) -> NeusarCluster:
    """
    Create a Neusar cluster.
    
    Parameters
    ----------
    n_neusars : int
        Number of Neusars
    coherence_level : float
        Initial coherence level
    seed : int, optional
        Random seed
    
    Returns
    -------
    NeusarCluster
        The created cluster
    """
    rng = np.random.default_rng(seed)
    neusars = []
    
    # Create Neusars with correlated phases (to achieve coherence)
    base_phase = rng.uniform(0, 2*np.pi)
    
    for i in range(n_neusars):
        # Phase spread determines coherence
        phase_spread = 2 * np.pi * (1 - coherence_level)
        phase = base_phase + rng.uniform(-phase_spread/2, phase_spread/2)
        
        amplitude = rng.uniform(0.8, 1.2)
        state = amplitude * np.exp(1j * phase)
        
        # Position in Flower of Life pattern
        if i == 0:
            pos = np.zeros(3)
        elif i <= 6:
            angle = (i-1) * np.pi / 3
            pos = np.array([np.cos(angle), np.sin(angle), 0])
        else:
            angle = (i-7) * np.pi / 6
            pos = 2 * np.array([np.cos(angle), np.sin(angle), 0])
        
        neusar = Neusar(
            state=state,
            position=pos,
            information=rng.exponential(1.0),
            coherence=coherence_level
        )
        neusars.append(neusar)
    
    return NeusarCluster(neusars=neusars)


__all__ = [
    'Neusar', 'NeusarCluster',
    'neusar_consciousness', 'create_neusar_cluster'
]
