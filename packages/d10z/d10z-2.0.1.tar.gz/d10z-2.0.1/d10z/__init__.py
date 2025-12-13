 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/__init__.py b/__init__.py
index 589762d4327fd94774f7a1934dfbb6d51fc04809..356068a5ed4aaf3f1c496e971ce55291837568a2 100644
--- a/__init__.py
+++ b/__init__.py
@@ -14,31 +14,97 @@ TTA consists of:
 - Nodal dynamics: F = f·v(Zₙ)
 
 Time and space are NOT fundamental - they EMERGE from TTA.
 """
 
 from .filaments import (
     Filament,
     FrequencyFilament,
     VibrationFilament,
     FilamentPair,
     create_filament_network
 )
 
 from .architecture import (
     TTANetwork,
     compute_F,
     tta_evolution
 )
 
 from .neusars import (
     Neusar,
     NeusarCluster,
     neusar_consciousness
 )
 
+# Analytical helpers
+from .big_start import (
+    BigStartProfile,
+    ignition_energy_density,
+    infifoton_yield,
+    ignition_status,
+)
+from .tta import (
+    master_equation,
+    nodal_energy,
+    evolve_step,
+    coherence_reduction,
+)
+from .omdi import (
+    omdi_invariant,
+    omdi_metric,
+)
+from .fv_relation import (
+    fv_scalar,
+    fv_vector,
+    fv_coherence_amplifier,
+)
+from .infifoton import (
+    energy_from_count,
+    count_from_energy,
+    infifoton_flux,
+)
+from .gm1051 import (
+    gm_params,
+    gm_frequency,
+    gm_period,
+)
+from .sahana_law import sahana
+from .isis_law import isis
+from .zn import (
+    amplitude,
+    phase,
+    normalize,
+    coherence,
+)
+from .galactic_rotation import rotation_curve
+from .nodal_density import (
+    radial_density,
+    mean_density,
+)
+from .universal_force import (
+    universal_force_density,
+    universal_acceleration,
+)
+from .n_field import (
+    evolve_n_field,
+    occupation_fraction,
+)
+
 __all__ = [
     'Filament', 'FrequencyFilament', 'VibrationFilament',
     'FilamentPair', 'create_filament_network',
     'TTANetwork', 'compute_F', 'tta_evolution',
-    'Neusar', 'NeusarCluster', 'neusar_consciousness'
+    'Neusar', 'NeusarCluster', 'neusar_consciousness',
+    'BigStartProfile', 'ignition_energy_density', 'infifoton_yield', 'ignition_status',
+    'master_equation', 'nodal_energy', 'evolve_step', 'coherence_reduction',
+    'omdi_invariant', 'omdi_metric',
+    'fv_scalar', 'fv_vector', 'fv_coherence_amplifier',
+    'energy_from_count', 'count_from_energy', 'infifoton_flux',
+    'gm_params', 'gm_frequency', 'gm_period',
+    'sahana', 'isis',
+    'amplitude', 'phase', 'normalize', 'coherence',
+    'rotation_curve',
+    'radial_density', 'mean_density',
+    'universal_force_density', 'universal_acceleration',
+    'evolve_n_field', 'occupation_fraction'
 ]
 
EOF
)