 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/gm1051.py b/gm1051.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a3d76c93790c95d35d566749625f48e4fd1407
--- /dev/null
+++ b/gm1051.py
@@ -0,0 +1,35 @@
+"""
+GM·10⁻⁵¹ scale utilities.
+
+These helpers expose conversions and parameter retrieval for the
+fundamental GM table defined in :mod:`constants`.
+"""
+
+from typing import Dict, Union
+
+from ..core.constants import GM_TABLE, GM_SCALE, get_gm_parameters
+
+Number = Union[int, float, str]
+
+
+def gm_params(scale: Number = GM_SCALE) -> Dict[str, float]:
+    """
+    Fetch parameter set for a given scale from the GM table.
+    """
+    params = get_gm_parameters(scale)
+    if params is None:
+        raise KeyError(f"Scale {scale} not found in GM_TABLE")
+    return params
+
+
+def gm_frequency(scale: Number = GM_SCALE) -> float:
+    """Return intrinsic frequency f at the requested scale."""
+    return gm_params(scale)["f"]
+
+
+def gm_period(scale: Number = GM_SCALE) -> float:
+    """Return intrinsic period T at the requested scale."""
+    return gm_params(scale)["T"]
+
+
+__all__ = ["gm_params", "gm_frequency", "gm_period"]
 
EOF
)