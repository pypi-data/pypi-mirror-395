import time
import threading
from typing import Optional, List, Tuple

import numpy as np
import matplotlib.pyplot as plt  # kept for potential debug/visualization
from numba import cuda
import cv2

# NEW: progress bar
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    tqdm = None
    HAS_TQDM = False

from .constructor import params_array
from ..utils.coordinates import det2zenith
from .flux_model import differential_flux
from .gpu import splat_kernels, splat_kernels_track
from .constants import sigma_window_ratio_lower, sigma_window_ratio_middle,  sigma_window_ratio_upper
from ..profiler import Profiler, print_profile


# ---------------------------------------------------------------------
# Host-side helpers (including progress bar wrapper)
# ---------------------------------------------------------------------

def _run_kernel_with_progress(
    desc: str,
    g_idx: int,
    kernel,
    params: np.ndarray,
    img: np.ndarray,
    threads_per_block: int,
    extra_args=(),
    blocks_per_launch: int = 256,
):
    """
    Run a CUDA kernel over `params` in chunks, updating a tqdm progress bar.

    - desc: label for tqdm (e.g. "splat1")
    - g_idx: GPU index (for positioning multiple bars)
    - kernel: the numba.cuda kernel
    - params: (N, P) float32 array (host)
    - img: (H, W) float32 array (host accumulator)
    - extra_args: extra kernel args after (PARAMS, OUTPUT, ...)
    - blocks_per_launch: how many PARAMS rows per kernel launch
    """
    n_jobs = params.shape[0]
    if n_jobs == 0:
        return

    params = np.ascontiguousarray(params)
    img_dev = cuda.to_device(img)

    # If tqdm is unavailable, just run in one shot
    if not HAS_TQDM:
        params_dev = cuda.to_device(params)
        blocks_per_grid = n_jobs
        kernel[blocks_per_grid, threads_per_block](params_dev, img_dev, *extra_args)
        cuda.synchronize()
        img_dev.copy_to_host(img)
        return

    # Chunked launches with progress bar
    with tqdm(
        total=n_jobs,
        desc=f"GPU {g_idx} {desc}",
        position=g_idx,
        leave=True,
        unit="job",
    ) as pbar:
        start = 0
        while start < n_jobs:
            end = min(start + blocks_per_launch, n_jobs)
            params_chunk = cuda.to_device(params[start:end])
            blocks_per_grid = end - start

            kernel[blocks_per_grid, threads_per_block](params_chunk, img_dev, *extra_args)
            cuda.synchronize()

            done = end - start
            pbar.update(done)

            start = end
            del params_chunk

    img_dev.copy_to_host(img)


def params_array_wrapper(energy, L, THX, THY, PhiE, window_size, flatten=True):
    idx = np.arange(THX.shape[0])
    idy = np.arange(THY.shape[1])
    IDX, IDY = np.meshgrid(idx, idy, indexing="ij")
    params = params_array(energy, L, THX, THY, IDX, IDY, PhiE, window_size)
    if flatten:
        params = params.reshape(-1, params.shape[-1])
    return params


def crop_indices(THX, THY, angle):
    """
    Compute cropping indices for a symmetric FOV around (0,0) given crop_angle [deg].
    Shared logic so RESULT and TRACK use identical FOV.
    """
    mrad = int(np.round(np.radians(angle) * 1000))

    thx = THX[:, 0]
    thy = THY[0, :]

    idx_min = np.argmin(np.abs(thx + mrad * 0.001))
    idx_max = np.argmin(np.abs(thx - mrad * 0.001))
    idy_min = np.argmin(np.abs(thy + mrad * 0.001))
    idy_max = np.argmin(np.abs(thy - mrad * 0.001))

    if idx_min > idx_max:
        idx_min, idx_max = idx_max, idx_min
    if idy_min > idy_max:
        idy_min, idy_max = idy_max, idy_min

    return idx_min, idx_max, idy_min, idy_max


