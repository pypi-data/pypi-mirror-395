from numba import njit, prange
import numpy as np
from pathlib import Path

# --- numeric safety knobs (match sr_fitter2_fixed.py) ---
_LOGDIFF_MIN = 1e-300
_DX_MIN      = 1e-300
_EXP_CLIP    = 700.0

# --- globals filled by use_sr_fit(...) ---
_sr_params = None         # flat coeff vector
_sr_sz_dx = _sr_sz_a = _sr_sz_n = _sr_sz_c = 0
_sr_i0_dx = _sr_i0_a = _sr_i0_n = _sr_i0_c = 0

_sr_standardized = 1      # bool as int for Numba
_sr_t_mean = 0.0
_sr_t_std  = 1.0

# link ids: 0 = exp, 1 = identity
_sr_link_dx = 1
_sr_link_a  = 1
_sr_link_n  = 1
_sr_link_c  = 1

_sr_use_n_bounds = 0
_sr_n_min = 0.25
_sr_n_max = 8.0

@njit(cache=True, inline='always')
def _apply_link(x, link_id):
    # 0: exp, 1: identity
    return np.exp(x) if link_id == 0 else x

@njit(cache=True)
def survival_rate(E, T):
    """
    Uses global parameters loaded by use_sr_fit(...).
    Same signature as your original survival_rate(E, T).
    """
    # Standardize thickness if requested
    z = (T - _sr_t_mean) / (_sr_t_std if _sr_t_std != 0.0 else 1.0) if _sr_standardized else T

    # Evaluate thickness polynomials (powers 0..deg)
    gx = 0.0
    for k in range(_sr_sz_dx):
        gx += _sr_params[_sr_i0_dx + k] * (z ** k)

    ga = 0.0
    for k in range(_sr_sz_a):
        ga += _sr_params[_sr_i0_a + k] * (z ** k)

    gn = 0.0
    for k in range(_sr_sz_n):
        gn += _sr_params[_sr_i0_n + k] * (z ** k)

    gc = 0.0
    for k in range(_sr_sz_c):
        gc += _sr_params[_sr_i0_c + k] * (z ** k)

    # Apply links to get dx(t), a(t), n(t), c(t)
    dx = _apply_link(gx, _sr_link_dx)
    a  = _apply_link(ga, _sr_link_a)
    n  = _apply_link(gn, _sr_link_n)
    c  = _apply_link(gc, _sr_link_c)

    # Optional clamp on n
    if _sr_use_n_bounds:
        if n < _sr_n_min:
            n = _sr_n_min
        elif n > _sr_n_max:
            n = _sr_n_max

    # If E <= dx, the law yields zero (blocked)
    dx_safe = dx if dx > _DX_MIN else _DX_MIN
    if E <= dx_safe:
        return 0.0

    # Stable denom = (ln(E) - ln(dx))**n
    logdiff = np.log(E) - np.log(dx_safe)
    if logdiff < _LOGDIFF_MIN:
        logdiff = _LOGDIFF_MIN

    log_denom = n * np.log(logdiff)
    if log_denom >  _EXP_CLIP: log_denom =  _EXP_CLIP
    if log_denom < -_EXP_CLIP: log_denom = -_EXP_CLIP
    denom = np.exp(log_denom)

    # y = c * exp(-a / denom), safely
    ratio = -a / denom
    if ratio >  _EXP_CLIP: ratio =  _EXP_CLIP
    if ratio < -_EXP_CLIP: ratio = -_EXP_CLIP
    return c * np.exp(ratio)

