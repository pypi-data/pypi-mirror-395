import numpy as np
from plotly.subplots import make_subplots
from .visual_2d import fmri_2dvisual


def _parse_axis_indices(axis_i_lses, n_vols):
    """
    Normalize axis_i_lses into:
        per_vol: list of (ix, iy, iz) tuples, one per volume
        axes_to_show: list of axes to show, subset of ['x', 'y', 'z']
    axis_i_lses can be:
      - [ix, iy, iz]  (shared across all volumes)
      - [[ix1, iy1, iz1], [ix2, iy2, iz2], ...] (one per volume)
    Use None instead of NULL to skip a direction.
    """
    if not isinstance(axis_i_lses, (list, tuple)):
        raise ValueError("'axis_i_lses' must be a list/tuple.")

    # Case 1: list of lists/tuples, one triple per volume
    if axis_i_lses and isinstance(axis_i_lses[0], (list, tuple)):
        if len(axis_i_lses) != n_vols:
            raise ValueError(
                "If 'axis_i_lses' is a list of lists, it must have "
                "one [ix, iy, iz] triple per p-value volume."
            )
        per_vol = []
        for triplet in axis_i_lses:
            if len(triplet) != 3:
                raise ValueError("Each axis index triple must have length 3 (ix, iy, iz).")
            per_vol.append(tuple(triplet))
    # Case 2: single triple reused for all volumes
    elif len(axis_i_lses) == 3:
        per_vol = [tuple(axis_i_lses)] * n_vols
    else:
        raise ValueError("'axis_i_lses' must either be length 3 or length n_vols of triples.")

    axis_names = ["x", "y", "z"]
    # Decide which axes are used at least once
    axes_to_show = []
    for dim_idx, axis_name in enumerate(axis_names):
        if any(tr[dim_idx] is not None for tr in per_vol):
            axes_to_show.append(axis_name)

    if not axes_to_show:
        raise ValueError("No axis indices supplied (all None). Nothing to plot.")

    return per_vol, axes_to_show


def _extract_slice(volume3d, mask3d, hemody3d, axis, index):
    """
    Extract 2D slices from volume, mask, and hemody along given axis at 'index'.
    Returns (p2d, mask2d, hemody2d or None, xs, ys).
    volume3d is p-values; we will convert to (1 - p) later.
    """
    if index is None:
        return None  # signal to skip

    vol = np.asarray(volume3d)
    mask = np.asarray(mask3d) if mask3d is not None else None
    hemody = np.asarray(hemody3d) if hemody3d is not None else None

    if axis == "x":
        # index along axis 0 → slice over (y, z)
        p2d = vol[index, :, :]
        mask2d = mask[index, :, :] if mask is not None else None
        hemody2d = hemody[index, :, :] if hemody is not None else None
        ys = np.arange(p2d.shape[0])  # y dimension
        xs = np.arange(p2d.shape[1])  # z dimension
        xlabel, ylabel = "Voxel (z)", "Voxel (y)"
    elif axis == "y":
        # index along axis 1 → slice over (x, z)
        p2d = vol[:, index, :]
        mask2d = mask[:, index, :] if mask is not None else None
        hemody2d = hemody[:, index, :] if hemody is not None else None
        ys = np.arange(p2d.shape[0])  # x dimension
        xs = np.arange(p2d.shape[1])  # z dimension
        xlabel, ylabel = "Voxel (z)", "Voxel (x)"
    elif axis == "z":
        # index along axis 2 → slice over (x, y)
        p2d = vol[:, :, index]
        mask2d = mask[:, :, index] if mask is not None else None
        hemody2d = hemody[:, :, index] if hemody is not None else None
        ys = np.arange(p2d.shape[0])  # x dimension
        xs = np.arange(p2d.shape[1])  # y dimension
        xlabel, ylabel = "Voxel (y)", "Voxel (x)"
    else:
        raise ValueError("axis must be one of 'x', 'y', 'z'.")

    return p2d, mask2d, hemody2d, xs, ys, xlabel, ylabel


