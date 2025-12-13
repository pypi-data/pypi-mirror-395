import numpy as np
from numba import njit, prange

CM2_TO_M2 = 10000  # cm^2 to m^2

P1, P2, P3, P4, P5 = 0.102573, -0.068287, 0.958633, 0.0407253, 0.817285

@njit(cache=True, fastmath=True)
def _cos_theta_star(theta_rad):
    c = np.cos(theta_rad)
    if c > 1.0: c = 1.0
    elif c < -1.0: c = -1.0
    num = c*c + P1*P1 + P2*(c**P3) + P4*(c**P5)
    den = 1.0 + P1*P1 + P2 + P4
    val = num / den
    if val < 0.0: val = 0.0
    return np.sqrt(val)

@njit(cache=True, fastmath=True)
def _dphi0_dE(theta_rad, E_GeV):
    if E_GeV <= 0.0: return 0.0
    cst   = _cos_theta_star(theta_rad)
    x     = E_GeV
    core  = x * (1.0 + 3.64 / (x * (cst**1.29)))
    spec  = 0.14 * (core ** (-2.7))
    dem_pi = 1.0 + 1.1 * x * cst / 115.0
    dem_K  = 1.0 + 1.1 * x * cst / 850.0
    return (spec * ((1.0 / dem_pi) + 0.054 / dem_K)) * CM2_TO_M2

@njit(cache=True, parallel=True, fastmath=True)
def differential_flux(theta_rad_array, E_GeV):
    shape = theta_rad_array.shape
    theta_rad_array = theta_rad_array.flatten()
    flux_array = np.zeros_like(theta_rad_array)
    for i in prange(theta_rad_array.shape[0]):
        if theta_rad_array[i] < 0.0 or theta_rad_array[i] > np.pi / 2:
            flux_array[i] = 0.0
        else:
            flux_array[i] = _dphi0_dE(theta_rad_array[i], E_GeV)

    flux_array = flux_array.reshape(shape)
    return flux_array