def use_sr_fit(fit_npz_path: str):
    """
    Load the single fitted NPZ and wire up global state for survival_rate(E, T).
    After calling this once, you can keep using `survival_rate(E, T)` everywhere.
    """
    z = np.load(fit_npz_path, allow_pickle=True)

    # flat params and sizes
    params = np.asarray(z["params"], dtype=np.float64)
    deg_dx = int(z["deg_dx"]); deg_a = int(z["deg_a"]); deg_n = int(z["deg_n"]); deg_c = int(z["deg_c"])
    sz_dx = deg_dx + 1; sz_a = deg_a + 1; sz_n = deg_n + 1; sz_c = deg_c + 1

    # indices into params
    i0_dx = 0
    i0_a  = i0_dx + sz_dx
    i0_n  = i0_a  + sz_a
    i0_c  = i0_n  + sz_n

    # links → ids
    link_map = {"exp": 0, "identity": 1}
    link_dx = link_map.get(str(z["link_dx"]), 1)
    link_a  = link_map.get(str(z["link_a" ]), 1)
    link_n  = link_map.get(str(z["link_n" ]), 1)
    link_c  = link_map.get(str(z["link_c" ]), 1)

    # standardization + bounds
    standardized = bool(z["standardized"]) if "standardized" in z else True
    t_mean = float(z["t_mean"]); t_std = float(z["t_std"])
    use_n_bounds = bool(z["use_n_bounds"]) if "use_n_bounds" in z else False
    n_min = float(z["n_min"]) if "n_min" in z else 0.25
    n_max = float(z["n_max"]) if "n_max" in z else 8.0

    # install to globals (Numba reads them)
    global _sr_params, _sr_sz_dx, _sr_sz_a, _sr_sz_n, _sr_sz_c
    global _sr_i0_dx, _sr_i0_a, _sr_i0_n, _sr_i0_c
    global _sr_link_dx, _sr_link_a, _sr_link_n, _sr_link_c
    global _sr_standardized, _sr_t_mean, _sr_t_std
    global _sr_use_n_bounds, _sr_n_min, _sr_n_max

    _sr_params = params.astype(np.float64)  # ensure dtype
    _sr_sz_dx, _sr_sz_a, _sr_sz_n, _sr_sz_c = sz_dx, sz_a, sz_n, sz_c
    _sr_i0_dx, _sr_i0_a, _sr_i0_n, _sr_i0_c = i0_dx, i0_a, i0_n, i0_c
    _sr_link_dx, _sr_link_a, _sr_link_n, _sr_link_c = link_dx, link_a, link_n, link_c
    _sr_standardized = 1 if standardized else 0
    _sr_t_mean, _sr_t_std = t_mean, t_std
    _sr_use_n_bounds = 1 if use_n_bounds else 0
    _sr_n_min, _sr_n_max = n_min, n_max

    # Trigger JIT once with a harmless call so later calls are fast
    _ = survival_rate(10.0, 100.0)  # warmup compile
    print(f"[sr-fit] Loaded survival model from '{fit_npz_path}' "
          f"(deg: dx/a/n/c = {deg_dx}/{deg_a}/{deg_n}/{deg_c}, "
          f"standardized={standardized}, links={link_dx,link_a,link_n,link_c})")


@njit(cache=True)
def N(ratio):
    ratio = np.log10(ratio)
    p7, p6, p5, p4, p3, p2, p1, p0 = 5.75878234, -23.15540197,  32.5761094,  -15.60652603, -11.64811135, 32.12022855, -34.78329596, 17.15939426
    y =  np.ceil((p7 * ratio**7 + p6 * ratio**6 + p5 * ratio**5 + p4 * ratio**4 + p3 * ratio**3 + p2 * ratio**2 + p1 * ratio + p0))

    if ratio < -1:
        y = 50.0

    if y < 2.0:
        y = 2.0

    return y


def loadparams(npz_path: str) -> dict:
    content = np.load(npz_path)
    params = {
        'mode': int(content['mode']),
        'coeffs': content['coeffs'],
        'powers': content['powers'],
        'log_z': bool(content['log_z']),
        'standardized': bool(content['standardized']),
        'xm': content['xm'],
        'xs': content['xs'],
        'ym': content.get('ym', None),
        'ys': content.get('ys', None),
    }
    return params


