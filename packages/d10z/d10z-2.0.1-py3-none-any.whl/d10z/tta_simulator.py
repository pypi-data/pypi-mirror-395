 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/tta_simulator.py b/tta_simulator.py
new file mode 100644
index 0000000000000000000000000000000000000000..db4b6df231856de8cda798510b05d2a46c3f16f5
--- /dev/null
+++ b/tta_simulator.py
@@ -0,0 +1,124 @@
+"""
+TTA Simulation CLI
+
+Provides a minimal quantification and simulation helper for the
+Flower-of-Life style network described in the GM10⁻⁵¹ framework. It
+combines the existing filament and flower geometry utilities to create
+an energy report for a given number of timesteps.
+"""
+from __future__ import annotations
+
+import argparse
+import json
+from dataclasses import asdict, dataclass
+from typing import List
+
+from constants import C_EMERGENT
+from filaments import (
+    FilamentPair,
+    create_filament_network,
+    total_infifotons,
+    total_network_energy,
+)
+from flower_of_life import create_flower_geometry
+
+
+@dataclass
+class SimulationResult:
+    """Aggregated metrics from a filament simulation."""
+
+    steps: int
+    kappa_E: float
+    total_energy: float
+    total_infifotons: int
+    equivalent_mass: float
+
+    def to_json(self) -> str:
+        """Return a JSON formatted string for downstream tooling."""
+
+        return json.dumps(asdict(self), indent=2)
+
+
+def run_simulation(
+    steps: int = 10,
+    dt: float = 0.1,
+    kappa_E: float = 1.0,
+    seed: int | None = None,
+) -> SimulationResult:
+    """
+    Evolve a 19-node Flower-of-Life network and quantify output.
+
+    Parameters
+    ----------
+    steps : int
+        Number of discrete timesteps to evolve.
+    dt : float
+        Time step size.
+    kappa_E : float
+        Coupling factor applied to f×v energy generation.
+    seed : int, optional
+        Deterministic seed for reproducibility.
+    """
+
+    # Build spatial scaffold first so callers can visualize if needed.
+    create_flower_geometry()
+
+    pairs: List[FilamentPair] = create_filament_network(
+        n_pairs=19, arrangement="flower", seed=seed
+    )
+
+    for _ in range(steps):
+        for pair in pairs:
+            pair.evolve(dt)
+
+    total_energy = total_network_energy(pairs, kappa_E=kappa_E)
+    n_ifi = total_infifotons(pairs, kappa_E=kappa_E)
+    equivalent_mass = total_energy / (C_EMERGENT**2)
+
+    return SimulationResult(
+        steps=steps,
+        kappa_E=kappa_E,
+        total_energy=total_energy,
+        total_infifotons=n_ifi,
+        equivalent_mass=equivalent_mass,
+    )
+
+
+def main() -> None:
+    parser = argparse.ArgumentParser(
+        description=(
+            "Quantify the GM10-51 Flower-of-Life network by evolving paired "
+            "frequency/vibration filaments and reporting energy, infifotons, "
+            "and equivalent mass."
+        )
+    )
+    parser.add_argument("--steps", type=int, default=10, help="Number of timesteps to evolve")
+    parser.add_argument("--dt", type=float, default=0.1, help="Size of each timestep")
+    parser.add_argument(
+        "--kappa", type=float, default=1.0, help="Coupling factor applied to f×v energy"
+    )
+    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
+    parser.add_argument(
+        "--format",
+        choices=["json", "text"],
+        default="text",
+        help="Output format for the summary",
+    )
+
+    args = parser.parse_args()
+    result = run_simulation(steps=args.steps, dt=args.dt, kappa_E=args.kappa, seed=args.seed)
+
+    if args.format == "json":
+        print(result.to_json())
+    else:
+        print("TTA GM10-51 Simulation Summary")
+        print("------------------------------")
+        print(f"Steps: {result.steps}")
+        print(f"Coupling (kappa_E): {result.kappa_E:.3f}")
+        print(f"Total energy: {result.total_energy:.6e} J")
+        print(f"Infifotons: {result.total_infifotons}")
+        print(f"Equivalent mass: {result.equivalent_mass:.6e} kg")
+
+
+if __name__ == "__main__":
+    main()
 
EOF
)