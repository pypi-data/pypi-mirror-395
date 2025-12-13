 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/filaments.py b/filaments.py
index 578b56acb89212697b331fb58d077cf621974d46..73e21fbe9942ff7c63dd9791f5748129501dc0a5 100644
--- a/filaments.py
+++ b/filaments.py
@@ -1,52 +1,50 @@
 # ═══════════════════════════════════════════════════════════════════════════════
 # d10z/tta/filaments.py
 # TTA FILAMENTS - FREQUENCY AND VIBRATION CARRIERS
 # ═══════════════════════════════════════════════════════════════════════════════
 """
 TTA Filaments
 
 The TTA network consists of filament pairs:
 - Frequency filament (f): Carries frequency information
 - Vibration filament (v): Carries vibration information
 
 These filaments:
 - Have thickness = 0.0000001% of GM·10⁻⁵¹
 - Are separated by 0.0000000000001%
 - Alternate: one f, one v, one f, one v...
 - Contain Neusars in their central cánula
 
 The interaction f × v generates ENERGY, which then produces INFIFOTÓNS.
 """
 
 import numpy as np
 from dataclasses import dataclass, field
 from typing import List, Optional, Tuple
-from ..core.constants import (
-    FILAMENT_THICKNESS, FILAMENT_SEPARATION,
-    GM_SCALE, EPSILON_IFI
-)
+
+from constants import EPSILON_IFI, FILAMENT_SEPARATION, FILAMENT_THICKNESS, GM_SCALE
 
 
 @dataclass
 class Filament:
     """
     Base class for TTA filaments.
     
     Attributes
     ----------
     intensity : float
         Current intensity of the filament
     phase : float
         Phase of oscillation
     position : np.ndarray
         Position of filament endpoint
     filament_type : str
         'frequency' or 'vibration'
     """
     intensity: float = 1.0
     phase: float = 0.0
     position: np.ndarray = field(default_factory=lambda: np.zeros(3))
     filament_type: str = "base"
     
     @property
     def thickness(self) -> float:
 
EOF
)