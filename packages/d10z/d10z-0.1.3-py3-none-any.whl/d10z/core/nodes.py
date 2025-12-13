# ═══════════════════════════════════════════════════════════════════════════════
# d10z/core/nodes.py
# NODAL STRUCTURES - THE FUNDAMENTAL UNITS OF REALITY
# ═══════════════════════════════════════════════════════════════════════════════
"""
D10Z Nodal Structures

The node Z_n ∈ ℂ is the fundamental unit of reality.
All phenomena emerge from nodal configurations and dynamics.

A node has:
- Amplitude |Z_n| ∈ ℝ⁺
- Phase θ_n ∈ [0, 2π)
- Position x_n ∈ ℝ³ (emergent)
- Connectivity to other nodes
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from .constants import PHI_CRITICAL, GAMMA_SAHANA


@dataclass
class Node:
    """
    A single node in the D10Z framework.
    
    The node Z_n = |Z_n| × e^(iθ_n) is the fundamental unit of reality.
    
    Attributes
    ----------
    z : complex
        The complex nodal value Z_n
    position : np.ndarray
        Spatial position (emergent, 3D)
    index : int
        Node index in network
    """
    z: complex
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    index: int = 0
    
    @property
    def amplitude(self) -> float:
        """Nodal amplitude |Z_n|"""
        return abs(self.z)
    
    @property
    def phase(self) -> float:
        """Nodal phase θ_n ∈ [0, 2π)"""
        return np.angle(self.z) % (2 * np.pi)
    
    @property
    def energy(self) -> float:
        """Nodal energy E_n = |Z_n|²"""
        return abs(self.z) ** 2
    
    def coherence_with(self, other: 'Node') -> float:
        """
        Compute coherence Φ_ij with another node.
        
        Φ_ij = |⟨Z_i, Z_j*⟩| / (|Z_i| × |Z_j|)
        """
        if self.amplitude == 0 or other.amplitude == 0:
            return 0.0
        inner = abs(self.z * np.conj(other.z))
        return inner / (self.amplitude * other.amplitude)
    
    def distance_to(self, other: 'Node') -> float:
        """Euclidean distance to another node"""
        return np.linalg.norm(self.position - other.position)
    
    def __repr__(self):
        return f"Node(z={self.z:.4f}, |Z|={self.amplitude:.4f}, θ={self.phase:.4f})"


class NodalNetwork:
    """
    A network of interconnected nodes.
    
    This is the fundamental structure from which spacetime,
    matter, and all phenomena emerge.
    
    Attributes
    ----------
    nodes : List[Node]
        List of nodes in the network
    connectivity : np.ndarray
        Connectivity matrix C_ij
    """
    
    def __init__(self, n_nodes: int = 19, seed: Optional[int] = None):
        """
        Initialize a nodal network.
        
        Parameters
        ----------
        n_nodes : int
            Number of nodes (default 19 for Flower of Life)
        seed : int, optional
            Random seed for reproducibility
        """
        self.rng = np.random.default_rng(seed)
        self.n_nodes = n_nodes
        self.nodes: List[Node] = []
        self.connectivity = np.zeros((n_nodes, n_nodes))
        
        self._initialize_nodes()
        self._compute_connectivity()
    
    def _initialize_nodes(self):
        """Initialize nodes with random complex values"""
        for i in range(self.n_nodes):
            # Random amplitude and phase
            amplitude = self.rng.uniform(0.5, 1.5)
            phase = self.rng.uniform(0, 2 * np.pi)
            z = amplitude * np.exp(1j * phase)
            
            # Random 3D position
            position = self.rng.normal(0, 1, size=3)
            
            self.nodes.append(Node(z=z, position=position, index=i))
    
    def _compute_connectivity(self, correlation_length: float = 2.0):
        """
        Compute connectivity matrix based on coherence and distance.
        
        C_ij = Φ_ij × exp(-d_ij / ξ)
        """
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                if i == j:
                    self.connectivity[i, j] = 1.0
                else:
                    phi_ij = self.nodes[i].coherence_with(self.nodes[j])
                    d_ij = self.nodes[i].distance_to(self.nodes[j])
                    self.connectivity[i, j] = phi_ij * np.exp(-d_ij / correlation_length)
    
    @property
    def z_array(self) -> np.ndarray:
        """Array of all nodal values Z_n"""
        return np.array([node.z for node in self.nodes])
    
    @z_array.setter
    def z_array(self, values: np.ndarray):
        """Set all nodal values"""
        for i, z in enumerate(values):
            self.nodes[i].z = z
    
    @property
    def amplitudes(self) -> np.ndarray:
        """Array of all amplitudes |Z_n|"""
        return np.abs(self.z_array)
    
    @property
    def phases(self) -> np.ndarray:
        """Array of all phases θ_n"""
        return np.angle(self.z_array)
    
    @property
    def positions(self) -> np.ndarray:
        """Array of all positions (N, 3)"""
        return np.array([node.position for node in self.nodes])
    
    @property
    def total_energy(self) -> float:
        """Total energy E = Σ|Z_n|²"""
        return np.sum(self.amplitudes ** 2)
    
    @property
    def global_coherence(self) -> float:
        """
        Global coherence Φ = |Σ_n e^(iθ_n)| / N
        
        Measures phase synchronization across all nodes.
        Φ = 1 means perfect coherence (all phases aligned)
        Φ = 0 means no coherence (random phases)
        """
        phase_sum = np.sum(np.exp(1j * self.phases))
        return abs(phase_sum) / self.n_nodes
    
    @property
    def structural_tension(self) -> float:
        """
        Structural tension T = Σ|∇Z_n|² (Isis Law)
        
        Approximated as sum of squared differences between connected nodes.
        """
        tension = 0.0
        for i in range(self.n_nodes):
            for j in range(i + 1, self.n_nodes):
                if self.connectivity[i, j] > 0.01:  # Only connected nodes
                    dz = self.nodes[i].z - self.nodes[j].z
                    tension += abs(dz) ** 2 * self.connectivity[i, j]
        return tension
    
    def evolve_sahana(self, dt: float = 0.01, steps: int = 1):
        """
        Evolve the network according to Sahana's Law.
        
        dZ_n/dt = -γ(Z_n - Σ_j C_nj Z_j / k_n)
        
        Nodes relax toward local coherence.
        
        Parameters
        ----------
        dt : float
            Time step
        steps : int
            Number of evolution steps
        """
        Z = self.z_array
        
        for _ in range(steps):
            # Compute weighted average for each node
            k = np.sum(self.connectivity, axis=1)  # degree
            k[k == 0] = 1  # avoid division by zero
            
            Z_avg = self.connectivity @ Z / k
            
            # Sahana evolution
            dZ = -GAMMA_SAHANA * (Z - Z_avg)
            Z = Z + dt * dZ
        
        self.z_array = Z
        self._compute_connectivity()
    
    def apply_infifoton(self, node_index: int, n_ifi: int = 1):
        """
        Apply infifotón transformation to a node.
        
        a†|Z⟩ = |Z + √ε_ifi × e^(iφ)⟩
        
        Parameters
        ----------
        node_index : int
            Index of node to transform
        n_ifi : int
            Number of infifotóns to add
        """
        from .constants import EPSILON_IFI
        
        phase = self.rng.uniform(0, 2 * np.pi)
        delta = np.sqrt(n_ifi * EPSILON_IFI) * np.exp(1j * phase)
        self.nodes[node_index].z += delta
    
    def get_state(self) -> dict:
        """Get current state of the network as dictionary"""
        return {
            'n_nodes': self.n_nodes,
            'z_array': self.z_array.copy(),
            'positions': self.positions.copy(),
            'connectivity': self.connectivity.copy(),
            'global_coherence': self.global_coherence,
            'total_energy': self.total_energy,
            'structural_tension': self.structural_tension
        }
    
    def __repr__(self):
        return (f"NodalNetwork(n={self.n_nodes}, "
                f"Φ={self.global_coherence:.4f}, "
                f"E={self.total_energy:.4f}, "
                f"T={self.structural_tension:.4f})")


def create_flower_of_life(scale: float = 1.0, seed: Optional[int] = None) -> NodalNetwork:
    """
    Create a nodal network with Flower of Life geometry (19 nodes).
    
    This is the initial geometry of Big Start.
    
    Parameters
    ----------
    scale : float
        Spatial scale of the pattern
    seed : int, optional
        Random seed
    
    Returns
    -------
    NodalNetwork
        Network with 19 nodes in Flower of Life arrangement
    """
    network = NodalNetwork(n_nodes=19, seed=seed)
    
    # Flower of Life positions (hexagonal + center)
    positions = []
    
    # Center node
    positions.append([0, 0, 0])
    
    # First ring (6 nodes)
    for i in range(6):
        angle = i * np.pi / 3
        positions.append([scale * np.cos(angle), scale * np.sin(angle), 0])
    
    # Second ring (12 nodes)
    for i in range(6):
        angle = i * np.pi / 3 + np.pi / 6
        positions.append([2 * scale * np.cos(angle), 2 * scale * np.sin(angle), 0])
    for i in range(6):
        angle = i * np.pi / 3
        positions.append([np.sqrt(3) * scale * np.cos(angle), 
                          np.sqrt(3) * scale * np.sin(angle), 0])
    
    # Assign positions
    for i, pos in enumerate(positions[:19]):
        network.nodes[i].position = np.array(pos)
    
    network._compute_connectivity()
    return network


__all__ = ['Node', 'NodalNetwork', 'create_flower_of_life']
