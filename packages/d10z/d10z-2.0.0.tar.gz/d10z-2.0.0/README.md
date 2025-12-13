from d10z import (
    Constants, Infifoton, TTAMesh,
    BigStart, LeySahana, LeyIsis,
    UniversalForce, NodalDensity,
    GalacticRotation, Z_pillar, N_pillar,
    fv_universal
)

# Nodo Z0 (Big Start)
Z0 = BigStart.initialize_node_zero()

# Infifotón
inf = Infifoton(frequency=7.83)

# Malla TTA
mesh = TTAMesh(N=100, dimension=10)
lambda2 = mesh.lambda2()

# Fuerza universal
F = UniversalForce.compute(frequency=7.83, velocity=1e3, nodal_density=1e26)

# Ley Sahana en un sistema aleatorio
import numpy as np
Z = np.random.rand(100)
Z_new = LeySahana.apply(Z, mesh.C_ij)

# Ley Isis
H = LeyIsis.harmony_index(Z_new, mesh.C_ij)

# Z, N, F=f·v(Zn)
from d10z import Z_pillar, N_pillar, fv_universal