def fmri_pval_comparison_2d(
    pval_ls,
    pval_name_ls,
    axis_i_lses,
    hemody_data=None,
    mask=None,
    p_threshold=0.05,
    legend_show=True,
    method="scale_p",
    color_pal="YlOrRd",
    multi_pranges=True,
    mask_width=1.5,
):
    """
    Python version of fmri_pval_comparison_2d.

    Parameters
    ----------
    pval_ls : list of 3D numpy arrays
        Each element is a 3D p-value volume.
    pval_name_ls : list of str
        Names for each p-value volume.
    axis_i_lses : list
        Either:
          - [ix, iy, iz] used for all volumes, or
          - [[ix1, iy1, iz1], [ix2, iy2, iz2], ...] one triple per volume.
        Use None for any axis you want to skip.
    hemody_data : 3D numpy array or None
        3D hemodynamic volume to overlay as contours.
    mask : 3D numpy array
        Brain mask volume.
    p_threshold : float
        Threshold in (0, 0.05] to drop p-values above this.
    legend_show : bool
        Whether to show colorbars for subplots.
    method : {"scale_p"}
        Currently only "scale_p" is supported, matching fmri_2dvisual.
    color_pal : str
        Matplotlib colormap name (e.g. "YlOrRd").
    multi_pranges : bool
        If True, use more p-bins; passed through to fmri_2dvisual.
    mask_width : float
        Line width for mask contour.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Multi-panel comparison figure.
    """
    # Basic checks
    if not isinstance(pval_ls, (list, tuple)) or not isinstance(pval_name_ls, (list, tuple)):
        raise ValueError("'pval_ls' and 'pval_name_ls' must be lists/tuples.")
    if len(pval_ls) != len(pval_name_ls):
        raise ValueError("'pval_ls' and 'pval_name_ls' must have the same length.")

    n_vols = len(pval_ls)

    if mask is None:
        raise ValueError("'mask' must be provided as a 3D array.")

    mask = np.asarray(mask)
    if mask.ndim != 3:
        raise ValueError("'mask' must be a 3D array.")

    if hemody_data is not None:
        hemody_data = np.asarray(hemody_data)
        if hemody_data.shape != mask.shape:
            raise ValueError("'hemody_data' must have the same shape as 'mask' and p-values.")

    if not (0 < p_threshold <= 0.05):
        raise ValueError("'p_threshold' must be in (0, 0.05].")

    if method != "scale_p":
        raise NotImplementedError(
            "This Python implementation currently only supports method='scale_p', "
            "which matches the fmri_2dvisual behavior."
        )

    # Normalize axis indices
    per_vol_indices, axes_to_show = _parse_axis_indices(axis_i_lses, n_vols)

    # Build subplot grid: rows = volumes, cols = number of axes used
    n_cols = len(axes_to_show)
    subplot_titles = []
    for name in pval_name_ls:
        for axis in axes_to_show:
            subplot_titles.append(f"{name} ({axis}-slice)")

    fig = make_subplots(
        rows=n_vols,
        cols=n_cols,
        subplot_titles=subplot_titles,
        horizontal_spacing=0.03,
        vertical_spacing=0.08,
    )

    # Fill in subplots
    for vol_idx, (pvals_3d, vol_name, (ix, iy, iz)) in enumerate(
        zip(pval_ls, pval_name_ls, per_vol_indices), start=1
    ):
        indices = {"x": ix, "y": iy, "z": iz}
        for col_idx, axis in enumerate(axes_to_show, start=1):
            index = indices[axis]
            if index is None:
                # No slice requested for this axis in this volume; skip plot.
                continue

            extract = _extract_slice(pvals_3d, mask, hemody_data, axis, index)
            if extract is None:
                continue

            p2d, mask2d, hemody2d, xs, ys, xlabel, ylabel = extract

            # Convert p to (1 - p) for fmri_2dvisual
            omp2d = 1.0 - np.asarray(p2d, float)

            # Show colorbar only on the last column of the last row if legend_show is True
            show_legend_here = legend_show and (
                (vol_idx == n_vols) and (col_idx == n_cols)
            )

            subfig = fmri_2dvisual(
                omp2d=omp2d,
                mask2d=mask2d,
                p_threshold=p_threshold,
                multi_pranges=multi_pranges,
                color_pal=color_pal,
                title="",  # subplot_titles already used
                xlabel=xlabel,
                ylabel=ylabel,
                xs=xs,
                ys=ys,
                legend_show=show_legend_here,
                mask_width=mask_width,
                hemody2d=hemody2d,
            )

            # Add traces from subfig into the correct subplot cell
            for trace in subfig.data:
                fig.add_trace(trace, row=vol_idx, col=col_idx)

            # Sync axis properties (square pixels)
            fig.update_xaxes(scaleanchor=f"y{vol_idx}", row=vol_idx, col=col_idx)

    fig.update_layout(
        height=300 * n_vols,
        width=350 * n_cols,
        showlegend=False,  # we handle colorbar via heatmap, not legend entries
        title="fMRI p-value comparison (2D slices)",
    )

    return fig
