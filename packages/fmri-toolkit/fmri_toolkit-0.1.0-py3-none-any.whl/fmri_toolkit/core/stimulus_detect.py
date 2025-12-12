import numpy as np
import sys
from ..simulate import fmri_simulate_func
import pandas as pd
from .stimulus_helper import (
    fmri_p_val,
    fmri_complex_p_val,
    fmri_on_off_volume,
    fmri_hrf_p_val,
)
from statsmodels.stats.multitest import multipletests

def _to_bool_mask(mask):
    if mask is None:
        return None
    m = np.asarray(mask)
    if m.dtype != bool:
        m = m != 0
    return m

def _sanitize_stimulus_idx(stimulus_idx, T):
    """Accept bool vector or integer indices (0- or 1-based). Return 0-based np.array."""
    if stimulus_idx is None:
        raise ValueError("stimulus_idx must be provided (R version also expects it unless HRF/gLRT with ons/dur).")
    stim = np.asarray(stimulus_idx)
    if stim.dtype == bool:
        if stim.size != T:
            raise ValueError("Boolean stimulus_idx must have length equal to time dimension.")
        return np.flatnonzero(stim)
    else:
        # integer indices: detect 1-based if min==1
        base = 1 if np.min(stim) == 1 else 0
        idx0 = stim.astype(int) - base
        if np.any((idx0 < 0) | (idx0 >= T)):
            raise ValueError("stimulus_idx out of bounds.")
        return idx0

def _ecdf_p_from_values(values, x):
    """
    Empirical CDF p-value like R:
    p = 1 - ecdf(volume)(value)
    """
    v = np.asarray(values, float)
    v = v[~np.isnan(v)]
    if v.size == 0:
        return 1.0
    # rank proportion <= x
    return 1.0 - (np.sum(v <= x) / float(v.size))

def _fdr_method_map(method):
    """
    Map R's p.adjust methods to statsmodels multipletests.
    Common R strings: 'BH','fdr','BY','bonferroni','holm','hochberg','hommel','sidak'
    """
    if method is None:
        return None
    m = method.lower()
    if m in ("bh", "fdr", "fdr_bh"):
        return "fdr_bh"
    if m in ("by", "fdr_by"):
        return "fdr_by"
    if m in ("bonferroni",):
        return "bonferroni"
    if m in ("holm",):
        return "holm"
    if m in ("hochberg",):
        return "simes-hochberg"  # closest available
    if m in ("hommel",):
        return "hommel"
    if m in ("sidak", "sidak_ss"):
        return "sidak"
    # default to BH if unknown
    return "fdr_bh"

def _cluster_threshold_like_R(x, level_thr, size_thr):
    """
    Emulate R's cluster.threshold over a 3D array:
      - threshold at level_thr on (1 - p) like in R code
      - label 6-connected clusters
      - zero out clusters with size < size_thr
      - return binary mask of kept clusters (1 else 0)
    """
    x = np.asarray(x, float)
    if x.ndim != 3:
        raise ValueError("cluster threshold expects a 3D array")

    # 6-connectivity structure (faces-only)
    structure = ndimage.generate_binary_structure(rank=3, connectivity=1)

    # threshold
    mask = (x >= level_thr)

    # label clusters
    labels, num = ndimage.label(mask, structure=structure)
    if num == 0:
        return np.zeros_like(x, dtype=float)

    # compute sizes
    sizes = np.bincount(labels.ravel())
    # sizes[0] is background, ignore
    keep = np.zeros_like(sizes, dtype=bool)
    keep_indices = np.where(sizes >= int(size_thr))[0]
    keep[keep_indices] = True
    keep[0] = False

    # build result: voxels in clusters of sufficient size -> 1
    res = keep[labels]
    return res.astype(float)

# -----------------------------
# Main function
# -----------------------------

