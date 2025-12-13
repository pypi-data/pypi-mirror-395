 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/galactic_rotation.py b/galactic_rotation.py
new file mode 100644
index 0000000000000000000000000000000000000000..b476991e23a6667ad63c9cd4644d3da79335c502
--- /dev/null
+++ b/galactic_rotation.py
@@ -0,0 +1,34 @@
+"""
+Galactic rotation curve in the TTA framework.
+
+Implements the analytic form used in the README:
+
+v²(r) = v²_baryon(r) · [1 + α·ln(r/r₀) + β·(r/r₀)^γ]
+"""
+
+import numpy as np
+
+
+def rotation_curve(r: np.ndarray, v_baryon: np.ndarray, alpha: float = 1.0, r0: float = 1.0,
+                   beta: float = 0.0, gamma: float = 0.0) -> np.ndarray:
+    """
+    Compute TTA-predicted circular velocity profile.
+
+    Parameters
+    ----------
+    r : np.ndarray
+        Radii (same units as r₀)
+    v_baryon : np.ndarray
+        Baryonic circular velocity contribution
+    alpha, beta, gamma : float
+        TTA correction parameters
+    r0 : float
+        Reference radius r₀
+    """
+    if r.shape != v_baryon.shape:
+        raise ValueError("r and v_baryon must have the same shape")
+    modifier = 1.0 + alpha * np.log(r / r0) + beta * (r / r0) ** gamma
+    return v_baryon * np.sqrt(modifier)
+
+
+__all__ = ["rotation_curve"]
 
EOF
)