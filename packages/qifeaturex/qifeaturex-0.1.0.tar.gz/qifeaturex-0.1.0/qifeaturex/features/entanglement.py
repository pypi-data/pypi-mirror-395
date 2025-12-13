import numpy as np
from ..states import to_density_matrix
from ..bipartite import partial_trace

def concurrence_two_qubit(rho):
    """
    Wootters concurrence for two-qubit density matrix.
    rho must be 4x4.
    """
    rho = to_density_matrix(rho)
    if rho.shape != (4, 4):
        raise ValueError("concurrence_two_qubit only supports 2-qubit (4x4) states.")

    sigma_y = np.array([[0, -1j],
                        [1j,  0]])
    sy_sy = np.kron(sigma_y, sigma_y)

    rho_conj = rho.conj()
    R = rho @ sy_sy @ rho_conj @ sy_sy
    evals = np.linalg.eigvals(R)
    evals = np.sort(np.sqrt(np.real_if_close(evals)))[::-1]
    c = max(0.0, float(evals[0] - np.sum(evals[1:])))
    return c

def negativity_two_qubit(rho, dims=(2, 2)):
    rho = to_density_matrix(rho)
    dA, dB = dims
    rho_reshaped = rho.reshape(dA, dB, dA, dB)
    rho_pt = rho_reshaped.swapaxes(1, 3).reshape(dA * dB, dA * dB)
    evals = np.linalg.eigvalsh(rho_pt)
    neg = np.sum(np.abs(evals[evals < 0]))
    return float(neg)

def log_negativity_two_qubit(rho, dims=(2, 2), base=2):
    neg = negativity_two_qubit(rho, dims=dims)
    trace_norm = 1 + 2 * neg
    log_fn = np.log2 if base == 2 else np.log
    return float(log_fn(trace_norm))

def entanglement_entropy_pure(rho_ab, dims, base=2):
    rho_a = partial_trace(rho_ab, dims, traced_system="B")
    from .entropy import von_neumann_entropy
    return von_neumann_entropy(rho_a, base=base)

def entanglement_features(rho, dims=(2, 2), base=2):
    """
    Basic entanglement features for 2-qubit-like systems.
    """
    feats = {}
    try:
        C = concurrence_two_qubit(rho)
        feats["C_concurrence"] = C
        feats["tangle"] = C**2
    except ValueError:
        feats["C_concurrence"] = None
        feats["tangle"] = None

    try:
        feats["negativity"] = negativity_two_qubit(rho, dims=dims)
        feats["log_negativity"] = log_negativity_two_qubit(rho, dims=dims, base=base)
    except ValueError:
        feats["negativity"] = None
        feats["log_negativity"] = None

    from .entropy import von_neumann_entropy
    s_rho = von_neumann_entropy(rho, base=base)
    if s_rho < 1e-6:
        feats["S_ent_A"] = entanglement_entropy_pure(rho, dims=dims, base=base)
    else:
        feats["S_ent_A"] = None

    return feats
