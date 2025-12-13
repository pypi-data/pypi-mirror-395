import numpy as np
from ..states import to_density_matrix
from .entropy import von_neumann_entropy

def l1_coherence(rho):
    rho = to_density_matrix(rho)
    off_diag = rho - np.diag(np.diag(rho))
    return float(np.sum(np.abs(off_diag)))

def relative_entropy_coherence(rho, base=2):
    rho = to_density_matrix(rho)
    diag = np.diag(np.diag(rho))
    return float(von_neumann_entropy(diag, base=base) - von_neumann_entropy(rho, base=base))

def coherence_features(rho, base=2):
    return {
        "C_l1": l1_coherence(rho),
        "C_rel_entropy": relative_entropy_coherence(rho, base=base),
    }
