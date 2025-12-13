 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/infifoton.py b/infifoton.py
new file mode 100644
index 0000000000000000000000000000000000000000..1a7906e2f66fd62c4ab5541c0ea99dbaed4f26fe
--- /dev/null
+++ b/infifoton.py
@@ -0,0 +1,36 @@
+"""
+Infifotón utilities.
+
+Provides helper functions around the fundamental quantum ε_ifi defined in
+:mod:`constants`.
+"""
+
+from typing import Union
+
+from ..core.constants import EPSILON_IFI, infifoton_count, infifoton_energy
+
+Number = Union[int, float]
+
+
+def energy_from_count(n_ifi: Number) -> float:
+    """E = N·ε_ifi"""
+    return infifoton_energy(int(n_ifi))
+
+
+def count_from_energy(energy: float) -> int:
+    """N = round(E / ε_ifi)"""
+    return infifoton_count(energy)
+
+
+def infifoton_flux(power: float) -> float:
+    """
+    Convert a power (J/s) into an infifotón flux (ifi/s).
+    """
+    return power / EPSILON_IFI
+
+
+__all__ = [
+    "energy_from_count",
+    "count_from_energy",
+    "infifoton_flux",
+]
 
EOF
)