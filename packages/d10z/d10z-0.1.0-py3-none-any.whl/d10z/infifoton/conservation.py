# ═══════════════════════════════════════════════════════════════════════════════
# d10z/infifoton/conservation.py
# INFIFOTÓN CONSERVATION LAW
# ═══════════════════════════════════════════════════════════════════════════════
"""
Infifotón Conservation

dN_ifi/dt = 0

This is the MOST FUNDAMENTAL conservation law in D10Z.
Energy conservation EMERGES from infifotón conservation.

N_ifi is conserved in ALL processes:
- Particle creation/annihilation
- Black hole evaporation
- Big Start
- All transformations
"""

import numpy as np
from typing import List, Optional, Dict
from ..core.constants import EPSILON_IFI


def total_infifoton_count(energies: np.ndarray) -> int:
    """
    Compute total infifotón count from energy array.
    
    N_ifi = Σ E_i / ε_ifi
    
    Parameters
    ----------
    energies : np.ndarray
        Array of energies in Joules
    
    Returns
    -------
    int
        Total infifotón count
    """
    return int(round(np.sum(energies) / EPSILON_IFI))


def check_conservation(initial: int, 
                       final: int, 
                       tolerance: int = 0) -> Dict:
    """
    Check if infifotón conservation is satisfied.
    
    Parameters
    ----------
    initial : int
        Initial infifotón count
    final : int
        Final infifotón count
    tolerance : int
        Allowed deviation (should be 0 for exact conservation)
    
    Returns
    -------
    dict
        Conservation check results
    """
    difference = final - initial
    conserved = abs(difference) <= tolerance
    
    return {
        'conserved': conserved,
        'initial': initial,
        'final': final,
        'difference': difference,
        'violation': not conserved
    }


def conservation_violation(initial: int, final: int) -> float:
    """
    Compute fractional violation of conservation.
    
    Parameters
    ----------
    initial : int
        Initial count
    final : int
        Final count
    
    Returns
    -------
    float
        Fractional violation |ΔN|/N_initial
    """
    if initial == 0:
        return float('inf') if final != 0 else 0.0
    return abs(final - initial) / initial


class ConservationTracker:
    """
    Track infifotón conservation through a process.
    
    Records initial state and monitors for violations.
    """
    
    def __init__(self, initial_count: int):
        """
        Initialize tracker.
        
        Parameters
        ----------
        initial_count : int
            Initial infifotón count
        """
        self.initial = initial_count
        self.history = [initial_count]
        self.times = [0.0]
        self.violations = []
    
    def record(self, count: int, time: float):
        """Record a measurement"""
        self.history.append(count)
        self.times.append(time)
        
        if count != self.initial:
            self.violations.append({
                'time': time,
                'count': count,
                'deviation': count - self.initial
            })
    
    @property
    def current(self) -> int:
        """Current infifotón count"""
        return self.history[-1]
    
    @property
    def is_conserved(self) -> bool:
        """Whether conservation has been maintained"""
        return len(self.violations) == 0
    
    @property
    def max_violation(self) -> int:
        """Maximum deviation from initial count"""
        return max(abs(c - self.initial) for c in self.history)
    
    def report(self) -> str:
        """Generate conservation report"""
        status = "✓ CONSERVED" if self.is_conserved else "✗ VIOLATED"
        
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    INFIFOTÓN CONSERVATION REPORT                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Status:           {status:50}║
║  Initial count:    {self.initial:<50}║
║  Final count:      {self.current:<50}║
║  Measurements:     {len(self.history):<50}║
║  Violations:       {len(self.violations):<50}║
║  Max deviation:    {self.max_violation:<50}║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        return report


def verify_process_conservation(initial_state: np.ndarray,
                                final_state: np.ndarray,
                                process_name: str = "Unknown") -> Dict:
    """
    Verify conservation for a physical process.
    
    Parameters
    ----------
    initial_state : np.ndarray
        Initial energies/amplitudes
    final_state : np.ndarray
        Final energies/amplitudes
    process_name : str
        Name of the process
    
    Returns
    -------
    dict
        Verification results
    """
    # Compute infifotón counts
    N_initial = total_infifoton_count(np.abs(initial_state)**2)
    N_final = total_infifoton_count(np.abs(final_state)**2)
    
    check = check_conservation(N_initial, N_final)
    
    result = {
        'process': process_name,
        'N_initial': N_initial,
        'N_final': N_final,
        **check
    }
    
    if check['conserved']:
        print(f"[D10Z] {process_name}: Conservation ✓ (N_ifi = {N_initial})")
    else:
        print(f"[D10Z] {process_name}: Conservation VIOLATED! "
              f"(ΔN = {check['difference']})")
    
    return result


def energy_conservation_from_infifoton(n_ifi_initial: int,
                                        n_ifi_final: int) -> Dict:
    """
    Derive energy conservation from infifotón conservation.
    
    If dN_ifi/dt = 0, then dE/dt = ε_ifi × dN_ifi/dt = 0
    
    Energy conservation is a CONSEQUENCE, not fundamental.
    
    Parameters
    ----------
    n_ifi_initial : int
        Initial infifotón count
    n_ifi_final : int
        Final infifotón count
    
    Returns
    -------
    dict
        Energy conservation derived from infifotón conservation
    """
    E_initial = n_ifi_initial * EPSILON_IFI
    E_final = n_ifi_final * EPSILON_IFI
    delta_E = E_final - E_initial
    
    return {
        'E_initial': E_initial,
        'E_final': E_final,
        'delta_E': delta_E,
        'conserved': abs(delta_E) < EPSILON_IFI,
        'derived_from': 'infifotón conservation'
    }


__all__ = [
    'total_infifoton_count',
    'check_conservation',
    'conservation_violation',
    'ConservationTracker',
    'verify_process_conservation',
    'energy_conservation_from_infifoton'
]
