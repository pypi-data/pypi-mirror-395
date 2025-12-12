import math
import random
import numpy as np
import pandas as pd

# OPTIONAL: only import if you actually use Hotelling or MANOVA
try:
    from hotelling.stats import hotelling_t2
except Exception:
    hotelling_t2 = None

try:
    from statsmodels.multivariate.manova import MANOVA
except Exception:
    MANOVA = None

from scipy.stats import ttest_ind, wilcoxon, laplace
import statsmodels.api as sm  # use sm.OLS
from ..simulate import fmri_simulate_func


# ---------------------------
# Helpers for stimulus / HRF
# ---------------------------

def _boxcar_from_ons_dur(T, ons, dur):
    """Build a 0/1 boxcar of length T from 1-based ons/dur."""
    s = np.zeros(T, dtype=float)
    if ons is not None and dur is not None:
        for o, d in zip(ons, dur):
            o0 = max(0, int(o) - 1)  # R->Python
            s[o0:o0 + int(d)] = 1.0
    return s

def _default_onoff(T, on=10, off=10):
    """Default 10-on / 10-off pattern repeated to fill T (boolean)."""
    pattern = np.r_[np.ones(on, dtype=bool), np.zeros(off, dtype=bool)]
    return np.tile(pattern, int(np.ceil(T / pattern.size)))[:T]


# ---------------------------
# Real-valued tests
# ---------------------------

def fmri_p_val(fmridata, voxel_location=None, stimulus_idx=None, rest_idx=None,
               epoch_length=10, is_4d=True, test_type="t-test"):
    """
    Per-voxel real-valued test (t-test or Wilcoxon) using epoch means.
    fmridata: 1D time series or 4D array (X,Y,Z,T)
    stimulus_idx: 0-based indices (list/array) OR boolean vector (length T)
    """
    fmridata = np.asarray(fmridata)
    # Extract 1D voxel series
    if is_4d and voxel_location is not None:
        x, y, z = voxel_location
        voxel = fmridata[x, y, z, :]
    else:
        voxel = fmridata

    T = voxel.shape[0]

    # on/off indices
    if stimulus_idx is None:
        on_mask = _default_onoff(T)
        on_idx = np.flatnonzero(on_mask)
    else:
        stim = np.asarray(stimulus_idx)
        on_idx = np.flatnonzero(stim) if stim.dtype == bool else np.asarray(stim, int)

    if rest_idx is None:
        off_idx = np.setdiff1d(np.arange(T), on_idx, assume_unique=True)
    else:
        off_idx = np.asarray(rest_idx, int)

    # epoch means
    vox_on = voxel[on_idx]
    vox_off = voxel[off_idx]

    # pad to multiples of epoch_length (minimal change to your approach)
    def _pad_to_epochs(a):
        n = int(np.ceil(a.size / epoch_length) * epoch_length)
        if n > a.size:
            a = np.pad(a, (0, n - a.size), mode="edge")
        return a.reshape(epoch_length, -1).mean(axis=0)

    g1 = _pad_to_epochs(vox_on)
    g2 = _pad_to_epochs(vox_off)

    if test_type == "t-test":
        return float(ttest_ind(g1, g2, alternative="greater", equal_var=False).pvalue)
    elif test_type == "wilcoxon_test":
        # Wilcoxon requires equal lengths; trim to min
        n = min(g1.size, g2.size)
        return float(wilcoxon(g1[:n], g2[:n], alternative="greater").pvalue)
    else:
        raise ValueError("Please type a valid test type: 't-test' or 'wilcoxon_test'.")


# ---------------------------
# Complex-valued tests
# ---------------------------

def fmri_complex_p_val(fmridata, voxel_location=None, method="HotellingsT2",
                       stimulus_idx=None, rest_idx=None, is_4d=True, ons=None, dur=None):
    """
    Two-class test for complex data (Hotelling T2 or Wilks-Lambda).
    Returns (test_result, method)
    """
    arr = np.asarray(fmridata)
    if is_4d and voxel_location is not None:
        x, y, z = voxel_location
        voxel = arr[x, y, z, :]
    else:
        voxel = arr

    T = voxel.shape[0]

    # on/off indices
    if stimulus_idx is None:
        on_mask = _default_onoff(T)
        on_idx = np.flatnonzero(on_mask)
    else:
        stim = np.asarray(stimulus_idx)
        on_idx = np.flatnonzero(stim) if stim.dtype == bool else np.asarray(stim, int)

    if rest_idx is None:
        off_idx = np.setdiff1d(np.arange(T), on_idx, assume_unique=True)
    else:
        off_idx = np.asarray(rest_idx, int)

    # Build real/imag pairs for on/off
    Y1 = np.vstack([voxel[on_idx].real, voxel[on_idx].imag]).T  # (n1, 2)
    Y2 = np.vstack([voxel[off_idx].real, voxel[off_idx].imag]).T  # (n2, 2)

    # stack to DataFrame with labels 1/0
    y12 = np.vstack([Y1, Y2])
    labels = np.r_[np.ones(Y1.shape[0]), np.zeros(Y2.shape[0])]
    df = pd.DataFrame({"real": y12[:, 0], "complex": y12[:, 1], "labels": labels})

    if method == "HotellingsT2":
        if hotelling_t2 is None:
            raise ImportError("hotelling package is not installed. pip install hotelling")
        # hotelling_t2 expects groups; some versions require a formula or grouped df.
        # Many users call it as hotelling_t2(df[['real','complex']], groups=df['labels'])
        # Here we try the common pattern; adjust if your version differs.
        out = hotelling_t2(df[["real", "complex"]], df["labels"])
        return out, method

    elif method == "Wilks-Lambda":
        if MANOVA is None:
            raise ImportError("statsmodels MANOVA is not available.")
        maov = MANOVA.from_formula("real + complex ~ labels", data=df)
        # retrieve Wilks' lambda row
        res = maov.mv_test().results["labels"]["stat"]
        return res.loc["Wilks' lambda"], method

    else:
        raise ValueError("method must be 'HotellingsT2' or 'Wilks-Lambda'.")


