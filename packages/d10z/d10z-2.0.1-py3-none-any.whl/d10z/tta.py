 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/tta.py b/tta.py
new file mode 100644
index 0000000000000000000000000000000000000000..d41e1902c985a6579bdf29f3a899d13d543b97c7
--- /dev/null
+++ b/tta.py
@@ -0,0 +1,74 @@
+"""
+Core Temporal Tensorial Architecture (TTA) equations.
+
+This module collects closed-form relations that tie together the
+frequency/vibration filaments, nodal states Zₙ, and coherence fields Φ.
+It complements :mod:`architecture` by exposing the algebraic forms used
+throughout the framework.
+"""
+
+from typing import Iterable
+import numpy as np
+
+from .architecture import compute_F
+from .coherence import sahana_law, isis_law
+from ..core.constants import EPSILON_IFI
+
+
+def master_equation(f: Iterable[float], v: Iterable[float], Z: np.ndarray) -> np.ndarray:
+    """
+    Evaluate F = f · v(Zₙ) element-wise for an array of nodes.
+
+    Parameters
+    ----------
+    f, v : Iterable[float]
+        Frequency and vibration values per node.
+    Z : np.ndarray
+        Complex nodal array Zₙ.
+    """
+    f = np.asarray(list(f))
+    v = np.asarray(list(v))
+    if Z.shape[0] != f.shape[0] or v.shape[0] != f.shape[0]:
+        raise ValueError("f, v, and Z must have matching lengths")
+    return np.array([compute_F(fi, vi, zi) for fi, vi, zi in zip(f, v, Z)])
+
+
+def nodal_energy(Z: np.ndarray) -> float:
+    """
+    Compute emergent energy stored in the nodal field.
+
+    E = ε_ifi · Σ |Zₙ|²
+    """
+    return EPSILON_IFI * float(np.sum(np.abs(Z) ** 2))
+
+
+def evolve_step(Z: np.ndarray, connectivity: np.ndarray, F: np.ndarray, dt: float = 0.01) -> np.ndarray:
+    """
+    One-step evolution including Sahana (coherence) and Isis (tension) terms.
+
+    dZ/dt = Sahana(Z) + Isis(Z) + α·F·Z/|Z|
+    """
+    sahana_term = sahana_law(Z, connectivity)
+    isis_term = isis_law(Z)
+    alpha = 0.001
+    driving = alpha * F * Z / (np.abs(Z) + 1e-10)
+    return Z + dt * (sahana_term + isis_term + driving)
+
+
+def coherence_reduction(Z: np.ndarray) -> float:
+    """
+    Fractional reduction of nodal fragmentation: 1 - Var(|Zₙ|)/⟨|Zₙ|⟩²
+    """
+    amplitudes = np.abs(Z)
+    mean_amp = np.mean(amplitudes)
+    if mean_amp == 0:
+        return 0.0
+    return 1.0 - np.var(amplitudes) / (mean_amp ** 2)
+
+
+__all__ = [
+    "master_equation",
+    "nodal_energy",
+    "evolve_step",
+    "coherence_reduction",
+]
 
EOF
)