def crop(THX, THY, OUTPUT, angle):
    """
    Original crop helper, kept for the non-tracking calculate().
    """
    idx_min, idx_max, idy_min, idy_max = crop_indices(THX, THY, angle)

    THX_ = THX[idx_min:idx_max + 1, idy_min:idy_max + 1]
    THY_ = THY[idx_min:idx_max + 1, idy_min:idy_max + 1]
    OUTPUT_ = OUTPUT[idx_min:idx_max + 1, idy_min:idy_max + 1]
    return THX_, THY_, OUTPUT_


def split_params_strided(params: np.ndarray, n_parts: int) -> List[np.ndarray]:
    """
    Split a (N, P) params array into n_parts strided chunks:
        part0 = params[0::n_parts]
        part1 = params[1::n_parts]
        ...
    Each chunk is made C-contiguous so numba.cuda.to_device() accepts it.
    """
    if n_parts <= 0:
        raise ValueError("n_parts must be >= 1")
    return [np.ascontiguousarray(params[i::n_parts]) for i in range(n_parts)]


def split_branches_for_gpus(
    params0: np.ndarray,
    params1: np.ndarray,
    params2: np.ndarray,
    params3: np.ndarray,
    n_gpus: int,
) -> List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    """
    For each GPU, return its 4 param chunks:
        gpu_parts[g] = (params0_g, params1_g, params2_g, params3_g)

    Splitting is strided: params_k[g] = params_k[g::n_gpus].
    """
    chunks0 = split_params_strided(params0, n_gpus)
    chunks1 = split_params_strided(params1, n_gpus)
    chunks2 = split_params_strided(params2, n_gpus)
    chunks3 = split_params_strided(params3, n_gpus)

    gpu_parts: List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = []
    for g in range(n_gpus):
        gpu_parts.append((chunks0[g], chunks1[g], chunks2[g], chunks3[g]))
    return gpu_parts


# ---------------------------------------------------------------------
# GPU worker (runs in a separate thread per GPU) - non-tracking version
# ---------------------------------------------------------------------

def _gpu_worker(
    g_idx: int,
    dev,
    p0_g: np.ndarray,
    p1_g: np.ndarray,
    p2_g: np.ndarray,
    p3_g: np.ndarray,
    partial0: List[np.ndarray],
    partial1: List[np.ndarray],
    partial2: List[np.ndarray],
    partial3: List[np.ndarray],
    splat1_kernel,
    splat2_kernel,
    splat3_kernel,
    gpu_prof: Profiler,
):
    """
    Worker for the standard calculate() (no TRACK array).
    """
    
    # Safety: make sure chunks are contiguous (should already be, but belt & suspenders)
    p0_g = np.ascontiguousarray(p0_g)
    p1_g = np.ascontiguousarray(p1_g)
    p2_g = np.ascontiguousarray(p2_g)
    p3_g = np.ascontiguousarray(p3_g)
    
    p0_g = np.astype(p0_g, np.float32)
    p1_g = np.astype(p1_g, np.float32)
    p2_g = np.astype(p2_g, np.float32)
    p3_g = np.astype(p3_g, np.float32)
    
    with dev:
        # Branch 0: direct accumulate (CPU on this chunk)
        with gpu_prof.section("splat:direct_accumulate"):
            if p0_g.shape[0] > 0:
                img0 = partial0[g_idx]
                for p in p0_g:
                    (
                        _A, _sigma, _s2, _s3, _n, _f1, _f2, sr,
                        thx, thy, idx, idy, _window, PhiE, _dummy1, _dummy2
                    ) = p
                    img0[int(idx), int(idy)] += PhiE * sr

        # Branch 1: GPU splat1_kernel on this GPU & chunk (with progress bar)
        with gpu_prof.section("splat:kernel1"):
            if p1_g.shape[0] > 0:
                img1 = partial1[g_idx]
                _run_kernel_with_progress(
                    desc="splat1",
                    g_idx=g_idx,
                    kernel=splat1_kernel,
                    params=p1_g,
                    img=img1,
                    threads_per_block=32,
                )

        # Branch 2: GPU splat2_kernel on this GPU & chunk (with progress bar)
        with gpu_prof.section("splat:kernel2"):
            if p2_g.shape[0] > 0:
                img2 = partial2[g_idx]
                _run_kernel_with_progress(
                    desc="splat2",
                    g_idx=g_idx,
                    kernel=splat2_kernel,
                    params=p2_g,
                    img=img2,
                    threads_per_block=32,
                )

        # Branch 3: GPU splat3_kernel on this GPU & chunk (with progress bar)
        with gpu_prof.section("splat:kernel3"):
            if p3_g.shape[0] > 0:
                img3 = partial3[g_idx]
                _run_kernel_with_progress(
                    desc="splat3",
                    g_idx=g_idx,
                    kernel=splat3_kernel,
                    params=p3_g,
                    img=img3,
                    threads_per_block=256,
                )


