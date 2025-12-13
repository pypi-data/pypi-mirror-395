import numpy as np

def to_density_matrix(psi_or_rho: np.ndarray) -> np.ndarray:
    """
    Ensure the input is a density matrix.

    If a statevector |psi> is given (shape (d,)),
    convert to rho = |psi><psi|.
    If a matrix is given, return as-is.
    """
    arr = np.asarray(psi_or_rho)
    if arr.ndim == 1:
        psi = arr.reshape(-1, 1)
        rho = psi @ psi.conj().T
        # normalize trace
        tr = np.trace(rho)
        if tr != 0:
            rho = rho / tr
        return rho
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        # normalize trace
        tr = np.trace(arr)
        if tr != 0:
            arr = arr / tr
        return arr
    else:
        raise ValueError("Input must be a statevector (d,) or density matrix (d,d).")


def is_density_matrix(rho: np.ndarray, tol: float = 1e-8) -> bool:
    rho = np.asarray(rho)
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        return False
    # Hermitian
    if not np.allclose(rho, rho.conj().T, atol=tol):
        return False
    # Positive semidefinite approx: eigenvalues non-negative
    evals = np.linalg.eigvalsh(rho)
    if np.min(evals) < -tol:
        return False
    # Trace ~ 1
    tr = np.trace(rho)
    if not np.allclose(tr, 1.0, atol=tol):
        return False
    return True
