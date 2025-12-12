import numpy as np
import pandas as pd
from scipy import stats

class ReducedRankRegressor:
    def __init__(self, rank):
        """
        Simple Reduced Rank Regression via SVD of the OLS coefficient matrix.

        Parameters
        ----------
        rank : int
            Desired rank of the coefficient matrix.
        """
        self.rank = rank
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, Y):
        """
        Fit reduced rank regression model.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
        Y : array-like, shape (n_samples, n_targets)
        """
        X = np.asarray(X, dtype=float)
        Y = np.asarray(Y, dtype=float)

        # Center X and Y (like typical regression)
        X_mean = X.mean(axis=0, keepdims=True)
        Y_mean = Y.mean(axis=0, keepdims=True)
        Xc = X - X_mean
        Yc = Y - Y_mean

        # OLS solution: minimize ||Yc - Xc B||_F
        # B_ols has shape (n_features, n_targets)
        B_ols, *_ = np.linalg.lstsq(Xc, Yc, rcond=None)

        # SVD of B_ols and truncate to desired rank
        U, s, Vt = np.linalg.svd(B_ols, full_matrices=False)
        r = min(self.rank, len(s))
        U_r = U[:, :r]                     # (n_features, r)
        S_r = np.diag(s[:r])               # (r, r)
        Vt_r = Vt[:r, :]                   # (r, n_targets)

        # Reduced-rank coefficient matrix
        B_rrr = U_r @ S_r @ Vt_r           # (n_features, n_targets)

        self.coef_ = B_rrr
        # Intercept so that predictions are centered correctly
        self.intercept_ = (Y_mean - X_mean @ self.coef_).ravel()
        return self

    def predict(self, X):
        """
        Predict Y given X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)

        Returns
        -------
        Y_pred : ndarray, shape (n_samples, n_targets)
        """
        X = np.asarray(X, dtype=float)
        return X @ self.coef_ + self.intercept_