# ---------------------------------------------------------------------
# GPU worker (runs in a separate thread per GPU) - tracking version
# ---------------------------------------------------------------------

def _gpu_worker_track(
    g_idx: int,
    dev,
    p0_g: np.ndarray,
    p1_g: np.ndarray,
    p2_g: np.ndarray,
    p3_g: np.ndarray,
    partial0: List[np.ndarray],
    partial1: List[np.ndarray],
    partial2: List[np.ndarray],
    partial3: List[np.ndarray],
    partial_track: List[np.ndarray],
    splat1_kernel,
    splat2_kernel,
    splat3_kernel,
    gpu_prof: Profiler,
):
    """
    Worker for calculate_and_track().

    Uses TRACK[src_idx, src_idy, dst_idx, dst_idy] to accumulate source→destination flux,
    including:
    - direct accumulate branch (CPU)
    - three GPU branches via splat*_kernel_track
    """

    # Safety: make sure chunks are contiguous (should already be, but belt & suspenders)
    p0_g = np.ascontiguousarray(p0_g)
    p1_g = np.ascontiguousarray(p1_g)
    p2_g = np.ascontiguousarray(p2_g)
    p3_g = np.ascontiguousarray(p3_g)
    
    p0_g = np.astype(p0_g, np.float32)
    p1_g = np.astype(p1_g, np.float32)
    p2_g = np.astype(p2_g, np.float32)
    p3_g = np.astype(p3_g, np.float32)
    with dev:
        img0 = partial0[g_idx]
        img1 = partial1[g_idx]
        img2 = partial2[g_idx]
        img3 = partial3[g_idx]
        track_host = partial_track[g_idx]

        # ----------------------------------------------------
        # Branch 0: direct accumulate (CPU on this chunk),
        #           also track flux as src_idx->idx, src_idy->idy.
        # ----------------------------------------------------
        with gpu_prof.section("splat:direct_accumulate"):
            if p0_g.shape[0] > 0:
                for p in p0_g:
                    (
                        _A, _sigma, _s2, _s3, _n, _f1, _f2, sr,
                        thx, thy, idx, idy, _window, PhiE, _dummy1, _dummy2
                    ) = p
                    ii = int(idx)
                    jj = int(idy)
                    img0[ii, jj] += PhiE * sr
                    # track direct contribution: source pixel == destination pixel
                    track_host[ii, jj, ii, jj] += PhiE * sr

        # Upload TRACK after CPU updates so GPU sees them
        track_device = cuda.to_device(track_host)

        # ----------------------------------------------------
        # Branch 1: GPU splat1_kernel on this GPU & chunk
        # ----------------------------------------------------
        with gpu_prof.section("splat:kernel1"):
            if p1_g.shape[0] > 0:
                _run_kernel_with_progress(
                    desc="splat1[track]",
                    g_idx=g_idx,
                    kernel=splat1_kernel,
                    params=p1_g,
                    img=img1,
                    threads_per_block=32,
                    extra_args=(track_device,),
                )

        # ----------------------------------------------------
        # Branch 2: GPU splat2_kernel on this GPU & chunk
        # ----------------------------------------------------
        with gpu_prof.section("splat:kernel2"):
            if p2_g.shape[0] > 0:
                _run_kernel_with_progress(
                    desc="splat2[track]",
                    g_idx=g_idx,
                    kernel=splat2_kernel,
                    params=p2_g,
                    img=img2,
                    threads_per_block=32,
                    extra_args=(track_device,),
                )

        # ----------------------------------------------------
        # Branch 3: GPU splat3_kernel on this GPU & chunk
        # ----------------------------------------------------
        with gpu_prof.section("splat:kernel3"):
            if p3_g.shape[0] > 0:
                _run_kernel_with_progress(
                    desc="splat3[track]",
                    g_idx=g_idx,
                    kernel=splat3_kernel,
                    params=p3_g,
                    img=img3,
                    threads_per_block=256,
                    extra_args=(track_device,),
                )

        # Finally, bring TRACK back to host
        track_device.copy_to_host(track_host)


