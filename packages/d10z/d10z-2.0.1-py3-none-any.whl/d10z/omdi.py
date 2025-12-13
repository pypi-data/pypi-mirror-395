 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/omdi.py b/omdi.py
new file mode 100644
index 0000000000000000000000000000000000000000..1f835c9d76ea1a24ea6f0f141e41c245b366fd69
--- /dev/null
+++ b/omdi.py
@@ -0,0 +1,46 @@
+"""
+OmDi (Omni-Dimensional Invariant)
+
+Quantifies how a nodal/coherence configuration projects across nested
+dimensional layers. The invariant is defined as a weighted sum of coherence
+gradient magnitudes across D dimensions.
+
+Ω_DI = Σ_d w_d · ||∇Φ_d||²
+"""
+
+from typing import Iterable
+import numpy as np
+
+
+def omdi_invariant(gradients: Iterable[np.ndarray], weights: Iterable[float] = None) -> float:
+    """
+    Compute the Omni-Dimensional invariant Ω_DI.
+
+    Parameters
+    ----------
+    gradients : Iterable[np.ndarray]
+        Gradient components ∇Φ_d for each dimensional slice.
+    weights : Iterable[float], optional
+        Weights w_d (defaults to uniform).
+    """
+    grads = list(gradients)
+    if weights is None:
+        weights = [1.0] * len(grads)
+    weights = np.asarray(list(weights))
+    if len(weights) != len(grads):
+        raise ValueError("weights must match number of gradient components")
+    norm_terms = [wd * float(np.sum(gd ** 2)) for wd, gd in zip(weights, grads)]
+    return float(np.sum(norm_terms))
+
+
+def omdi_metric(gradients: Iterable[np.ndarray], coherence: float) -> float:
+    """
+    Normalized OmDi metric combining Ω_DI with mean coherence Φ̄.
+
+    M_omdi = Ω_DI · Φ̄ / (1 + Ω_DI)
+    """
+    omega = omdi_invariant(gradients)
+    return omega * coherence / (1.0 + omega)
+
+
+__all__ = ["omdi_invariant", "omdi_metric"]
 
EOF
)