def predictor(params, molire_wrapper=False):
    mode = params['mode']
    coeffs = params['coeffs']
    powers = params['powers']
    xm = params['xm']
    xs = params['xs']
    ym = params.get('ym', None)
    ys = params.get('ys', None)
    standardized = params['standardized']
    log_z = params['log_z']

    @njit
    def predictor_1_nstd_lin(x):
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * x ** p[0]

        return z

    @njit
    def predictor_1_std_lin(x):
        x_std = (x - xm) / (xs or 1.0)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * x_std ** p[0]
        return z

    @njit
    def predictor_1_nstd_log(x):
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * x ** p[0]
        return np.exp(z)

    @njit
    def predictor_1_std_log(x):
        x_std = (x - xm) / (xs or 1.0)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * x_std ** p[0]
        return np.exp(z)

    @njit
    def predictor_2_nstd_lin(x, y):
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x ** p[0]) * (y ** p[1])
        return z

    @njit
    def predictor_2_std_lin(x, y):
        x_std = (x - xm) / (xs or 1.0)
        y_std = (y - ym) / (ys or 1.0)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x_std ** p[0]) * (y_std ** p[1])
        return z

    @njit
    def predictor_2_nstd_log(x, y):
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x ** p[0]) * (y ** p[1])
        return np.exp(z)

    @njit
    def predictor_2_std_log(x, y):
        x_std = (x - xm) / (xs or 1.0)
        y_std = (y - ym) / (ys or 1.0)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x_std ** p[0]) * (y_std ** p[1])
        return np.exp(z)

    @njit
    def predictor_2_nstd_lin_moliere(x, y):
        x = np.log(x / y)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x ** p[0]) * (y ** p[1])
        return z

    @njit
    def predictor_2_std_lin_moliere(x, y):
        x = np.log(x / y)
        x_std = (x - xm) / (xs or 1.0)
        y_std = (y - ym) / (ys or 1.0)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x_std ** p[0]) * (y_std ** p[1])
        return z

    @njit
    def predictor_2_nstd_log_moliere(x, y):
        x = np.log(x / y)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x ** p[0]) * (y ** p[1])
        return np.exp(z)

    @njit
    def predictor_2_std_log_moliere(x, y):
        x = np.log(x / y)
        x_std = (x - xm) / (xs or 1.0)
        y_std = (y - ym) / (ys or 1.0)
        z = np.zeros_like(x, dtype=np.float64)
        for p, c in zip(powers, coeffs):
            z += c * (x_std ** p[0]) * (y_std ** p[1])
        return np.exp(z)

    if mode == 1 and not standardized and not log_z:
        return predictor_1_nstd_lin
    elif mode == 1 and standardized and not log_z:
        return predictor_1_std_lin
    elif mode == 1 and not standardized and log_z:
        return predictor_1_nstd_log
    elif mode == 1 and standardized and log_z:
        return predictor_1_std_log
    elif mode == 2 and not standardized and not log_z:
        return predictor_2_nstd_lin if not molire_wrapper else predictor_2_nstd_lin_moliere
    elif mode == 2 and standardized and not log_z:
        return predictor_2_std_lin if not molire_wrapper else predictor_2_std_lin_moliere
    elif mode == 2 and not standardized and log_z:
        return predictor_2_nstd_log if not molire_wrapper else predictor_2_nstd_log_moliere
    elif mode == 2 and standardized and log_z:
        return predictor_2_std_log if not molire_wrapper else predictor_2_std_log_moliere
    else:
        raise ValueError("Invalid combination of mode, standardized, and log_z in parameters.")


def build_predictor(npz_path: str, molire_wrapper=False):
    params = loadparams(npz_path)
    return predictor(params, molire_wrapper)



# Directory this file lives in
_THIS_DIR = Path(__file__).resolve().parent
_DATA_DIR = _THIS_DIR / "predictors"

A_path     = _DATA_DIR / "Moliere_A_predictor.npz"
sigma_path = _DATA_DIR / "Moliere_sigma_predictor.npz"
f1_path    = _DATA_DIR / "Moliere_f1_predictor.npz"
f2_path    = _DATA_DIR / "Moliere_f2_predictor.npz"
s2_path    = _DATA_DIR / "Moliere_s2_predictor.npz"
s3_path    = _DATA_DIR / "Moliere_s3_predictor.npz"
n_path     = _DATA_DIR / "Moliere_n_predictor.npz"

SR_path    = _DATA_DIR / "poly_thickness_fit.npz"


A_predictor = build_predictor(A_path, molire_wrapper=True)
sigma_predictor = build_predictor(sigma_path, molire_wrapper=True)
f1_predictor = build_predictor(f1_path, molire_wrapper=False)
f2_predictor = build_predictor(f2_path, molire_wrapper=False)
s2_predictor = build_predictor(s2_path, molire_wrapper=True)
s3_predictor = build_predictor(s3_path, molire_wrapper=True)
n_predictor = build_predictor(n_path, molire_wrapper=True)

use_sr_fit(SR_path)
eps = 1e-9


@njit(cache=True, fastmath=True)
def gaussian(x, sigma):
    if sigma < eps:
        sigma = eps
    coeff = 1.0 / (sigma * np.sqrt(2.0 * np.pi))
    exponent = -0.5 * (x / sigma) ** 2
    return coeff * np.exp(exponent)


