 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/fv_relation.py b/fv_relation.py
new file mode 100644
index 0000000000000000000000000000000000000000..6f724973aa0d22d0425c1b2453ce5fba2f360476
--- /dev/null
+++ b/fv_relation.py
@@ -0,0 +1,35 @@
+"""
+Fundamental relation F = f · v(Zₙ).
+
+This module exposes helper functions to compute the coupling between
+frequency filaments, vibration filaments, and nodal amplitudes.
+"""
+
+import numpy as np
+
+from .architecture import compute_F
+
+
+def fv_scalar(f: float, v: float, Z_n: complex) -> float:
+    """Return the scalar F for a single node."""
+    return compute_F(f, v, Z_n)
+
+
+def fv_vector(f: np.ndarray, v: np.ndarray, Z: np.ndarray) -> np.ndarray:
+    """
+    Vectorized computation of F = f · v(Zₙ) for multiple nodes.
+    """
+    if f.shape != v.shape or f.shape != Z.shape:
+        raise ValueError("f, v, and Z must share the same shape")
+    return f * v * np.abs(Z)
+
+
+def fv_coherence_amplifier(F: np.ndarray, phi: float, beta: float = 0.05) -> np.ndarray:
+    """
+    Amplify F based on coherence Φ using:
+    F_eff = F · (1 + β·Φ)
+    """
+    return F * (1.0 + beta * phi)
+
+
+__all__ = ["fv_scalar", "fv_vector", "fv_coherence_amplifier"]
 
EOF
)