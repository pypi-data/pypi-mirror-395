import numpy as np
from ..states import to_density_matrix

def trace_distance(rho, sigma):
    rho = to_density_matrix(rho)
    sigma = to_density_matrix(sigma)
    diff = rho - sigma
    evals = np.linalg.eigvals(diff)
    return float(0.5 * np.sum(np.abs(evals)))

def fidelity(rho, sigma):
    rho = to_density_matrix(rho)
    sigma = to_density_matrix(sigma)
    sqrt_rho = scipy.linalg.sqrtm(rho)
    product = sqrt_rho @ sigma @ sqrt_rho
    eigvals = np.linalg.eigvalsh(product)
    return float((np.sum(np.sqrt(np.abs(eigvals)))) ** 2)

def bures_distance(rho, sigma):
    F = fidelity(rho, sigma)
    return float(np.sqrt(2 * (1 - np.sqrt(F))))

def hs_distance(rho, sigma):
    return float(np.linalg.norm(to_density_matrix(rho) - to_density_matrix(sigma)))
