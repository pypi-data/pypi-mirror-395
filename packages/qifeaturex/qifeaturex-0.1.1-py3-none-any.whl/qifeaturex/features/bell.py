import numpy as np
from ..states import to_density_matrix

def chsh_violation(rho):
    """
    Compute maximal Bell-CHSH violation for a 2-qubit state.
    Returns value > 2.0 if nonlocal.
    """
    rho = to_density_matrix(rho)
    if rho.shape != (4,4):
        return None

    # correlation matrix T
    pauli = [
        np.array([[1,0],[0,1]]),
        np.array([[0,1],[1,0]]),
        np.array([[0,-1j],[1j,0]]),
        np.array([[1,0],[0,-1]])
    ]

    T = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            op = np.kron(pauli[i+1], pauli[j+1])
            T[i,j] = np.real(np.trace(rho @ op))

    # singular values
    evals = np.linalg.svd(T, compute_uv=False)
    s1, s2, _ = evals
    Bmax = 2 * np.sqrt(s1**2 + s2**2)

    return float(Bmax)
