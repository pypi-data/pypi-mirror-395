# ═══════════════════════════════════════════════════════════════════════════════
# d10z/bigstart/flower_of_life.py
# FLOWER OF LIFE GEOMETRY - PRIMORDIAL STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════
"""
Flower of Life Geometry

The Flower of Life is the primordial geometry of Big Start.
19 nodes arranged in sacred hexagonal pattern.

This is NOT arbitrary - it is the natural geometry that emerges
from coherence dynamics. The Flower of Life appears across all
scales because it is a fundamental attractor of nodal systems.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
from ..core.constants import FLOWER_OF_LIFE_NODES, PHI_CRITICAL


@dataclass
class FlowerOfLife:
    """
    The Flower of Life sacred geometry.
    
    19 nodes in hexagonal arrangement:
    - 1 center node
    - 6 first ring nodes
    - 12 second ring nodes
    
    Attributes
    ----------
    positions : np.ndarray
        3D positions of all nodes (19, 3)
    scale : float
        Spatial scale of the pattern
    center : np.ndarray
        Center position
    """
    positions: np.ndarray
    scale: float
    center: np.ndarray
    
    @property
    def n_nodes(self) -> int:
        return FLOWER_OF_LIFE_NODES
    
    @property
    def first_ring(self) -> np.ndarray:
        """Positions of first ring (6 nodes)"""
        return self.positions[1:7]
    
    @property
    def second_ring(self) -> np.ndarray:
        """Positions of second ring (12 nodes)"""
        return self.positions[7:19]
    
    def get_connectivity(self) -> np.ndarray:
        """
        Get natural connectivity matrix for Flower of Life.
        
        Nodes are connected based on their ring membership
        and angular proximity.
        """
        C = np.zeros((self.n_nodes, self.n_nodes))
        
        # Center connects to all first ring
        for i in range(1, 7):
            C[0, i] = 1.0
            C[i, 0] = 1.0
        
        # First ring connects to neighbors
        for i in range(1, 7):
            next_i = 1 + (i % 6)
            C[i, next_i] = 1.0
            C[next_i, i] = 1.0
        
        # First ring connects to second ring
        for i in range(1, 7):
            # Each first ring node connects to 2 second ring nodes
            j1 = 7 + 2 * (i - 1)
            j2 = 7 + (2 * (i - 1) + 1) % 12
            C[i, j1] = 0.8
            C[j1, i] = 0.8
            C[i, j2] = 0.8
            C[j2, i] = 0.8
        
        # Second ring connects to neighbors
        for i in range(7, 19):
            next_i = 7 + ((i - 7 + 1) % 12)
            C[i, next_i] = 0.6
            C[next_i, i] = 0.6
        
        return C


def create_flower_geometry(scale: float = 1.0, 
                           center: Optional[np.ndarray] = None,
                           z_offset: float = 0.0) -> FlowerOfLife:
    """
    Create Flower of Life geometry.
    
    Parameters
    ----------
    scale : float
        Radius of first ring
    center : np.ndarray, optional
        Center position (default origin)
    z_offset : float
        Z coordinate offset
    
    Returns
    -------
    FlowerOfLife
        The geometry structure
    """
    if center is None:
        center = np.array([0.0, 0.0, z_offset])
    
    positions = np.zeros((FLOWER_OF_LIFE_NODES, 3))
    
    # Node 0: Center
    positions[0] = center
    
    # Nodes 1-6: First ring (hexagon)
    for i in range(6):
        angle = i * np.pi / 3
        positions[1 + i] = center + scale * np.array([
            np.cos(angle),
            np.sin(angle),
            0
        ])
    
    # Nodes 7-18: Second ring
    # Outer hexagon (6 nodes)
    for i in range(6):
        angle = i * np.pi / 3 + np.pi / 6
        positions[7 + i] = center + 2 * scale * np.array([
            np.cos(angle),
            np.sin(angle),
            0
        ])
    
    # Inner second ring (6 nodes at √3 distance)
    for i in range(6):
        angle = i * np.pi / 3
        positions[13 + i] = center + np.sqrt(3) * scale * np.array([
            np.cos(angle),
            np.sin(angle),
            0
        ])
    
    return FlowerOfLife(
        positions=positions,
        scale=scale,
        center=center
    )


def flower_coherence(phases: np.ndarray) -> float:
    """
    Compute coherence specific to Flower of Life geometry.
    
    Weights the center node more heavily as it is the
    nexus of the pattern.
    
    Parameters
    ----------
    phases : np.ndarray
        Phases of all 19 nodes
    
    Returns
    -------
    float
        Weighted coherence
    """
    assert len(phases) == FLOWER_OF_LIFE_NODES
    
    # Weights: center = 3, first ring = 2, second ring = 1
    weights = np.array([3.0] + [2.0]*6 + [1.0]*12)
    weights /= np.sum(weights)
    
    # Weighted phase sum
    phase_vectors = np.exp(1j * phases)
    weighted_sum = np.sum(weights * phase_vectors)
    
    return abs(weighted_sum)


def visualize_flower(flower: FlowerOfLife, 
                     phases: Optional[np.ndarray] = None,
                     ax=None):
    """
    Visualize Flower of Life geometry.
    
    Parameters
    ----------
    flower : FlowerOfLife
        The geometry to visualize
    phases : np.ndarray, optional
        Node phases for coloring
    ax : matplotlib axis, optional
        Axis to plot on
    """
    import matplotlib.pyplot as plt
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    
    pos = flower.positions[:, :2]  # 2D projection
    
    # Draw connections
    C = flower.get_connectivity()
    for i in range(flower.n_nodes):
        for j in range(i+1, flower.n_nodes):
            if C[i, j] > 0:
                ax.plot([pos[i, 0], pos[j, 0]], 
                        [pos[i, 1], pos[j, 1]], 
                        'k-', alpha=0.3 * C[i, j], lw=1)
    
    # Draw nodes
    if phases is not None:
        colors = (phases % (2*np.pi)) / (2*np.pi)
        scatter = ax.scatter(pos[:, 0], pos[:, 1], 
                            c=colors, cmap='hsv', 
                            s=200, edgecolors='black', zorder=5)
    else:
        ax.scatter(pos[:, 0], pos[:, 1], 
                  c='gold', s=200, edgecolors='black', zorder=5)
    
    # Draw circles for visual reference
    for r in [flower.scale, 2*flower.scale]:
        circle = plt.Circle(flower.center[:2], r, 
                           fill=False, color='gray', 
                           linestyle='--', alpha=0.5)
        ax.add_patch(circle)
    
    ax.set_aspect('equal')
    ax.set_title('Flower of Life - Primordial Geometry')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    return ax


__all__ = [
    'FlowerOfLife',
    'create_flower_geometry',
    'flower_coherence',
    'visualize_flower'
]
