 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/big_start.py b/big_start.py
new file mode 100644
index 0000000000000000000000000000000000000000..787a0e08eaed09d818576508be8764e321759905
--- /dev/null
+++ b/big_start.py
@@ -0,0 +1,100 @@
+# ═══════════════════════════════════════════════════════════════════════════════
+# d10z/tta/big_start.py
+# BIG START FORMULATION (IGNITION DYNAMICS)
+# ═══════════════════════════════════════════════════════════════════════════════
+"""
+Big Start Formulation
+
+Mathematical envelope for the ignition process (Φ → 1) that defines the
+"Big Start" in the D10Z framework. The functions provided here do not replace
+`ignition.py`; they provide closed-form relations that are algebraically
+consistent with the nodal dynamics used elsewhere in the package.
+
+Key relations
+-------------
+1. **Coherence ramp** (logistic approach to Φ → 1):
+   Φ(t) = 1 - (1 - Φ₀)·exp(-t/τ)
+
+2. **Ignition energy density** (per GM·10⁻⁵¹ volume element):
+   ρ_E = (Φ / GM) · ε_ifi · ρ_n
+
+3. **Infifotón yield** from a coherent domain:
+   N_ifi = ρ_E · V / ε_ifi
+"""
+
+from dataclasses import dataclass
+from typing import Tuple
+import numpy as np
+
+from ..core.constants import (
+    EPSILON_IFI,
+    GM_SCALE,
+    PHI_IGNITION,
+)
+
+
+@dataclass
+class BigStartProfile:
+    """
+    Analytic profile of a coherence ramp toward ignition.
+
+    Attributes
+    ----------
+    phi_0 : float
+        Initial coherence Φ₀
+    tau : float
+        Characteristic ramp time τ (internal units)
+    """
+
+    phi_0: float = 0.8
+    tau: float = 1.0
+
+    def phi(self, t: float) -> float:
+        """Compute Φ(t) = 1 - (1 - Φ₀)·exp(-t/τ)."""
+        return 1.0 - (1.0 - self.phi_0) * np.exp(-t / self.tau)
+
+    def time_to_threshold(self, threshold: float = PHI_IGNITION) -> float:
+        """Return the time required for Φ(t) to reach a given threshold."""
+        if threshold <= self.phi_0:
+            return 0.0
+        return -self.tau * np.log(1.0 - threshold) + self.tau * np.log(1.0 - self.phi_0)
+
+
+def ignition_energy_density(phi: float, nodal_density: float) -> float:
+    """
+    Energy density released at Big Start per GM·10⁻⁵¹ volume element.
+
+    ρ_E = (Φ / GM) · ε_ifi · ρ_n
+    """
+    return (phi / GM_SCALE) * EPSILON_IFI * nodal_density
+
+
+def infifoton_yield(phi: float, nodal_density: float, volume: float) -> float:
+    """
+    Estimate number of infifotóns produced in a coherent domain.
+
+    N_ifi = ρ_E · V / ε_ifi
+    """
+    rho_E = ignition_energy_density(phi, nodal_density)
+    return rho_E * volume / EPSILON_IFI
+
+
+def ignition_status(phi_mean: float) -> Tuple[bool, float]:
+    """
+    Convenience wrapper around :func:`check_ignition_condition` for scalar Φ.
+
+    Parameters
+    ----------
+    phi_mean : float
+        Global coherence value.
+    """
+    ready = phi_mean >= PHI_IGNITION
+    return ready, phi_mean
+
+
+__all__ = [
+    "BigStartProfile",
+    "ignition_energy_density",
+    "infifoton_yield",
+    "ignition_status",
+]
 
EOF
)