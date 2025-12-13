import numpy as np
from ..states import to_density_matrix
from ..bipartite import partial_trace

def _safe_eigvals(rho):
    evals = np.linalg.eigvalsh(rho)
    evals = np.real_if_close(evals)
    evals[evals < 0] = 0.0
    return evals

def von_neumann_entropy(rho, base=2):
    rho = to_density_matrix(rho)
    evals = _safe_eigvals(rho)
    evals = evals[evals > 0]
    if evals.size == 0:
        return 0.0
    log_fn = np.log2 if base == 2 else np.log
    return float(-np.sum(evals * log_fn(evals)))

def linear_entropy(rho):
    rho = to_density_matrix(rho)
    return float(1.0 - np.trace(rho @ rho).real)

def renyi_entropy(rho, alpha=2, base=2):
    if alpha == 1:
        return von_neumann_entropy(rho, base=base)
    rho = to_density_matrix(rho)
    evals = _safe_eigvals(rho)
    evals = evals[evals > 0]
    if evals.size == 0:
        return 0.0
    tr_alpha = np.sum(evals**alpha)
    log_fn = np.log2 if base == 2 else np.log
    return float((1.0 / (1.0 - alpha)) * log_fn(tr_alpha))

def mutual_information(rho_ab, dims, base=2):
    rho_ab = to_density_matrix(rho_ab)
    rho_a = partial_trace(rho_ab, dims, traced_system="B")
    rho_b = partial_trace(rho_ab, dims, traced_system="A")
    s_ab = von_neumann_entropy(rho_ab, base=base)
    s_a = von_neumann_entropy(rho_a, base=base)
    s_b = von_neumann_entropy(rho_b, base=base)
    return float(s_a + s_b - s_ab)

def entropy_features(rho, dims=None, base=2):
    """
    Compute basic entropy-related features for a state.

    If dims is provided and len(dims) == 2, also computes mutual information.
    """
    feats = {}
    feats["S_vN"] = von_neumann_entropy(rho, base=base)
    feats["S_linear"] = linear_entropy(rho)
    feats["S_Renyi_2"] = renyi_entropy(rho, alpha=2, base=base)

    if dims is not None and len(dims) == 2:
        feats["I_A_B"] = mutual_information(rho, dims=dims, base=base)
    return feats
