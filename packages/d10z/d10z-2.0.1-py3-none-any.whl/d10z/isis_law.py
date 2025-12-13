 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/isis_law.py b/isis_law.py
new file mode 100644
index 0000000000000000000000000000000000000000..3ade3f9f571302897b85fa120ef96b649e7ab500
--- /dev/null
+++ b/isis_law.py
@@ -0,0 +1,22 @@
+"""
+Isis Law (Harmonic Resonance).
+
+Wraps :func:`coherence.isis_law` to expose the analytical expression used
+throughout the framework.
+"""
+
+import numpy as np
+
+from .coherence import isis_law as _isis_law
+
+
+def isis(Z: np.ndarray, sigma: float = None) -> np.ndarray:
+    """
+    f_LI(φ₁, φ₂) = cos(φ₁ - φ₂) · exp(-|D₁ - D₂|² / 2σ²)
+    """
+    if sigma is None:
+        return _isis_law(Z)
+    return _isis_law(Z, sigma=sigma)
+
+
+__all__ = ["isis"]
 
EOF
)