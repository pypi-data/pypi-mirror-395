# ═══════════════════════════════════════════════════════════════════════════════
# d10z/bigstart/ignition.py
# BIG START IGNITION DYNAMICS
# ═══════════════════════════════════════════════════════════════════════════════
"""
Big Start Ignition

The universe does not "bang" - it IGNITES.

When coherence Φ → 1 across the primordial nodal network (Flower of Life),
the system transitions into a new state: a universe.

This is NOT a singularity. There is no infinite density.
There is coherence threshold crossing.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple
from ..core.constants import (
    PHI_IGNITION, PHI_CRITICAL, EPSILON_IFI,
    FLOWER_OF_LIFE_NODES
)
from ..core.nodes import NodalNetwork, create_flower_of_life
from ..core.coherence import compute_coherence


@dataclass
class BigStartEvent:
    """
    Record of a Big Start ignition event.
    
    Attributes
    ----------
    time : float
        Time of ignition (in internal units)
    coherence_at_ignition : float
        Global coherence when ignition occurred
    n_nodes : int
        Number of nodes at ignition
    total_energy : float
        Total energy at ignition
    n_infifotons : int
        Number of infifotóns released
    state_before : dict
        Network state before ignition
    state_after : dict
        Network state after ignition
    """
    time: float
    coherence_at_ignition: float
    n_nodes: int
    total_energy: float
    n_infifotons: int
    state_before: dict
    state_after: dict
    
    def summary(self) -> str:
        """Return human-readable summary"""
        return f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                            BIG START EVENT                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Time of ignition:     {self.time:.6f}                                        
║  Coherence at Φ → 1:   {self.coherence_at_ignition:.6f}                       
║  Nodes:                {self.n_nodes}                                         
║  Total energy:         {self.total_energy:.6e} (natural units)                
║  Infifotóns released:  {self.n_infifotons:.6e}                                
╚═══════════════════════════════════════════════════════════════════════════════╝
"""


def check_ignition_condition(network: NodalNetwork, 
                             threshold: float = 0.99) -> Tuple[bool, float]:
    """
    Check if a nodal network is ready for Big Start ignition.
    
    Ignition occurs when global coherence approaches 1.
    
    Parameters
    ----------
    network : NodalNetwork
        The nodal network to check
    threshold : float
        Coherence threshold for ignition (default 0.99)
    
    Returns
    -------
    tuple
        (ready: bool, current_coherence: float)
    """
    phi = network.global_coherence
    ready = phi >= threshold
    return ready, phi


def compute_ignition_energy(network: NodalNetwork) -> Tuple[float, int]:
    """
    Compute the energy released at Big Start ignition.
    
    The energy is the total nodal energy converted to infifotóns.
    
    Parameters
    ----------
    network : NodalNetwork
        Network at ignition
    
    Returns
    -------
    tuple
        (total_energy: float, n_infifotons: int)
    """
    total_energy = network.total_energy
    n_infifotons = int(total_energy / EPSILON_IFI)
    return total_energy, n_infifotons


def trigger_ignition(network: NodalNetwork, 
                     force: bool = False) -> Optional[BigStartEvent]:
    """
    Trigger Big Start ignition on a prepared network.
    
    This transforms the network from pre-universe to universe state.
    
    Parameters
    ----------
    network : NodalNetwork
        The network to ignite
    force : bool
        If True, ignite even if threshold not met
    
    Returns
    -------
    BigStartEvent or None
        The ignition event record, or None if conditions not met
    """
    ready, phi = check_ignition_condition(network)
    
    if not ready and not force:
        print(f"[D10Z] Ignition condition not met. Φ = {phi:.4f} < 0.99")
        return None
    
    # Record state before
    state_before = network.get_state()
    
    # IGNITION: Synchronize all phases
    # This is the moment of Big Start
    Z = network.z_array
    mean_phase = np.angle(np.sum(Z))
    amplitudes = np.abs(Z)
    
    # All nodes align to mean phase (coherence → 1)
    Z_ignited = amplitudes * np.exp(1j * mean_phase)
    network.z_array = Z_ignited
    
    # Small expansion perturbation (universe begins expanding)
    perturbation = np.random.normal(0, 0.01, len(Z))
    new_phases = mean_phase + perturbation
    network.z_array = amplitudes * np.exp(1j * new_phases)
    
    # Record state after
    state_after = network.get_state()
    
    # Compute energy release
    total_energy, n_infifotons = compute_ignition_energy(network)
    
    event = BigStartEvent(
        time=0.0,  # Big Start defines t=0
        coherence_at_ignition=phi,
        n_nodes=network.n_nodes,
        total_energy=total_energy,
        n_infifotons=n_infifotons,
        state_before=state_before,
        state_after=state_after
    )
    
    print(event.summary())
    return event


def prepare_for_ignition(network: NodalNetwork, 
                        steps: int = 1000,
                        dt: float = 0.1) -> bool:
    """
    Prepare a network for Big Start by evolving toward coherence.
    
    Uses Sahana dynamics to drive the system toward Φ → 1.
    
    Parameters
    ----------
    network : NodalNetwork
        Network to prepare
    steps : int
        Maximum evolution steps
    dt : float
        Time step
    
    Returns
    -------
    bool
        True if ignition threshold reached
    """
    print("[D10Z] Preparing network for Big Start ignition...")
    
    for step in range(steps):
        network.evolve_sahana(dt=dt, steps=1)
        phi = network.global_coherence
        
        if step % 100 == 0:
            print(f"  Step {step}: Φ = {phi:.4f}")
        
        if phi >= 0.99:
            print(f"[D10Z] Ignition threshold reached at step {step}!")
            return True
    
    print(f"[D10Z] Threshold not reached after {steps} steps. Φ = {phi:.4f}")
    return False


def simulate_big_start(seed: Optional[int] = None) -> BigStartEvent:
    """
    Run a complete Big Start simulation.
    
    1. Create Flower of Life geometry (19 nodes)
    2. Evolve toward coherence
    3. Trigger ignition
    
    Parameters
    ----------
    seed : int, optional
        Random seed for reproducibility
    
    Returns
    -------
    BigStartEvent
        The ignition event
    """
    print("\n" + "="*70)
    print("           D10Z BIG START SIMULATION")
    print("="*70 + "\n")
    
    # Create primordial network
    print("[D10Z] Creating Flower of Life (19 nodes)...")
    network = create_flower_of_life(scale=1.0, seed=seed)
    print(f"  Initial state: {network}")
    
    # Prepare for ignition
    ready = prepare_for_ignition(network, steps=2000, dt=0.05)
    
    if not ready:
        print("[D10Z] Forcing ignition despite threshold...")
    
    # IGNITE
    event = trigger_ignition(network, force=True)
    
    print("\n" + "="*70)
    print("           BIG START COMPLETE - UNIVERSE IGNITED")
    print("="*70 + "\n")
    
    return event


__all__ = [
    'BigStartEvent',
    'check_ignition_condition',
    'compute_ignition_energy',
    'trigger_ignition',
    'prepare_for_ignition',
    'simulate_big_start'
]