def fmri_ROI_phase2(
    fmridata,
    label_mask,
    label_dict,
    stimulus_idx,
    stimulus_dur,
    fmri_design_order=2,
    fmri_stimulus_TR=3,
    rrr_rank=3,
    method="t_test",
    parallel_computing=False,
    ncor=None,
    *,
    fmri_stimulus_func=None,
    fmri_design_func=None,
    rrr_func=None,
):
    """
    Tensor-on-tensor regression on region of interest (ROI) of the brain.
    Python translation of fmri_ROI_phase2, now with default fmri_stimulus/fmri_design.
    """

    # ------------------------------------------------------------------
    # Default implementations (your code) if user does not supply funcs
    # ------------------------------------------------------------------
    if fmri_stimulus_func is None:
        def fmri_stimulus_func(time_span, onsets, durations, TR=fmri_stimulus_TR):
            # Your placeholder: random stimulus vector per time point
            return [np.random.rand(1) for _ in range(time_span)]

    if fmri_design_func is None:
        def fmri_design_func(fixed_stim, order):
            # Your placeholder design: [stim, intercept, random, order]
            initial = np.column_stack((fixed_stim, np.ones(len(fixed_stim))))
            order_col = np.full(len(fixed_stim), order)
            initial = np.column_stack(
                (initial, np.random.rand(len(fixed_stim)), order_col)
            )
            return initial

    if rrr_func is None:
        def rrr_func(X_tensor, Y_tensor, rank):
            """
            Wrapper around ReducedRankRegressor to mimic MultiwayRegression::rrr.

            X_tensor: (T, p, 1)
            Y_tensor: (T, nx, ny, nz)
            Returns an object with attribute .B shaped (p, nx, ny, nz)
            """
            # Flatten X: (T, p, 1) -> (T, p)
            T, p, _ = X_tensor.shape
            X = X_tensor.reshape(T, p)

            # Flatten Y: (T, nx, ny, nz) -> (T, n_vox)
            T2, nx, ny, nz = Y_tensor.shape
            assert T2 == T, "Time dimension mismatch between X_tensor and Y_tensor"
            n_vox = nx * ny * nz
            Y = Y_tensor.reshape(T, n_vox)

            # Fit reduced-rank regression
            model = ReducedRankRegressor(rank=rank)
            model.fit(X, Y)   # X: (n_samples, n_features), Y: (n_samples, n_targets)

            # Coefficients: (p, n_vox)
            B_mat = np.asarray(model.coef_)  # shape should be (p, n_vox)

            # Reshape to (p, nx, ny, nz)
            B_full = B_mat.reshape(p, nx, ny, nz)

            # Make a tiny object with attribute B so it matches our fmri_ROI_phase2 expectation
            class RRRResult:
                def __init__(self, B):
                    self.B = B

            return RRRResult(B_full)


    if parallel_computing:
        raise NotImplementedError(
            "parallel_computing=True is not implemented in this Python version yet."
        )

    # ---- Input checks ----
    fmridata = np.asarray(fmridata)
    if fmridata.ndim != 4:
        raise ValueError("'fmridata' should be a 4D array (X, Y, Z, T).")

    label_mask = np.asarray(label_mask)
    if label_mask.ndim != 3:
        raise ValueError("'label_mask' should be a 3D array.")
    if label_mask.shape != fmridata.shape[:3]:
        raise ValueError(
            "The shape of 'label_mask' must match the first three dimensions of 'fmridata'."
        )

    if not isinstance(label_dict, pd.DataFrame):
        raise ValueError("'label_dict' should be a pandas DataFrame.")
    if label_dict.shape[1] < 2:
        raise ValueError(
            "'label_dict' should have at least two columns as indices and names of the ROI."
        )
    if not np.issubdtype(label_dict.iloc[:, 0].dtype, np.number):
        raise ValueError(
            "First column of 'label_dict' must be numeric ROI indices."
        )

    from pandas.api.types import is_string_dtype, is_categorical_dtype
    if not (is_string_dtype(label_dict.iloc[:, 1].dtype) or
            is_categorical_dtype(label_dict.iloc[:, 1].dtype)):
        raise ValueError(
            "Second column of 'label_dict' must contain ROI names "
            "(character or factor-like)."
        )

    if method not in {"t_test", "corrected_t_test"}:
        raise ValueError("`method` must be 't_test' or 'corrected_t_test'.")

    # ---- Helper: ROI bounding box ----
    def ROI_bounding_box(fmridata_4d, label_mask_3d, label_id):
        fdata = np.abs(fmridata_4d)  # like R's Mod
        time_span_local = fdata.shape[3]

        ROI_index = np.argwhere(label_mask_3d == label_id)  # (N, 3)
        if ROI_index.size == 0:
            return (
                np.zeros((0, 0, 0, time_span_local), dtype=fdata.dtype),
                ROI_index,
                ROI_index,
            )

        x_min, y_min, z_min = ROI_index.min(axis=0)
        x_max, y_max, z_max = ROI_index.max(axis=0)

        ROI_index_move = ROI_index.copy()
        ROI_index_move[:, 0] -= x_min
        ROI_index_move[:, 1] -= y_min
        ROI_index_move[:, 2] -= z_min

        nx = x_max - x_min + 1
        ny = y_max - y_min + 1
        nz = z_max - z_min + 1
        bounding_box = np.zeros((nx, ny, nz, time_span_local), dtype=fdata.dtype)

        x0, y0, z0 = ROI_index.T
        xm, ym, zm = ROI_index_move.T
        for t in range(time_span_local):
            bounding_box[xm, ym, zm, t] = fdata[x0, y0, z0, t]

        return bounding_box, ROI_index, ROI_index_move

    # ---- Helper: p-values from block ----
    def block_p_value(BOLD_coef, time_span_local, num_of_predictors):
        n = time_span_local
        p = num_of_predictors

        sd_global = np.nanstd(BOLD_coef, ddof=1)
        if sd_global == 0 or not np.isfinite(sd_global):
            t_value = np.zeros_like(BOLD_coef, dtype=float)
        else:
            with np.errstate(divide="ignore", invalid="ignore"):
                t_value = BOLD_coef / sd_global

        df = n - p - 1
        p_value = 2 * stats.t.sf(np.abs(t_value), df=df)
        return p_value

    # ---- Main body ----
    time_span = fmridata.shape[3]

    fixed_stim = fmri_stimulus_func(
        time_span,
        onsets=np.asarray(stimulus_idx, dtype=int),
        durations=np.asarray(stimulus_dur, dtype=int),
        TR=fmri_stimulus_TR,
    )

    X_tensor = fmri_design_func(fixed_stim, order=fmri_design_order)
    X_tensor = np.asarray(X_tensor)
    X_tensor = X_tensor.reshape(time_span, fmri_design_order + 2, 1)

    overall_p_value = np.ones(fmridata.shape[:3], dtype=float)

    label_list = label_dict.iloc[:, 0].to_numpy()
    num_predictors = fmri_design_order + 2

    for label_id in label_list:
        bounding_box, ROI_index, ROI_index_move = ROI_bounding_box(
            fmridata, label_mask, label_id
        )
        if ROI_index.size == 0:
            continue

        # Y_tensor: (T, nx, ny, nz)
        Y_tensor = np.transpose(bounding_box, (3, 0, 1, 2))

        rrr_result = rrr_func(X_tensor, Y_tensor, rank=rrr_rank)
        B_full = np.asarray(rrr_result.B)
        BOLD_coef = B_full[0]  # (nx, ny, nz)

        if method == "t_test":
            p_block = block_p_value(BOLD_coef, time_span, num_predictors)
        else:
            sd_block = np.std(bounding_box, axis=3, ddof=1)
            with np.errstate(divide="ignore", invalid="ignore"):
                corrected_BOLD = BOLD_coef / sd_block
            corrected_BOLD[~np.isfinite(corrected_BOLD)] = 0.0
            p_block = block_p_value(corrected_BOLD, time_span, num_predictors)

        x0, y0, z0 = ROI_index.T
        xm, ym, zm = ROI_index_move.T
        overall_p_value[x0, y0, z0] = p_block[xm, ym, zm]

    return overall_p_value
