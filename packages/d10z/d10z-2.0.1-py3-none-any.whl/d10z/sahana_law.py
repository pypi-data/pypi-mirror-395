 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/sahana_law.py b/sahana_law.py
new file mode 100644
index 0000000000000000000000000000000000000000..7552aa8b9054ed6f5937760a25114682a108cfd5
--- /dev/null
+++ b/sahana_law.py
@@ -0,0 +1,22 @@
+"""
+Sahana Law (Coherence Dynamics).
+
+This module re-exports the Sahana formulation from :mod:`coherence` with a
+minimal convenience wrapper.
+"""
+
+import numpy as np
+
+from .coherence import sahana_law as _sahana_law
+
+
+def sahana(Z: np.ndarray, connectivity: np.ndarray, gamma: float = None) -> np.ndarray:
+    """
+    dZ/dt = -γ (Zₙ - Σ_j Cₙⱼ Zⱼ / kₙ)
+    """
+    if gamma is None:
+        return _sahana_law(Z, connectivity)
+    return _sahana_law(Z, connectivity, gamma=gamma)
+
+
+__all__ = ["sahana"]
 
EOF
)