import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ..core.stimulus_detect import fmri_stimulus_detect
from ..core.post_hoc import fmri_post_hoc

try:
    import nibabel as nib  # optional (only if users pass a NIfTI image)
except Exception:  # pragma: no cover
    nib = None


def fmri_3dvisual(
    pval,
    mask,
    p_threshold: float | None = 0.05,
    method: str = "scale_p",
    color_pal: str = "YlOrRd",
    multi_pranges: bool = True,
    title: str | None = None
):
    """
    Visualization of the 3D brain with activated areas (Plotly).

    Parameters
    ----------
    pval : np.ndarray
        3D array of p-values (ZYX or XYZ – treated as numpy [x, y, z] indexing).
    mask : np.ndarray or nib.Nifti1Image
        3D NIfTI image or 3D array defining the brain volume (shell).
    p_threshold : float or None, default 0.05
        If method='scale_p', keep voxels with p <= p_threshold (0 < p <= 0.05).
        If method='low5_percent', set this to None.
    method : {'scale_p', 'low5_percent'}, default 'scale_p'
        'scale_p'  — fixed p-value bins (like the R version).
        'low5_percent' — color the lowest 5% p-values present.
    color_pal : str, default 'YlOrRd'
        Name of Plotly color scale (e.g., 'YlOrRd', 'Viridis', etc.).
    multi_pranges : bool, default True
        If True, use up to 9 bins; if False, use up to 4 bins (coarser legend).
    title : str or None, default None
        Figure title.

    Returns
    -------
    dict
        {
          "fig": plotly.graph_objects.Figure,
          "pval_df": pandas.DataFrame with columns:
              ['x','y','z','p_val','bin','colorgrp','color']
        }
    """

    # ---------- Validation ----------
    if not (isinstance(pval, np.ndarray) and pval.ndim == 3):
        raise ValueError("'pval' should be a 3D numpy array.")
    if hasattr(mask, "shape") and isinstance(mask, np.ndarray):
        mask_arr = mask
    elif (nib is not None) and isinstance(mask, nib.Nifti1Image):
        mask_arr = np.asarray(mask.get_fdata())
    else:
        raise ValueError("'mask' should be a 3D numpy array or a NIfTI image.")
    if mask_arr.ndim != 3:
        raise ValueError("'mask' should be 3D.")
    if method not in ("scale_p", "low5_percent"):
        raise ValueError("'method' must be 'scale_p' or 'low5_percent'.")
    if method == "scale_p":
        if p_threshold is None:
            raise ValueError("For 'scale_p', 'p_threshold' must be a number in (0, 0.05].")
        if not (isinstance(p_threshold, (int, float)) and (0 < p_threshold <= 0.05)):
            raise ValueError("'p_threshold' should be numeric in (0, 0.05].")
    else:
        # low5_percent
        if p_threshold is not None:
            raise ValueError("For 'low5_percent', set 'p_threshold=None'.")

    if pval.shape != mask_arr.shape:
        raise ValueError("Shapes of 'pval' and 'mask' must match.")

    # ---------- Prep voxel table ----------
    # Create a voxel coordinate grid
    sx, sy, sz = pval.shape
    xs = np.arange(sx)
    ys = np.arange(sy)
    zs = np.arange(sz)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")

    df = pd.DataFrame({
        "x": X.ravel(),
        "y": Y.ravel(),
        "z": Z.ravel(),
        "p_val": pval.ravel(),
        "mask_val": mask_arr.ravel()
    })

    # Only consider voxels inside mask (mask > 0)
    df = df[df["mask_val"] > 0].copy()

    # ---------- Select voxels to display & binning ----------
    if method == "scale_p":
        # Keep voxels under threshold
        df = df[df["p_val"] <= p_threshold].copy()
        if df.empty:
            raise ValueError(
                "No voxels survive the selected threshold. "
                "Try a larger 'p_threshold' (≤ 0.05) or use method='low5_percent'."
            )

        if multi_pranges:
            # 9 bins (like the R code)
            bins = [0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 5e-2]
            labels = [
                "[0,1e-8]", "(1e-8,1e-7]", "(1e-7,1e-6]", "(1e-6,1e-5]",
                "(1e-5,1e-4]", "(1e-4,1e-3]", "(1e-3,1e-2]", "(1e-2,5e-2]"
            ]
        else:
            # 4 bins
            bins = [0, 1e-7, 1e-5, 1e-3, 5e-2]
            labels = ["[0,1e-7]", "(1e-7,1e-5]", "(1e-5,1e-3]", "(1e-3,5e-2]"]

        df["bin"] = pd.cut(df["p_val"], bins=bins, labels=labels, include_lowest=True, right=True)

    else:  # method == "low5_percent"
        q5 = np.nanquantile(df["p_val"].values, 0.05)
        df = df[df["p_val"] <= q5].copy()
        if df.empty:
            raise ValueError("No voxels at or below the 5th percentile of p-values.")

        pmin, pmax = float(df["p_val"].min()), float(df["p_val"].max())
        if np.isclose(pmax - pmin, 0.0):
            # All identical p's
            df["bin"] = pd.Series([f"[{pmin:.3f}]" for _ in range(df.shape[0])], index=df.index)
            labels = sorted(df["bin"].unique().tolist())
        else:
            # 10 equal-width bins between min and max
            k = 10
            edges = np.linspace(pmin, pmax, k)
            # slightly expand extremes to include boundaries robustly
            edges[0] = np.floor(edges[0] * 100) / 100.0
            edges[-1] = np.ceil(edges[-1] * 100) / 100.0
            labels = []
            for i in range(len(edges) - 1):
                left = "[" if i == 0 else "("
                labels.append(f"{left}{edges[i]:.3f},{edges[i+1]:.3f}]")
            df["bin"] = pd.cut(df["p_val"], bins=edges, labels=labels, include_lowest=True, right=True)

    # Drop bins with no members (possible at extremes)
    df = df[~df["bin"].isna()].copy()
    if df.empty:
        raise ValueError("No voxels remain after binning. Adjust method/threshold.")

    # Assign integer groups by bin order
    unique_bins = pd.Categorical(df["bin"]).categories.tolist()
    bin_to_idx = {b: i for i, b in enumerate(unique_bins, start=1)}
    df["colorgrp"] = df["bin"].map(bin_to_idx)

    # ---------- Colors ----------
    # Plotly supports many color scales incl. 'YlOrRd'
    # We’ll sample len(unique_bins) colors from the chosen scale.
    # (Reverse like R does for brewer palettes.)
    def sample_colors(colorscale_name, n):
        # Use Plotly's built-in colorscales by sampling [0..1]
        from plotly.colors import find_intermediate_color, sample_colorscale
        # reversed like in the R code
        return list(reversed(sample_colorscale(colorscale_name, [i/(n-1) if n>1 else 0.5 for i in range(n)])))

    n_bins = len(unique_bins)
    # If multi_pranges is False, mimic R's sparser palette by sub-sampling the 9-scale
    if multi_pranges:
        palette = sample_colors(color_pal, n_bins)
    else:
        # coarser set (still consistent and ordered)
        palette = sample_colors(color_pal, n_bins)

    # map bin index -> color
    idx_to_color = {i: palette[i-1] for i in range(1, n_bins+1)}
    df["color"] = df["colorgrp"].map(idx_to_color)

    # ---------- Figure ----------
    fig = go.Figure()

    # Brain shell using isosurface of mask (simple & robust)
    # Normalize mask to [0,1] and draw a single isosurface at 0.5
    mask_arr = mask_arr.astype(np.float32, copy=False)
    mask_norm = (mask_arr - mask_arr.min()) / (mask_arr.max() - mask_arr.min() + 1e-12)
    fig.add_trace(go.Isosurface(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        value=mask_norm.ravel(),
        isomin=0.5, isomax=0.5, surface_count=1,
        caps=dict(x_show=False, y_show=False, z_show=False),
        opacity=0.05,
        showscale=False,
        name="Brain Shell"
    ))

    # Add points per bin (to control legend entries and sizes like R)
    # Size: larger for more significant groups, mimicking R logic
    # (Reverse order so the most significant bin appears bigger.)
    max_base = n_bins
    for i, b in enumerate(unique_bins, start=1):
        pts = df[df["colorgrp"] == i]
        if pts.empty:
            continue
        size = (max_base - i + 1) + (2 if not multi_pranges else 0)
        fig.add_trace(go.Scatter3d(
            x=pts["x"], y=pts["y"], z=pts["z"],
            mode="markers",
            marker=dict(size=size, color=pts["color"], opacity=0.6),
            name=f"p value in {b}",
            hovertemplate="x=%{x}, y=%{y}, z=%{z}<br>p=%{customdata}<extra></extra>",
            customdata=np.round(pts["p_val"].values, 6)
        ))

    fig.update_scenes(xaxis_title="x", yaxis_title="y", zaxis_title="z", aspectmode="data")
    fig.update_layout(
        title=title or "",
        legend=dict(itemsizing="constant"),
        margin=dict(l=0, r=0, t=40, b=0),
    )

    # Return similar structure as R (plot + table)
    out_df = df.loc[:, ["x", "y", "z", "p_val", "bin", "colorgrp", "color"]].reset_index(drop=True)
    return {"fig": fig, "pval_df": out_df}


