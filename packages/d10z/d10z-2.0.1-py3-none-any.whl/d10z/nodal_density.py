 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/nodal_density.py b/nodal_density.py
new file mode 100644
index 0000000000000000000000000000000000000000..6feb53b6bb1ab990440d6bdfe4609bee5d4afc84
--- /dev/null
+++ b/nodal_density.py
@@ -0,0 +1,26 @@
+"""
+Nodal density estimators.
+"""
+
+import numpy as np
+
+
+def radial_density(r: np.ndarray, Z: np.ndarray, sigma: float = 1.0) -> np.ndarray:
+    """
+    Compute a smoothed radial density profile ρ_n(r).
+
+    ρ_n(r) = Σ |Zₙ|² · exp(-(r - rₙ)² / 2σ²)
+    """
+    if r.shape != Z.shape:
+        raise ValueError("r and Z must have same shape")
+    amplitudes = np.abs(Z) ** 2
+    profile = amplitudes * np.exp(-((r - r.mean()) ** 2) / (2 * sigma ** 2))
+    return profile
+
+
+def mean_density(Z: np.ndarray, volume: float) -> float:
+    """⟨ρ_n⟩ = Σ |Zₙ|² / V"""
+    return float(np.sum(np.abs(Z) ** 2) / volume)
+
+
+__all__ = ["radial_density", "mean_density"]
 
EOF
)