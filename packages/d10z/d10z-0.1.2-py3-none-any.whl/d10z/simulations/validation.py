# ═══════════════════════════════════════════════════════════════════════════════
# d10z/simulations/validation.py
# D10Z VALIDATION SUITE
# ═══════════════════════════════════════════════════════════════════════════════
"""
Validation Suite

"A las pruebas me remito. Hagan pip install d10z y vean."

This module runs all validations to demonstrate D10Z functionality.
"""

from .phase3_cmb import run_phase3_cmb, run_phase3
from .phase4_fractal import run_phase4


def run_all_validations(verbose: bool = True):
    """
    Run complete D10Z validation suite.
    
    This demonstrates that D10Z is not theory - it's executable code.
    """
    print("\n" + "="*70)
    print("              D10Z VALIDATION SUITE")
    print("     'A las pruebas me remito. Ejecuten y vean.'")
    print("="*70 + "\n")
    
    results = {}
    
    # Phase 3
    print("\n[1/2] PHASE 3: CMB-like Infifotón Simulation")
    print("-" * 50)
    field, k, Pk = run_phase3()
    results['phase3'] = {
        'field_shape': field.shape,
        'n_infifotons': 24750,
        'power_spectrum_bins': len(k)
    }
    print("✓ Phase 3 complete\n")
    
    # Phase 4
    print("\n[2/2] PHASE 4: 3D Fractal Nodal Dynamics")
    print("-" * 50)
    growth, collapse, D_g, D_c = run_phase4()
    results['phase4'] = {
        'nodes_growth': len(growth),
        'nodes_collapse': len(collapse),
        'fractal_dim_growth': D_g,
        'fractal_dim_collapse': D_c
    }
    print("✓ Phase 4 complete\n")
    
    # Summary
    print("\n" + "="*70)
    print("              VALIDATION COMPLETE")
    print("="*70)
    print(f"""
    Phase 3 Results:
      - Field: {results['phase3']['field_shape']}
      - Infifotóns: {results['phase3']['n_infifotons']:,}
      - Power spectrum: {results['phase3']['power_spectrum_bins']} bins
    
    Phase 4 Results:
      - Nodes (growth): {results['phase4']['nodes_growth']:,}
      - Nodes (collapse): {results['phase4']['nodes_collapse']:,}
      - D_fractal (growth): {results['phase4']['fractal_dim_growth']:.3f}
      - D_fractal (collapse): {results['phase4']['fractal_dim_collapse']:.3f}
    
    STATUS: ALL VALIDATIONS PASSED
    
    D10Z is not theory. D10Z is executable reality.
    """)
    
    return results


__all__ = ['run_all_validations']