# import scipy.io as sio
# from scipy.ndimage import gaussian_filter
# mat = sio.loadmat("./test_data/subj1_run1_complex_all.mat")
# bigim1 = mat["bigim"][:, ::-1, :, :]          # flip Y like R: [,64:1,,]
# bigim1_mod = np.abs(bigim1)

# # Gaussian smoothing in space only (sigma ~3 voxels in x/y, ~1–2 in z)
# smoothmod = np.empty_like(bigim1_mod)
# for t in range(bigim1_mod.shape[-1]):
#     smoothmod[..., t] = gaussian_filter(bigim1_mod[..., t], sigma=(3,3,1), mode="nearest")
# import numpy as np, pyreadr, xarray as xr

# res_mask = pyreadr.read_r("./test_data/mask.rda")
# mask_obj = next(iter(res_mask.values()))
# mask = mask_obj.values if isinstance(mask_obj, xr.DataArray) else np.asarray(mask_obj)
# mask = mask.astype(bool)  # shape should match (X,Y,Z) of your data
# T = bigim1_mod.shape[-1]  # 160
# pattern = np.r_[np.ones(10, bool), np.zeros(10, bool)]
# stimulus_idx = np.tile(pattern, T // pattern.size)[:T]
# pval1 = fmri_stimulus_detect(fmridata= bigim1_mod, mask = mask,
#                              stimulus_idx = stimulus_idx,
#                              method = "HRF" , 
#                              ons = [1, 21, 41, 61, 81, 101, 121, 141], 
#                              dur = [10, 10, 10, 10, 10, 10, 10, 10] )

# pval4 = fmri_post_hoc(pval1, 0.05, 5, False, fdr_corr="fdr")

# res = fmri_3dvisual(
#     pval1, mask,
#     p_threshold=0.05,
#     method="scale_p",
#     multi_pranges=True,              # TRUE -> True in Python
#     title="Accounting for HRF"
# )

# res = fmri_3dvisual(
#     pval4, mask,
#     p_threshold=0.05,
#     method="scale_p",
#     multi_pranges=True,              # TRUE -> True in Python
#     title="Accounting for HRF"
# )

# R: pval1_3d$plot  ->  Python: res["fig"]
# fig = res["fig"]                     # the Plotly figure
# pval_df = res["pval_df"]             # the dataframe, R's pval1_3d$pval_df

# show in a browser (standalone web page)
# fig.write_html(
#     "fmri_activation.html",
#     include_plotlyjs="cdn",
#     full_html=True,
#     auto_open=True                   # opens your default browser
# )