@njit(cache=True, fastmath=True)
def power_law(x, sigma, n):
    if sigma < eps:
        sigma = eps
    # simple bounded heavy tail; not strictly normalized in x∈[0,∞) without truncation,
    # but we keep the previous convention for shape control and scaling by A
    norm = (n - 1.0) / sigma
    value = 1.0 / (1.0 + (x / sigma) ** n)
    return norm * value


@njit(cache=True, fastmath=True)
def exponential(x, sigma):
    if sigma < eps:
        sigma = eps
    coeff = 1.0 / sigma
    exponent = -x / sigma
    return coeff * np.exp(exponent)


@njit(cache=True, fastmath=True, parallel=True)
def trapz(y, x):
    n = y.shape[0]
    s = np.zeros(n - 1, dtype=np.float64)

    for i in prange(n - 1):
        dx = x[i + 1] - x[i]
        s[i] = 0.5 * (y[i] + y[i + 1]) * dx

    return np.sum(s)


@njit(cache=True)
def moliere_pdf(x, A, sigma1, s2, s3, n, w1, w2):
    sigma2 = s2 * sigma1
    sigma3 = s3 * sigma1

    f1 = w1
    f2 = w2 * (1.0 - w1)
    f3 = (1.0 - w1) * (1.0 - w2)

    xabs = np.abs(x)  # robust to any negative angles
    s = np.sin(xabs)

    y1 = gaussian(xabs, sigma1)
    y2 = power_law(xabs, sigma2, n)
    y3 = exponential(xabs, sigma3)

    y = f1 * y1 + f2 * y2 + f3 * y3
    func_ = 2 * np.pi * s * y

    y = A * func_

    # ensure finite output
    out = np.empty_like(y)
    for i in range(y.size):
        v = y[i]
        if not np.isfinite(v):
            out[i] = 1e300
        else:
            out[i] = v
    return out


@njit(cache=True)
def moliere(E, T):
    A = A_predictor(E, T)
    sigma1 = sigma_predictor(E, T)
    f1 = f1_predictor(E, T)
    f2 = f2_predictor(E, T)
    s2 = s2_predictor(E, T)
    s3 = s3_predictor(E, T)
    n = n_predictor(E, T)

    return A, sigma1, s2, s3, n, f1, f2


@njit(cache=True)
def params(E, T):
    A, sigma1, s2, s3, n, f1, f2 = moliere(E, T)
    sr = survival_rate(E, T)
    return A, sigma1, s2, s3, n, f1, f2, sr

@njit(cache=True, parallel=True)
def params_array(E, T_array, THX, THY, IDX, IDY, PhiE, window_size):
    shape = T_array.shape
    T_array = T_array.flatten()
    THX = THX.flatten()
    THY = THY.flatten()
    IDX = IDX.flatten()
    IDY = IDY.flatten()
    PhiE = PhiE.flatten()
    n = T_array.shape[0]
    out = np.empty((n, 16), dtype=np.float32)
    for i in prange(n):
        T = T_array[i]
        sr = survival_rate(E, T)
        if sr == 0.0:
            out[i, 0] = 0.0
            out[i, 1] = 0.0
            out[i, 2] = 0.0
            out[i, 3] = 0.0
            out[i, 4] = 0.0
            out[i, 5] = 0.0
            out[i, 6] = 0.0
            out[i, 7] = 0.0
            out[i, 8] = THX[i]
            out[i, 9] = THY[i]
            out[i, 10] = IDX[i]
            out[i, 11] = IDY[i]
            out[i, 12] = i
            out[i, 13] = 0.0
            out[i, 14] = 0.0
            out[i, 15] = 0.0
            continue
        A, sigma1, s2, s3, n_, f1, f2 = moliere(E, T)
        out[i, 0] = A
        out[i, 1] = sigma1
        out[i, 2] = s2
        out[i, 3] = s3
        out[i, 4] = n_
        out[i, 5] = f1
        out[i, 6] = f2
        out[i, 7] = sr
        out[i, 8] = THX[i]
        out[i, 9] = THY[i]
        out[i, 10] = IDX[i]
        out[i, 11] = IDY[i]
        out[i, 12] = i
        out[i, 13] = PhiE[i]
        out[i, 14] = N(sigma1 / window_size)
        out[i, 15] = 0.0

    out = out.reshape((*shape, 16))
    return out