def fmri_stimulus_detect(
    fmridata,
    mask=None,
    stimulus_idx=None,
    rest_idx=None,                 # R has 'rest_idex'; we accept rest_idx
    method=None,
    fdr_corr=None,
    spatial_cluster_thr=None,      # R: spatial_cluster.thr
    spatial_cluster_size=None,     # R: spatial_cluster.size
    ons=None,
    dur=None,
):
    """
    Python port aligned with the provided R function's behavior.
    Returns:
      - 3D array of p-values if input is 4D
      - vector of p-values if input is 2D/3D(time last)
      - scalar p-value if input is 1D
    """

    if fmridata is None:
        raise ValueError("fmridata must be provided.")

    arr = np.asarray(fmridata)
    ndim = arr.ndim

    # normalize mask
    mask_bool = _to_bool_mask(mask)
    # normalize method
    if method is None:
        raise ValueError("method must be specified.")

    # -------------- 1D case --------------
    if ndim == 1:
        y = arr
        if not np.iscomplexobj(y) and method in ("t-test", "wilcoxon-test"):
            p_val = fmri_p_val(fmridata=y, stimulus_idx=stimulus_idx, test_type=method)
            return 1.0 if p_val is None or np.isnan(p_val) else float(p_val)
        elif np.iscomplexobj(y) and method in ("HotellingsT2", "Wilks-Lambda", "gLRT"):
            try:
                _, p_val = fmri_complex_p_val(fmridata=y, stimulus_idx=stimulus_idx, method=method, ons=ons, dur=dur)
                return 1.0 if p_val is None or np.isnan(p_val) else float(p_val)
            except Exception:
                return 1.0
        else:
            if np.iscomplexobj(y):
                raise ValueError("Invalid test type for complex 1D data. Use 'HotellingsT2', 'Wilks-Lambda', or 'gLRT'.")
            raise ValueError("Invalid test type for real 1D data. Use 't-test' or 'wilcoxon-test'.")

    # -------------- 2D/3D (time last) -> treat as V x T --------------
    if ndim in (2, 3):
        T = arr.shape[-1]
        fmri_mat = arr.reshape(-1, T)
        p_list = []

        for i in range(fmri_mat.shape[0]):
            y = fmri_mat[i, :]
            if not np.iscomplexobj(y) and method in ("t-test", "wilcoxon-test"):
                p = fmri_p_val(fmridata=y, stimulus_idx=stimulus_idx, test_type=method)
                if p is None or np.isnan(p):
                    p = 1.0
            elif np.iscomplexobj(y) and method in ("HotellingsT2", "Wilks-Lambda", "gLRT"):
                try:
                    _, p = fmri_complex_p_val(fmridata=y, stimulus_idx=stimulus_idx, method=method, ons=ons, dur=dur)
                    if p is None or np.isnan(p):
                        p = 1.0
                except Exception:
                    p = 1.0
            else:
                if np.iscomplexobj(y):
                    raise ValueError("Invalid test type for complex data. Use 'HotellingsT2', 'Wilks-Lambda', or 'gLRT'.")
                raise ValueError("Invalid test type for real data. Use 't-test' or 'wilcoxon-test'.")
            p_list.append(p)

        p_vec = np.asarray(p_list, float).reshape(arr.shape[:-1])
        return p_vec

    # -------------- 4D case (X,Y,Z,T) --------------
    if ndim != 4:
        raise ValueError("fmridata must be 1D, 2D, 3D(time last), or 4D (X,Y,Z,T).")

    X, Y, Z, T = arr.shape
    p_val_3d = np.ones((X, Y, Z), dtype=float)

    # build on/off indices like R
    on_idx = _sanitize_stimulus_idx(stimulus_idx, T) if stimulus_idx is not None else None
    off_idx = np.setdiff1d(np.arange(T), on_idx) if on_idx is not None else None
    if rest_idx is not None:
        off_idx = np.asarray(rest_idx, int)

    # ---------- Real data paths ----------
    if not np.iscomplexobj(arr) and method in ("t-test", "wilcoxon-test", "on_off_diff", "HRF"):

        if method in ("t-test", "wilcoxon-test"):
            for x in range(X):
                for y in range(Y):
                    for z in range(Z):
                        if mask_bool is not None and not mask_bool[x, y, z]:
                            p_val_3d[x, y, z] = 1.0
                            continue
                        p = fmri_p_val(fmridata=arr[x, y, z, :], stimulus_idx=stimulus_idx, test_type=method)
                        if p is None or np.isnan(p):
                            p = 1.0
                        p_val_3d[x, y, z] = float(p)

        elif method == "on_off_diff":
            if mask_bool is None:
                raise ValueError("on_off_diff requires a mask in the R code. Provide mask.")
            # collect volumes for voxels inside mask
            vols = []
            idxs = []
            for i in range(X):
                for j in range(Y):
                    for k in range(Z):
                        if mask_bool[i, j, k]:
                            v = fmri_on_off_volume(arr, x=i, y=j, z=k)
                            idxs.append((i, j, k))
                            vols.append(v)
            vols = np.asarray(vols, float)
            # empirical p-values
            for (i, j, k), v in zip(idxs, vols):
                p = _ecdf_p_from_values(vols, v)
                p_val_3d[i, j, k] = float(p)

        elif method == "HRF":
            if mask_bool is None:
                raise ValueError("HRF path in R typically expects a mask. Provide mask.")
            # delegate to helper
            try:
                pmap = fmri_hrf_p_val(arr, mask=mask_bool, ons=ons, dur=dur)
            except TypeError:
                pmap = fmri_hrf_p_val(arr, mask_bool, ons, dur)
            pmap = np.asarray(pmap, float)
            if pmap.shape != (X, Y, Z):
                raise ValueError("fmri_hrf_p_val returned unexpected shape. Expected (X,Y,Z).")
            p_val_3d = pmap

        else:
            raise ValueError("Invalid test type for real data. Use 't-test', 'wilcoxon-test', 'on_off_diff', or 'HRF'.")

    # ---------- Complex data paths ----------
    elif np.iscomplexobj(arr) and method in ("HotellingsT2", "Wilks-Lambda", "gLRT"):
        for i in range(X):
            for j in range(Y):
                for k in range(Z):
                    if mask_bool is not None and not mask_bool[i, j, k]:
                        p_val_3d[i, j, k] = 1.0
                        continue
                    try:
                        _, p = fmri_complex_p_val(arr[i, j, k, :], stimulus_idx=stimulus_idx, method=method, ons=ons, dur=dur)
                        if p is None or np.isnan(p):
                            p = 1.0
                    except Exception:
                        p = 1.0
                    p_val_3d[i, j, k] = float(p)
    else:
        if np.iscomplexobj(arr):
            raise ValueError("Invalid test type for complex data. Use 'HotellingsT2', 'Wilks-Lambda', or 'gLRT'.")
        raise ValueError("Invalid test type for real data. Use 't-test', 'wilcoxon-test', 'on_off_diff', or 'HRF'.")

    # ---------------- Post-hoc processing ----------------

    # FDR correction (optional) — mirrors R's p.adjust
    if fdr_corr is not None:
        method_sm = _fdr_method_map(fdr_corr)
        flat = p_val_3d.ravel()
        # statsmodels returns corrected p-values in position 1
        _, p_corr, _, _ = multipletests(flat, method=method_sm)
        p_val_3d = p_corr.reshape((X, Y, Z))

    # Spatial clustering (optional)
    if (spatial_cluster_size is not None) and (spatial_cluster_thr is not None):
        # R code: spatial_cluster.filter = cluster.threshold(1 - p, level.thr=thr, size.thr=size)
        # then: p' = 1 - ((1 - p) * filter)
        one_minus_p = 1.0 - p_val_3d
        filt = _cluster_threshold_like_R(one_minus_p, level_thr=float(spatial_cluster_thr), size_thr=int(spatial_cluster_size))
        p_val_3d = 1.0 - ((1.0 - p_val_3d) * filt)

    # Clean NaNs/inf
    p_val_3d = np.nan_to_num(p_val_3d, nan=1.0, posinf=1.0, neginf=1.0)
    return p_val_3d