import numpy as np
import pandas as pd
from scipy import stats


def fmri_ROI_phase1(
    fmridata,
    label_mask=None,
    label_dict=None,
    stimulus_idx=None,
    rest_idx=None,
    p_threshold=0.05,
):
    """
    p-values on region of interest (ROI) of the brain.

    This is a Python translation of the R function fmri_ROI_phase1.

    Parameters
    ----------
    fmridata : np.ndarray
        4D array (X, Y, Z, T) with fMRI data.
    label_mask : np.ndarray
        3D array (X, Y, Z) of ROI labels (integers).
    label_dict : pandas.DataFrame
        DataFrame with at least two columns:
            - 'index' : numeric ROI indices that match label_mask values
            - 'name'  : ROI names (strings)
    stimulus_idx : array-like of int
        Time indices (0-based) when the stimulus is ON (motion happens).
    rest_idx : array-like of int or None, optional
        Time indices (0-based) when subject is at rest.
        If None, these are taken as the complement of stimulus_idx.
    p_threshold : float, optional
        Threshold in (0, 0.05] used for Bonferroni-corrected significance.

    Returns
    -------
    result : dict
        {
            "all_ROI":  pandas.DataFrame with columns ['index', 'name', 'pval_t']
                        sorted by pval_t ascending,
            "sign_ROI": pandas.DataFrame with only significant ROIs
                        (p <= p_threshold / n_ROIs)
        }
    """

    # ---- Input checks (mirroring the R code) ----
    fmridata = np.asarray(fmridata)
    if fmridata.ndim != 4:
        raise ValueError("'fmridata' should be a 4D array (X, Y, Z, T).")

    if label_mask is None:
        raise ValueError("'label_mask' must be provided.")
    label_mask = np.asarray(label_mask)
    if label_mask.ndim != 3:
        raise ValueError("'label_mask' should be a 3D array.")
    if label_mask.shape != fmridata.shape[:3]:
        raise ValueError(
            "The shape of 'label_mask' must match the first three dimensions of 'fmridata'."
        )

    if label_dict is None or not isinstance(label_dict, pd.DataFrame):
        raise ValueError("'label_dict' should be a pandas DataFrame.")

    if label_dict.shape[1] < 2:
        raise ValueError(
            "'label_dict' should have at least two columns: indices and ROI names."
        )

    # Expect first column numeric indices, second column ROI names
    if not np.issubdtype(label_dict.iloc[:, 0].dtype, np.number):
        raise ValueError(
            "The first column of 'label_dict' must contain numeric ROI indices."
        )
    if not (pd.api.types.is_string_dtype(label_dict.iloc[:, 1].dtype) or
            pd.api.types.is_categorical_dtype(label_dict.iloc[:, 1].dtype)):
        raise ValueError(
            "The second column of 'label_dict' must contain ROI names (string or factor-like)."
        )

    if stimulus_idx is None:
        raise ValueError("'stimulus_idx' must be provided and cannot be None.")

    # ---- Time index handling ----
    time_span = fmridata.shape[3]
    stimulus_idx = np.asarray(stimulus_idx, dtype=int)

    # In R: OFF_idx = setdiff(1:time_span, ON_idx)
    # In Python, time indices are 0..time_span-1
    if rest_idx is None:
        all_idx = np.arange(time_span)
        OFF_idx = np.setdiff1d(all_idx, stimulus_idx)
    else:
        OFF_idx = np.asarray(rest_idx, dtype=int)

    ON_idx = stimulus_idx

    # ---- Compute ON-OFF differences ----
    # Y_ON_OFF has shape (X, Y, Z, N_pairs)
    Y_ON_OFF = fmridata[..., ON_idx] - fmridata[..., OFF_idx]

    # Flatten spatial dims to voxels x time
    n_voxels = np.prod(Y_ON_OFF.shape[:3])
    n_pairs = Y_ON_OFF.shape[3]
    Y_ON_OFF_mat = Y_ON_OFF.reshape(n_voxels, n_pairs)

    # Mean and SD across time (paired differences)
    mean_ON_OFF = Y_ON_OFF_mat.mean(axis=1)
    sd_ON_OFF = Y_ON_OFF_mat.std(axis=1, ddof=1)  # sample SD like R's sd()

    # Temporal CNR
    # (Avoid division by zero warnings; inf/nan will propagate to the t-test)
    with np.errstate(divide="ignore", invalid="ignore"):
        CNR = mean_ON_OFF / sd_ON_OFF

    # Reshape back to 3D
    CNR = CNR.reshape(Y_ON_OFF.shape[:3])

    # ---- ROI-wise t-tests ----
    index = label_dict.iloc[:, 0].to_numpy()
    names = label_dict.iloc[:, 1].to_numpy()
    pval_t = np.empty(len(index), dtype=float)

    for j, roi_idx in enumerate(index):
        roi_mask = (label_mask == roi_idx)
        roi_values = CNR[roi_mask]

        # Filter out NaNs/Infs just in case
        roi_values = roi_values[np.isfinite(roi_values)]

        if roi_values.size == 0:
            # If no voxels, set p-value to NaN
            pval_t[j] = np.nan
        else:
            # One-sample t-test against mean=0 (like t.test(CNR[..]) in R)
            t_stat, p_val = stats.ttest_1samp(roi_values, popmean=0.0, nan_policy="omit")
            pval_t[j] = p_val

    # ---- Build results DataFrames ----
    all_ROI = pd.DataFrame({
        "index": index,
        "name": names,
        "pval_t": pval_t
    }).sort_values("pval_t", ascending=True, na_position="last")

    # Bonferroni correction threshold
    alpha_bonf = p_threshold / len(index)
    sign_ROI = all_ROI[all_ROI["pval_t"] <= alpha_bonf].copy()

    result = {
        "all_ROI": all_ROI,
        "sign_ROI": sign_ROI,
    }
    return result