# ---------------------------
# HRF GLM p-values (real-valued), returns (X,Y,Z) map
# ---------------------------

def fmri_hrf_p_val(fmridata, ons=None, dur=None, mask=None, tr=1.0):
    """
    Fit y = b0 + b1*r(t) voxelwise, where r(t) is boxcar(ons,dur) convolved HRF (here: simple boxcar).
    Returns p-value map for regressor b1: shape (X,Y,Z).
    Minimal-change: uses one regressor + intercept; no HTML parsing.
    """
    data = np.asarray(fmridata, float)
    if data.ndim != 4:
        raise ValueError("fmridata must be 4D: (X,Y,Z,T)")
    Xdim, Ydim, Zdim, T = data.shape

    # Build regressor r(t): if ons/dur missing, use default 10-on/10-off
    if ons is None or dur is None:
        r = _default_onoff(T).astype(float)
    else:
        r = _boxcar_from_ons_dur(T, ons, dur)

    # Normalize regressor; guard constant
    r = (r - r.mean()) / (r.std() + 1e-12)
    if not np.isfinite(r).all() or r.std() < 1e-12:
        # No usable regressor → all p=1
        return np.ones((Xdim, Ydim, Zdim), float)

    # Design matrix with intercept
    X = np.column_stack([np.ones(T), r])  # (T, 2)

    # Output p-value map
    p_map = np.ones((Xdim, Ydim, Zdim), dtype=float)
    if mask is not None:
        mask = np.asarray(mask, bool)
        if mask.shape != (Xdim, Ydim, Zdim):
            raise ValueError("mask shape must match fmridata spatial dims")

    # Voxel loop (simple and clear; vectorization is possible but not required)
    for i in range(Xdim):
        # print(f"slice {i+1}/{Xdim}")  # uncomment if you want progress
        for j in range(Ydim):
            for k in range(Zdim):
                if mask is not None and not mask[i, j, k]:
                    p_map[i, j, k] = 1.0
                    continue
                y = data[i, j, k, :].astype(float)

                # guard constant/invalid series
                if not np.isfinite(y).all() or y.std() < 1e-12:
                    p_map[i, j, k] = 1.0
                    continue

                # OLS (no summary, no HTML)
                res = sm.OLS(y, X, hasconst=True).fit()
                # param[1] is the HRF regressor; pvalues[1] its p-value
                p = float(res.pvalues[1]) if res.pvalues.size > 1 and np.isfinite(res.pvalues[1]) else 1.0
                p_map[i, j, k] = p

    return np.nan_to_num(p_map, nan=1.0, posinf=1.0, neginf=1.0)


# ---------------------------
# On/Off "volume" difference (kept close to your original)
# ---------------------------

def fmri_on_off_volume(data, x, y, z, coordinates="polar"):
    """
    Very rough on/off contrast at one voxel.
    """
    voxel_data = np.asarray(data)[x, y, z, :]
    on_data = []
    off_data = []
    for t in range(voxel_data.size):
        if (t // 10) % 2 == 0:
            on_data.append(voxel_data[t])
        else:
            off_data.append(voxel_data[t])
    on_data = np.array(on_data, float)
    off_data = np.array(off_data, float)

    if coordinates == "polar":
        # energy difference
        return float((np.sum(on_data ** 2) - np.sum(off_data ** 2)) / max(1, on_data.size))
    elif coordinates == "cartesian":
        # (kept minimal; your original cartesian code had several indexing bugs)
        return float((np.sum(on_data) - np.sum(off_data)) / max(1, on_data.size))
    else:
        raise ValueError("coordinates must be 'polar' or 'cartesian'.")


# ---------------------------
# Example usage
# ---------------------------

if __name__ == "__main__":
    # Simulated complex 4D data from your helper
    sim = fmri_simulate_func(
        dim_data=[64, 64, 40], mask=None,
        ons=[1, 21, 41, 61, 81, 101, 121, 141],
        dur=[10, 10, 10, 10, 10, 10, 10, 10]
    )
    data = sim["fmridata"]           # (64,64,40,160) complex
    mag = np.abs(data)               # use magnitude for HRF GLM

    # Optional mask: here everything is "brain"
    mask = np.ones(mag.shape[:3], dtype=bool)

    # Build stimulus as boolean 10-on/10-off (like your R code)
    T = mag.shape[-1]
    stim_bool = _default_onoff(T)    # length 160, True/False pattern

    # 1) Per-voxel HRF p-map (simple 1-regressor GLM)
    pmap = fmri_hrf_p_val(mag, ons=[1, 21, 41, 61, 81, 101, 121, 141],
                          dur=[10] * 8, mask=mask)
    print("HRF p-map:", pmap.shape, pmap.min(), pmap.max())

    # 2) Single-voxel real test (t-test) using epoch means
    pv = fmri_p_val(mag, voxel_location=(20, 30, 20),
                    stimulus_idx=np.flatnonzero(stim_bool),
                    is_4d=True, test_type="t-test")
    print("Single-voxel t-test p:", pv)

