 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/universal_force.py b/universal_force.py
new file mode 100644
index 0000000000000000000000000000000000000000..03d66596cb0eefed814c16b65a3f809c3753e435
--- /dev/null
+++ b/universal_force.py
@@ -0,0 +1,27 @@
+"""
+Universal force density emerging from coherence gradients and nodal density.
+
+F_U = κ · ρ_n · ||∇Φ||
+"""
+
+import numpy as np
+
+
+def universal_force_density(coherence_gradient: np.ndarray, nodal_density: np.ndarray, kappa: float = 1e-3) -> np.ndarray:
+    """
+    Compute force density F_U at each node.
+    """
+    if coherence_gradient.shape != nodal_density.shape:
+        raise ValueError("Gradient and nodal density must match in shape")
+    grad_norm = np.linalg.norm(coherence_gradient, axis=0)
+    return kappa * nodal_density * grad_norm
+
+
+def universal_acceleration(force_density: np.ndarray, mass_density: np.ndarray) -> np.ndarray:
+    """a = F/ρ_m"""
+    if force_density.shape != mass_density.shape:
+        raise ValueError("Force density and mass density must match in shape")
+    return force_density / (mass_density + 1e-30)
+
+
+__all__ = ["universal_force_density", "universal_acceleration"]
 
EOF
)