import numpy as np

def partial_trace(rho, dims, traced_system="B"):
    """
    Partial trace over subsystem B or A for a bipartite state.

    rho: density matrix of shape (d, d)
    dims: (dA, dB)
    traced_system: "A" or "B"

    Returns: reduced density matrix rho_A or rho_B.
    """
    rho = np.asarray(rho)
    dA, dB = dims
    d = dA * dB
    if rho.shape != (d, d):
        raise ValueError(f"rho shape {rho.shape} incompatible with dims {dims}.")

    rho_reshaped = rho.reshape(dA, dB, dA, dB)

    if traced_system == "B":
        # trace over B indices
        return np.einsum("ijik->jk", rho_reshaped)
    elif traced_system == "A":
        # trace over A indices
        return np.einsum("iijk->jk", rho_reshaped)
    else:
        raise ValueError('traced_system must be "A" or "B".')
