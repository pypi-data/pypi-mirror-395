from numba import cuda, float32
from numba.cuda.libdevice import expf, powf, fmaxf
import numpy as np
from .constants import EPS, ONE, NEG_HALF, gaussian_factor


@cuda.jit("float32(float32, float32)", device=True, inline=True, fastmath=True)
def gaussian(x, sigma):
    sigma = fmaxf(sigma, EPS)
    inv   = ONE / sigma
    t     = x * inv
    arg   = NEG_HALF * t * t
    return (gaussian_factor * inv) * expf(arg)

@cuda.jit("float32(float32, float32)", device=True, inline=True, fastmath=True)
def exponential(x, sigma):
    sigma = fmaxf(sigma, EPS)
    inv   = ONE / sigma
    return inv * expf(-x * inv)

@cuda.jit("float32(float32, float32, float32)", device=True, inline=True, fastmath=True)
def power_law(x, sigma, n):
    sigma = fmaxf(sigma, EPS)
    n     = fmaxf(n, np.float32(1.0001))
    inv   = ONE / sigma
    t     = x * inv
    norm  = (n - ONE) * inv
    value = ONE / (ONE + powf(t, n))
    return norm * value

@cuda.jit("float32(float32, float32, float32, float32, float32, float32, float32, float32)", device=True, inline=True, fastmath=True)
def PDF(x, A, sigma, s2, s3, n, w1, w2):
    f1 = w1
    f2 = w2 * (ONE - w1)
    f3 = (ONE - w1) * (ONE - w2)

    sigma1 = sigma
    sigma2 = s2 * sigma
    sigma3 = s3 * sigma

    g_ = gaussian(x, sigma1)
    p_ = power_law(x, sigma2, n)
    e_ = exponential(x, sigma3)

    return A * (f1 * g_ + f2 * p_ + f3 * e_)


