# ═══════════════════════════════════════════════════════════════════════════════
# d10z/simulations/phase3_cmb.py
# PHASE 3: CMB-LIKE SIMULATION WITH INFIFOTÓNS
# ═══════════════════════════════════════════════════════════════════════════════
"""
Phase 3 Simulation: 2D CMB-like map from infifotón dynamics.

~24,750 infifotóns excite a nodal network, producing
fluctuation patterns similar to CMB observations.
"""

import numpy as np

def run_phase3_cmb(grid_size=256, n_nodes=10, n_infifotons=24750, seed=42):
    """
    Run Phase 3 CMB simulation.
    
    Parameters
    ----------
    grid_size : int
        Size of output map
    n_nodes : int
        Number of source nodes
    n_infifotons : int
        Number of infifotón events
    seed : int
        Random seed
    
    Returns
    -------
    dict
        Simulation results including field and power spectrum
    """
    rng = np.random.default_rng(seed)
    
    print(f"[D10Z] Phase 3 CMB Simulation")
    print(f"  Grid: {grid_size}×{grid_size}")
    print(f"  Nodes: {n_nodes}")
    print(f"  Infifotóns: {n_infifotons}")
    
    # Node positions
    node_pos = rng.normal(0, 0.15, (n_nodes, 2))
    
    # Generate field in Fourier space
    kx = np.fft.fftfreq(grid_size)
    ky = np.fft.fftfreq(grid_size)
    KX, KY = np.meshgrid(kx, ky)
    
    fourier_field = np.zeros((grid_size, grid_size), dtype=complex)
    sigma_k = 8.0
    
    for i in range(n_infifotons):
        # Select source node
        node_idx = rng.integers(0, n_nodes)
        
        # Random k-mode
        k_mag = rng.rayleigh(sigma_k)
        theta = rng.uniform(0, 2*np.pi)
        kx_mode = k_mag * np.cos(theta)
        ky_mode = k_mag * np.sin(theta)
        
        # Phase from infifotón
        phase = rng.uniform(0, 2*np.pi)
        
        # Mode profile
        mode = np.exp(-((KX-kx_mode)**2 + (KY-ky_mode)**2) / (2*(sigma_k/4)**2))
        fourier_field += np.exp(1j * phase) * mode
    
    # Transform to real space
    field = np.real(np.fft.ifft2(fourier_field))
    field -= np.mean(field)
    field /= np.std(field) + 1e-10
    
    # Power spectrum
    P = np.abs(np.fft.fft2(field))**2
    K = np.sqrt(KX**2 + KY**2)
    
    # Radial average
    k_bins = np.linspace(0, 0.5, 50)
    Pk = np.zeros(len(k_bins)-1)
    for i in range(len(k_bins)-1):
        mask = (K >= k_bins[i]) & (K < k_bins[i+1])
        if np.sum(mask) > 0:
            Pk[i] = np.mean(P[mask])
    
    k_centers = 0.5 * (k_bins[:-1] + k_bins[1:])
    
    print(f"[D10Z] Simulation complete. Field variance: {np.var(field):.4f}")
    
    return {
        'field': field,
        'k': k_centers,
        'Pk': Pk,
        'n_infifotons': n_infifotons,
        'n_nodes': n_nodes
    }
