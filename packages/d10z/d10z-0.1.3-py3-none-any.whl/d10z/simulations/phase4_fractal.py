# ═══════════════════════════════════════════════════════════════════════════════
# d10z/simulations/phase4_fractal.py
# PHASE 4: 3D FRACTAL NODAL SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════
"""
Phase 4 Simulation: 3D fractal cloud from infifotón-driven growth.

22,000-28,000 nodes generated through branching growth,
followed by coherence-driven collapse.
"""

import numpy as np

def run_phase4_fractal(target_nodes=(22000, 28000), 
                       collapse_fraction=0.35,
                       seed=123):
    """
    Run Phase 4 fractal simulation.
    
    Parameters
    ----------
    target_nodes : tuple
        (min, max) target node count
    collapse_fraction : float
        Fraction of nodes that collapse
    seed : int
        Random seed
    
    Returns
    -------
    dict
        Simulation results
    """
    rng = np.random.default_rng(seed)
    
    print(f"[D10Z] Phase 4 Fractal Simulation")
    print(f"  Target nodes: {target_nodes[0]}-{target_nodes[1]}")
    
    # Initialize with seeds
    n_seeds = 4
    points = rng.normal(0, 1, (n_seeds, 3))
    
    # Growth phase
    branching = 1.2
    spread = 1.0
    
    for step in range(40):
        n_current = len(points)
        n_children = int(branching * n_current)
        
        if n_children <= 0:
            break
        
        # Select parents
        parent_idx = rng.integers(0, n_current, n_children)
        parents = points[parent_idx]
        
        # Generate children
        displacements = rng.normal(0, spread/(1+0.3*step), (n_children, 3))
        children = parents + displacements
        
        points = np.vstack([points, children])
        
        if len(points) >= target_nodes[1]:
            break
    
    # Trim to target
    points = points[:target_nodes[1]]
    points_growth = points.copy()
    
    print(f"  Growth complete: {len(points)} nodes")
    
    # Collapse phase
    center = np.mean(points, axis=0)
    n_collapse = int(collapse_fraction * len(points))
    collapse_idx = rng.choice(len(points), n_collapse, replace=False)
    
    collapse_step = 0.6
    points[collapse_idx] += collapse_step * (center - points[collapse_idx])
    points_collapse = points.copy()
    
    # Estimate fractal dimension (box counting)
    def box_count(pts, n_boxes):
        mins = pts.min(axis=0)
        maxs = pts.max(axis=0)
        L = maxs - mins
        box_size = L / n_boxes
        idx = np.floor((pts - mins) / (box_size + 1e-10)).astype(int)
        idx = np.clip(idx, 0, n_boxes-1)
        unique = np.unique(idx, axis=0)
        return len(unique)
    
    boxes = [4, 6, 8, 10, 12, 16]
    N_boxes_growth = [box_count(points_growth, b) for b in boxes]
    N_boxes_collapse = [box_count(points_collapse, b) for b in boxes]
    
    # Fit fractal dimension
    log_boxes = np.log(boxes)
    log_N_growth = np.log(N_boxes_growth)
    log_N_collapse = np.log(N_boxes_collapse)
    
    D_growth = np.polyfit(log_boxes, log_N_growth, 1)[0]
    D_collapse = np.polyfit(log_boxes, log_N_collapse, 1)[0]
    
    print(f"  Fractal dimension (growth): {D_growth:.3f}")
    print(f"  Fractal dimension (collapse): {D_collapse:.3f}")
    
    return {
        'points_growth': points_growth,
        'points_collapse': points_collapse,
        'D_growth': D_growth,
        'D_collapse': D_collapse,
        'n_nodes': len(points)
    }