# ---------------------------------------------------------------------
# Main calculation (multi-GPU capable, with profiling)
# ---------------------------------------------------------------------

def calculate(
    path,
    density_map,
    crop_angle,
    E_min,
    E_max,
    E_N,
    E_scale,
    window_size=20.0,
    bins=128,
    *,
    profiler: Optional[Profiler] = None,
    profile: bool = False,
    max_gpus: Optional[int] = None,  # optional limit on number of GPUs
):
    """
    Standard simulation (no TRACK), multi-GPU, with profiling.
    Returns cropped THX/THY/RESULT and the (possibly padded) density_map.
    """
    wall_t0 = time.perf_counter()
    prof = profiler if profiler is not None else Profiler()
    gpu_profs: List[Profiler] = []  # per-GPU profilers (filled later if GPUs exist)

    # ---------------- I/O: load NPZ & metadata ----------------
    with prof.section("io:load_npz"):
        data = np.load(path, allow_pickle=True)
        meta = data["meta"].item()
        THX = data["THX_rad"]
        THY = data["THY_rad"]
        THX_mrad = data["THX_mrad"]
        THY_mrad = data["THY_mrad"]

    # ---------------- Setup: pixel size & kernels ----------------
    with prof.section("setup:kernels"):
        x_ = THX[:, 0]
        y_ = THX[0, :]

        dx_ = np.abs(x_[1] - x_[0])
        dy_ = np.abs(y_[1] - y_[0])

        pixel_size = np.max([dx_, dy_])  # in rad

        print(f"Pixel size: {pixel_size * 1000:.3f} mrad")
        splat1_kernel, splat2_kernel, splat3_kernel = splat_kernels(
            pixel_size, window_size, bins
        )

    # ---------------- Density map prepare / pad ----------------
    with prof.section("density:prepare"):
        if density_map is None:
            density_map = np.ones_like(THX, dtype=np.float32) * 2.65
        else:
            THX_cropped, THY_cropped, _ = crop(THX, THY, np.zeros_like(THX), crop_angle)

            density_map = cv2.resize(
                density_map,
                (THX_cropped.shape[1], THX_cropped.shape[0]),
                interpolation=cv2.INTER_AREA,
            )

            pad_y = THX.shape[0] - density_map.shape[0]
            pad_x = THX.shape[1] - density_map.shape[1]

            pad_width = (
                (pad_y // 2, pad_y - pad_y // 2),
                (pad_x // 2, pad_x - pad_x // 2),
            )

            density_map = np.pad(density_map, pad_width, mode="edge")

    # ---------------- Thickness scaling & zenith angles ----------------
    with prof.section("thickness:scale_and_zenith"):
        L = data["L"] / 2.65 * density_map
        L = np.clip(L, 1, 3500)  # limit max thickness to 1000 m
        zenith = det2zenith(
            THX_mrad,
            -THY_mrad,
            np.radians(meta["angle_deg"]),
            0,
        )
    
        L /= 2
    # ---------------- Allocate result buffers (final accumulators) ----------------
    with prof.section("setup:result_buffers"):
        RESULT0 = np.zeros(THX.shape, dtype=np.float32)
        RESULT1 = np.zeros(THX.shape, dtype=np.float32)
        RESULT2 = np.zeros(THX.shape, dtype=np.float32)
        RESULT3 = np.zeros(THX.shape, dtype=np.float32)

    # ---------------- Energy grid & parameter building ----------------
    with prof.section("loop:build_all_params"):
        if E_scale == "linear":
            energies = np.linspace(E_min, E_max, E_N)  # GeV
        elif E_scale == "log":
            energies = np.logspace(np.log10(E_min), np.log10(E_max), E_N)  # GeV
        else:
            raise ValueError(f"Invalid E_scale: {E_scale}")

        dE = energies[1:] - energies[:-1]
        energies_mid = 0.5 * (energies[1:] + energies[:-1])
        
        params = None
        for i, energy in enumerate(energies_mid):
            PhiE = differential_flux(zenith, energy) * dE[i]

            params_ = params_array_wrapper(
                energy, L, THX, THY, PhiE, pixel_size, flatten=True
            )
            # filter out samples with non-positive sr
            params_ = params_[params_[:, 7] > 0]

            if params_ is None or params_.size == 0:
                continue

            if params is None:
                params = params_
            else:
                params = np.concatenate((params, params_), axis=0)
    
    
    
    if params is None or params.shape[0] == 0:
        # No contributions at all
        if profile:
            print_profile("simulate() main", prof)
            wall_t1 = time.perf_counter()
            print(f"[simulate()] wall time = {wall_t1 - wall_t0:.3f} s")
        return THX, THY, np.zeros_like(THX, dtype=np.float32), density_map

    # ---------------- Sort & split params by sigma-scale ----------------
    with prof.section("params:sort_and_split"):
        argsort = np.argsort(params[:, 1])
        params = params[argsort]
        sigma_ps = params[:, 1] / pixel_size
        

        mask0 = sigma_ps < sigma_window_ratio_lower
        mask1 = (sigma_ps > sigma_window_ratio_lower) & (sigma_ps < sigma_window_ratio_middle) 
        mask2 = (sigma_ps >= sigma_window_ratio_middle) & (sigma_ps < sigma_window_ratio_upper)
        mask3 = sigma_ps >= sigma_window_ratio_upper
        

        params0 = params[mask0]
        params1 = params[mask1]
        params2 = params[mask2]
        params3 = params[mask3]
    
    # ---------------- Multi-GPU setup ----------------
    with prof.section("gpu:setup_devices"):
        all_gpus = list(cuda.gpus)
        if max_gpus is not None:
            all_gpus = all_gpus[:max_gpus]
        n_gpus = len(all_gpus)

        if n_gpus == 0:
            raise RuntimeError("No CUDA GPUs available.")

        # Split each branch's params into strided chunks per GPU
        gpu_parts = split_branches_for_gpus(params0, params1, params2, params3, n_gpus)

        # Per-GPU partial images
        partial0 = [np.zeros_like(RESULT0) for _ in range(n_gpus)]
        partial1 = [np.zeros_like(RESULT1) for _ in range(n_gpus)]
        partial2 = [np.zeros_like(RESULT2) for _ in range(n_gpus)]
        partial3 = [np.zeros_like(RESULT3) for _ in range(n_gpus)]

        # Per-GPU profilers
        gpu_profs = [Profiler() for _ in range(n_gpus)]

    # ---------------- Per-GPU processing (parallel via threads) ----------------
    with prof.section("gpu:launch_threads"):
        threads: List[threading.Thread] = []

        for g_idx, dev in enumerate(all_gpus):
            p0_g, p1_g, p2_g, p3_g = gpu_parts[g_idx]
            gpu_prof = gpu_profs[g_idx]

            t = threading.Thread(
                target=_gpu_worker,
                args=(
                    g_idx,
                    dev,
                    p0_g, p1_g, p2_g, p3_g,
                    partial0, partial1, partial2, partial3,
                    splat1_kernel, splat2_kernel, splat3_kernel,
                    gpu_prof,
                ),
                daemon=False,
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    # ---------------- Reduce partial results (sum over GPUs) ----------------
    with prof.section("post:reduce_partial_results"):
        RESULT0 = sum(partial0)
        RESULT1 = sum(partial1)
        RESULT2 = sum(partial2)
        RESULT3 = sum(partial3)

    # ---------------- Crop & combine ----------------
    with prof.section("post:crop_and_combine"):
        _, _, RESULT0_c = crop(THX, THY, RESULT0, crop_angle)
        _, _, RESULT1_c = crop(THX, THY, RESULT1, crop_angle)
        _, _, RESULT2_c = crop(THX, THY, RESULT2, crop_angle)
        THX_c, THY_c, RESULT3_c = crop(THX, THY, RESULT3, crop_angle)

        RESULT = RESULT0_c + RESULT1_c + RESULT2_c + RESULT3_c

    # ---------------- Profiling output ----------------
    if profile:
        print_profile("simulate() main", prof)
        for g_idx, gp in enumerate(gpu_profs):
            if gp.total() > 0:
                print_profile(f"simulate() gpu{g_idx}", gp)
        wall_t1 = time.perf_counter()
        print(f"[simulate()] wall time = {wall_t1 - wall_t0:.3f} s")

    return THX_c, THY_c, RESULT, L


# ---------------------------------------------------------------------
# Tracking version: calculate_and_track (returns cropped TRACK)
# ---------------------------------------------------------------------

def calculate_and_track(
    path,
    density_map,
    crop_angle,
    E_min,
    E_max,
    E_N,
    E_scale,
    window_size=20.0,
    bins=128,
    *,
    profiler: Optional[Profiler] = None,
    profile: bool = False,
    max_gpus: Optional[int] = None,  # optional limit on number of GPUs
):
    """
    Same as calculate(), but also keeps a 4D TRACK tensor:

        TRACK[src_i, src_j, dst_i, dst_j]  = flux from source pixel (i,j) to dst (i,j)

    It returns **cropped FOV** versions:
        THX_c, THY_c, RESULT_c, density_map, TRACK_c

    where TRACK_c is cropped in both source and destination indices
    according to crop_angle.
    """
    wall_t0 = time.perf_counter()
    prof = profiler if profiler is not None else Profiler()
    gpu_profs: List[Profiler] = []  # per-GPU profilers (filled later if GPUs exist)

    # ---------------- I/O: load NPZ & metadata ----------------
    with prof.section("io:load_npz"):
        data = np.load(path, allow_pickle=True)
        meta = data["meta"].item()
        THX = data["THX_rad"]
        THY = data["THY_rad"]
        THX_mrad = data["THX_mrad"]
        THY_mrad = data["THY_mrad"]

    # ---------------- Setup: pixel size & kernels ----------------
    with prof.section("setup:kernels"):
        x_ = THX[:, 0]
        y_ = THX[0, :]

        dx_ = np.abs(x_[1] - x_[0])
        dy_ = np.abs(y_[1] - y_[0])

        pixel_size = np.max([dx_, dy_])  # in rad

        print(f"Pixel size: {pixel_size * 1000:.3f} mrad")
        splat1_kernel, splat2_kernel, splat3_kernel = splat_kernels_track(
            pixel_size, window_size, bins
        )

    # ---------------- Density map prepare / pad ----------------
    with prof.section("density:prepare"):
        if density_map is None:
            density_map = np.ones_like(THX, dtype=np.float32) * 2.65
        else:
            THX_cropped, THY_cropped, _ = crop(THX, THY, np.zeros_like(THX), crop_angle)

            density_map = cv2.resize(
                density_map,
                (THX_cropped.shape[1], THX_cropped.shape[0]),
                interpolation=cv2.INTER_AREA,
            )

            pad_y = THX.shape[0] - density_map.shape[0]
            pad_x = THX.shape[1] - density_map.shape[1]

            pad_width = (
                (pad_y // 2, pad_y - pad_y // 2),
                (pad_x // 2, pad_x - pad_x // 2),
            )

            density_map = np.pad(density_map, pad_width, mode="edge")

    # ---------------- Thickness scaling & zenith angles ----------------
    with prof.section("thickness:scale_and_zenith"):
        L = data["L"] / 2.65 * density_map
        L = np.clip(L, 1, 3500)  # limit max thickness to 1000 m
        zenith = det2zenith(
            THX_mrad,
            -THY_mrad,
            np.radians(meta["angle_deg"]),
            0,
        )

    # ---------------- Allocate result buffers (final accumulators) ----------------
    with prof.section("setup:result_buffers"):
        H, W = THX.shape
        RESULT0 = np.zeros((H, W), dtype=np.float32)
        RESULT1 = np.zeros((H, W), dtype=np.float32)
        RESULT2 = np.zeros((H, W), dtype=np.float32)
        RESULT3 = np.zeros((H, W), dtype=np.float32)

        # Full-FOV TRACK tensor (cropped later)
        TRACK = np.zeros((H, W, H, W), dtype=np.float32)
        print(f"TRACK size (full FOV): {TRACK.nbytes / (1024**3):.3f} GB")

    # ---------------- Energy grid & parameter building ----------------
    with prof.section("loop:build_all_params"):
        if E_scale == "linear":
            energies = np.linspace(E_min, E_max, E_N)  # GeV
        elif E_scale == "log":
            energies = np.logspace(np.log10(E_min), np.log10(E_max), E_N)  # GeV
        else:
            raise ValueError(f"Invalid E_scale: {E_scale}")

        dE = energies[1:] - energies[:-1]
        energies_mid = 0.5 * (energies[1:] + energies[:-1])

        params = None
        for i, energy in enumerate(energies_mid):
            PhiE = differential_flux(zenith, energy) * dE[i]

            params_ = params_array_wrapper(
                energy, L, THX, THY, PhiE, pixel_size, flatten=True
            )
            # filter out samples with non-positive sr
            params_ = params_[params_[:, 7] > 0]

            if params_ is None or params_.size == 0:
                continue

            if params is None:
                params = params_
            else:
                params = np.concatenate((params, params_), axis=0)

    if params is None or params.shape[0] == 0:
        # No contributions at all
        if profile:
            print_profile("simulate() main (track)", prof)
            wall_t1 = time.perf_counter()
            print(f"[simulate_and_track()] wall time = {wall_t1 - wall_t0:.3f} s")
        return THX, THY, np.zeros_like(THX, dtype=np.float32), density_map, np.zeros((0, 0, 0, 0), dtype=np.float32)

    # ---------------- Sort & split params by sigma-scale ----------------
    with prof.section("params:sort_and_split"):
        argsort = np.argsort(params[:, 1])
        params = params[argsort]
        sigma_ps = params[:, 1] / pixel_size

        mask0 = sigma_ps < sigma_window_ratio_lower
        mask1 = (sigma_ps > sigma_window_ratio_lower) & (sigma_ps < sigma_window_ratio_middle)
        mask2 = (sigma_ps >= sigma_window_ratio_middle) & (sigma_ps < sigma_window_ratio_upper)
        mask3 = sigma_ps >= sigma_window_ratio_upper

        params0 = params[mask0]
        params1 = params[mask1]
        params2 = params[mask2]
        params3 = params[mask3]

    # ---------------- Multi-GPU setup ----------------
    with prof.section("gpu:setup_devices"):
        all_gpus = list(cuda.gpus)
        if max_gpus is not None:
            all_gpus = all_gpus[:max_gpus]
        n_gpus = len(all_gpus)

        if n_gpus == 0:
            raise RuntimeError("No CUDA GPUs available.")

        # Split each branch's params into strided chunks per GPU
        gpu_parts = split_branches_for_gpus(params0, params1, params2, params3, n_gpus)

        # Per-GPU partial images + track
        partial0 = [np.zeros_like(RESULT0) for _ in range(n_gpus)]
        partial1 = [np.zeros_like(RESULT1) for _ in range(n_gpus)]
        partial2 = [np.zeros_like(RESULT2) for _ in range(n_gpus)]
        partial3 = [np.zeros_like(RESULT3) for _ in range(n_gpus)]
        partial_track = [np.zeros_like(TRACK) for _ in range(n_gpus)]

        # Per-GPU profilers
        gpu_profs = [Profiler() for _ in range(n_gpus)]

    # ---------------- Per-GPU processing (parallel via threads) ----------------
    with prof.section("gpu:launch_threads"):
        threads: List[threading.Thread] = []

        for g_idx, dev in enumerate(all_gpus):
            p0_g, p1_g, p2_g, p3_g = gpu_parts[g_idx]
            gpu_prof = gpu_profs[g_idx]

            t = threading.Thread(
                target=_gpu_worker_track,
                args=(
                    g_idx,
                    dev,
                    p0_g, p1_g, p2_g, p3_g,
                    partial0, partial1, partial2, partial3,
                    partial_track,
                    splat1_kernel, splat2_kernel, splat3_kernel,
                    gpu_prof,
                ),
                daemon=False,
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    # ---------------- Reduce partial results (sum over GPUs) ----------------
    with prof.section("post:reduce_partial_results"):
        RESULT0 = sum(partial0)
        RESULT1 = sum(partial1)
        RESULT2 = sum(partial2)
        RESULT3 = sum(partial3)
        TRACK = sum(partial_track)

    # ---------------- Crop & combine (RESULT and TRACK) ----------------
    with prof.section("post:crop_and_combine"):
        # Get consistent indices for FOV
        idx_min, idx_max, idy_min, idy_max = crop_indices(THX, THY, crop_angle)

        THX_c = THX[idx_min:idx_max + 1, idy_min:idy_max + 1]
        THY_c = THY[idx_min:idx_max + 1, idy_min:idy_max + 1]

        RESULT0_c = RESULT0[idx_min:idx_max + 1, idy_min:idy_max + 1]
        RESULT1_c = RESULT1[idx_min:idx_max + 1, idy_min:idy_max + 1]
        RESULT2_c = RESULT2[idx_min:idx_max + 1, idy_min:idy_max + 1]
        RESULT3_c = RESULT3[idx_min:idx_max + 1, idy_min:idy_max + 1]

        RESULT_c = RESULT0_c + RESULT1_c + RESULT2_c + RESULT3_c

        TRACK_SUM_CHECK = np.sum(TRACK, axis=(0, 1))[idx_min:idx_max + 1, idy_min:idy_max + 1]
        # Crop TRACK in both source and destination indices
        TRACK_c = TRACK[
            idx_min:idx_max + 1,
            idy_min:idy_max + 1,
            idx_min:idx_max + 1,
            idy_min:idy_max + 1,
        ]

    # ---------------- Profiling output ----------------
    if profile:
        print_profile("simulate() main (track)", prof)
        for g_idx, gp in enumerate(gpu_profs):
            if gp.total() > 0:
                print_profile(f"simulate() gpu{g_idx} (track)", gp)
        wall_t1 = time.perf_counter()
        print(f"[simulate_and_track()] wall time = {wall_t1 - wall_t0:.3f} s")

    TRACK_c = TRACK_c.astype(np.float32)
    TRACK_SUM_CHECK = TRACK_SUM_CHECK.astype(np.float32)
    # NOTE: we return TRACK_c (cropped FOV), not the full TRACK
    return THX_c, THY_c, RESULT_c, density_map, TRACK_c, TRACK_SUM_CHECK, TRACK
