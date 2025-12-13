 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/flower_of_life.py b/flower_of_life.py
index cc67c9394c30ca941a7c4c0209df35597b6de953..1aaccd0f47ec5a306c688ca412f7de6a78d0ac9d 100644
--- a/flower_of_life.py
+++ b/flower_of_life.py
@@ -1,44 +1,45 @@
 # ═══════════════════════════════════════════════════════════════════════════════
 # d10z/bigstart/flower_of_life.py
 # FLOWER OF LIFE GEOMETRY - PRIMORDIAL STRUCTURE
 # ═══════════════════════════════════════════════════════════════════════════════
 """
 Flower of Life Geometry
 
 The Flower of Life is the primordial geometry of Big Start.
 19 nodes arranged in sacred hexagonal pattern.
 
 This is NOT arbitrary - it is the natural geometry that emerges
 from coherence dynamics. The Flower of Life appears across all
 scales because it is a fundamental attractor of nodal systems.
 """
 
 import numpy as np
 from dataclasses import dataclass
-from typing import List, Tuple, Optional
-from ..core.constants import FLOWER_OF_LIFE_NODES, PHI_CRITICAL
+from typing import List, Optional, Tuple
+
+from constants import FLOWER_OF_LIFE_NODES, PHI_CRITICAL
 
 
 @dataclass
 class FlowerOfLife:
     """
     The Flower of Life sacred geometry.
     
     19 nodes in hexagonal arrangement:
     - 1 center node
     - 6 first ring nodes
     - 12 second ring nodes
     
     Attributes
     ----------
     positions : np.ndarray
         3D positions of all nodes (19, 3)
     scale : float
         Spatial scale of the pattern
     center : np.ndarray
         Center position
     """
     positions: np.ndarray
     scale: float
     center: np.ndarray
     
 
EOF
)