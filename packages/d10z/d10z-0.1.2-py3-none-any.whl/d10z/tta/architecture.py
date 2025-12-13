# ═══════════════════════════════════════════════════════════════════════════════
# d10z/tta/architecture.py
# TTA ARCHITECTURE - THE FABRIC OF REALITY
# ═══════════════════════════════════════════════════════════════════════════════
"""
TTA Architecture

The complete Temporal Tensorial Architecture that generates
spacetime and all physical phenomena.

F = f · v(Zₙ)

This fundamental relation links frequency, vibration, and nodal state.
"""

import numpy as np
from typing import List, Optional, Dict
from dataclasses import dataclass
from .filaments import FilamentPair, create_filament_network
from ..core.nodes import NodalNetwork
from ..core.coherence import sahana_law, isis_law, compute_coherence
from ..core.constants import EPSILON_IFI, GAMMA_SAHANA


@dataclass
class TTAState:
    """State of the TTA network at a given time"""
    time: float
    coherence: float
    energy: float
    n_infifotons: int
    tension: float
    mean_amplitude: float


class TTANetwork:
    """
    Complete TTA Network.
    
    Combines:
    - Nodal network (Z_n)
    - Filament pairs (f, v)
    - Coherence dynamics
    - Energy generation
    - Infifotón production
    
    This is the fundamental structure from which spacetime emerges.
    """
    
    def __init__(self, 
                 n_nodes: int = 19,
                 seed: Optional[int] = None):
        """
        Initialize TTA network.
        
        Parameters
        ----------
        n_nodes : int
            Number of nodes (default 19 for Flower of Life)
        seed : int, optional
            Random seed
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
        # Create nodal network
        self.nodes = NodalNetwork(n_nodes=n_nodes, seed=seed)
        
        # Create filament pairs (one per node)
        self.filaments = create_filament_network(
            n_pairs=n_nodes,
            arrangement='flower',
            seed=seed
        )
        
        # Time tracking
        self.time = 0.0
        
        # History
        self.history: List[TTAState] = []
    
    @property
    def n_nodes(self) -> int:
        return self.nodes.n_nodes
    
    @property
    def coherence(self) -> float:
        return self.nodes.global_coherence
    
    @property
    def total_energy(self) -> float:
        """Total energy from filament interactions"""
        return sum(fp.compute_energy() for fp in self.filaments)
    
    @property
    def total_infifotons(self) -> int:
        """Total infifotóns generated"""
        return int(self.total_energy / EPSILON_IFI)
    
    @property
    def tension(self) -> float:
        return self.nodes.structural_tension
    
    def get_state(self) -> TTAState:
        """Get current TTA state"""
        return TTAState(
            time=self.time,
            coherence=self.coherence,
            energy=self.total_energy,
            n_infifotons=self.total_infifotons,
            tension=self.tension,
            mean_amplitude=np.mean(self.nodes.amplitudes)
        )
    
    def evolve(self, dt: float = 0.01, 
               omega_f: float = 1.0,
               omega_v: float = 1.1):
        """
        Evolve TTA network one time step.
        
        1. Evolve filaments (f, v oscillation)
        2. Compute F = f·v(Zₙ)
        3. Apply energy to nodes
        4. Evolve nodes via Sahana
        5. Record state
        """
        # Evolve filaments
        for fp in self.filaments:
            fp.evolve(dt, omega_f, omega_v)
        
        # Compute F for each node
        F_values = self._compute_F_values()
        
        # Apply to nodes (modulate amplitudes)
        Z = self.nodes.z_array
        amplitudes = np.abs(Z)
        phases = np.angle(Z)
        
        # F modulates amplitude slightly
        new_amplitudes = amplitudes * (1 + 0.001 * F_values)
        self.nodes.z_array = new_amplitudes * np.exp(1j * phases)
        
        # Sahana evolution
        self.nodes.evolve_sahana(dt=dt, steps=1)
        
        # Update time
        self.time += dt
        
        # Record history
        self.history.append(self.get_state())
    
    def _compute_F_values(self) -> np.ndarray:
        """
        Compute F = f·v(Zₙ) for each node.
        
        F links filament dynamics to nodal state.
        """
        F = np.zeros(self.n_nodes)
        
        for i, fp in enumerate(self.filaments):
            f = fp.f_filament.get_frequency()
            v = fp.v_filament.get_vibration()
            Z_n = abs(self.nodes.nodes[i].z)
            
            # F = f · v(Zₙ) - the fundamental relation
            F[i] = f * v * Z_n
        
        return F
    
    def run_simulation(self, 
                       duration: float = 10.0,
                       dt: float = 0.01) -> List[TTAState]:
        """
        Run TTA simulation for given duration.
        
        Parameters
        ----------
        duration : float
            Total simulation time
        dt : float
            Time step
        
        Returns
        -------
        List[TTAState]
            History of states
        """
        steps = int(duration / dt)
        
        print(f"[TTA] Running simulation: {steps} steps, dt={dt}")
        
        for i in range(steps):
            self.evolve(dt=dt)
            
            if i % (steps // 10) == 0:
                state = self.get_state()
                print(f"  t={state.time:.2f}: Φ={state.coherence:.4f}, "
                      f"E={state.energy:.2e}, N_ifi={state.n_infifotons:.2e}")
        
        print(f"[TTA] Simulation complete. Final Φ={self.coherence:.4f}")
        return self.history
    
    def visualize_state(self, ax=None):
        """Visualize current TTA state"""
        import matplotlib.pyplot as plt
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        
        # Node positions
        pos = self.nodes.positions[:, :2]
        
        # Node colors by phase
        phases = self.nodes.phases
        colors = (phases % (2*np.pi)) / (2*np.pi)
        
        # Plot
        scatter = ax.scatter(pos[:, 0], pos[:, 1],
                            c=colors, cmap='hsv',
                            s=200, edgecolors='black')
        
        ax.set_title(f'TTA Network (t={self.time:.2f}, Φ={self.coherence:.4f})')
        ax.set_aspect('equal')
        
        return ax


def compute_F(f: float, v: float, Z_n: complex) -> float:
    """
    Compute F = f · v(Zₙ)
    
    The fundamental TTA relation.
    
    Parameters
    ----------
    f : float
        Frequency value
    v : float
        Vibration value
    Z_n : complex
        Nodal value
    
    Returns
    -------
    float
        F value
    """
    return f * v * abs(Z_n)


def tta_evolution(Z: np.ndarray,
                  F: np.ndarray,
                  connectivity: np.ndarray,
                  dt: float = 0.01) -> np.ndarray:
    """
    Evolve nodes according to TTA dynamics.
    
    dZ_n/dt = -γ(Z_n - ⟨Z⟩) + α·F_n
    
    Parameters
    ----------
    Z : np.ndarray
        Current nodal values
    F : np.ndarray
        F values for each node
    connectivity : np.ndarray
        Connectivity matrix
    dt : float
        Time step
    
    Returns
    -------
    np.ndarray
        New nodal values
    """
    # Sahana term
    dZ_sahana = sahana_law(Z, connectivity)
    
    # F driving term
    alpha = 0.001
    dZ_F = alpha * F * Z / (np.abs(Z) + 1e-10)
    
    # Total evolution
    Z_new = Z + dt * (dZ_sahana + dZ_F)
    
    return Z_new


__all__ = [
    'TTAState', 'TTANetwork',
    'compute_F', 'tta_evolution'
]
