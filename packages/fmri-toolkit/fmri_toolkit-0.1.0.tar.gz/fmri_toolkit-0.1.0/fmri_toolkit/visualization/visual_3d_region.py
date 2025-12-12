import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.spatial import Delaunay
from matplotlib import cm, colors as mpl_colors


def _make_palette(n_colors: int, name: str):
    cmap = cm.get_cmap(name, n_colors)
    return [mpl_colors.to_hex(cmap(i), keep_alpha=False) for i in range(cmap.N)]


def _scale_p_bins(multi_pranges: bool):
    if multi_pranges:
        edges = np.array([0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 5e-2], float)
        labels = [
            "[0,1e-8]", "(1e-8,1e-7]", "(1e-7,1e-6]", "(1e-6,1e-5]",
            "(1e-5,1e-4]", "(1e-4,1e-3]", "(1e-3,1e-2]", "(1e-2,5e-2]"
        ]
    else:
        edges = np.array([0, 1e-7, 1e-5, 1e-3, 5e-2], float)
        labels = ["[0,1e-7]", "(1e-7,1e-5]", "(1e-5,1e-3]", "(1e-3,5e-2]"]
    return edges, labels


def fmri_3dvisual_region(
    pval,
    mask,
    label_index,
    label_name,
    top_num=None,
    p_threshold=0.05,
    method="scale_p",
    multi_pranges=True,
    color_pal="YlOrRd",
    rank=None,
    title=None,
):
    """
    Python translation of fmri_3dvisual_region (R).
    Returns a plotly.graph_objects.Figure.
    """

    def floor_dec(x, level=1):
        return np.round(x - 5 * 10 ** (-level - 1), level)

    def ceiling_dec(x, level=1):
        return np.round(x + 5 * 10 ** (-level - 1), level)

    mask = np.asarray(mask)
    xdim, ydim, zdim = mask.shape

    label_index = np.asarray(label_index)
    label_name = np.asarray(label_name, dtype=str)

    fig = go.Figure()
    if title is not None:
        fig.update_layout(title=title)

    # ---- List-of-two 3D pval volumes (side-by-side brains) ----
    flag = False
    if isinstance(pval, (list, tuple)):
        pval1 = np.asarray(pval[0])
        pval2 = np.asarray(pval[1])
        flag = True
        pval = np.ones((2 * xdim, ydim, zdim), dtype=float)
        pval[:xdim, :, :] = pval1
        pval[xdim:, :, :] = pval2

    # ---- Brain shell generation helpers ----
    def compute_outer_boundary(mask_vol):
        """Get boundary voxels and Delaunay triangulation."""
        xs, ys, zs = np.where(mask_vol != 0)
        if xs.size == 0:
            return None, None
        pts = np.vstack([xs, ys, zs]).T.astype(float)
        tri = Delaunay(pts)
        return pts, tri.simplices

    # Outer brain shell for first brain
    newMask_shell = (mask != 0).astype(int)
    outer_pts, outer_tri = compute_outer_boundary(newMask_shell)
    if outer_pts is not None:
        fig.add_trace(go.Mesh3d(
            x=outer_pts[:, 0],
            y=outer_pts[:, 1],
            z=outer_pts[:, 2],
            i=outer_tri[:, 0],
            j=outer_tri[:, 1],
            k=outer_tri[:, 2],
            opacity=0.01,
            name="Brain Shell",
            contour=dict(show=True, color="#000", width=15),
            showlegend=True,
        ))

    # If list-of-two, shell for second brain shifted in x
    if flag:
        newMask_shell2 = np.zeros((2 * xdim, ydim, zdim), int)
        newMask_shell2[xdim:, :, :] = newMask_shell
        outer_pts2, outer_tri2 = compute_outer_boundary(newMask_shell2)
        if outer_pts2 is not None:
            fig.add_trace(go.Mesh3d(
                x=outer_pts2[:, 0],
                y=outer_pts2[:, 1],
                z=outer_pts2[:, 2],
                i=outer_tri2[:, 0],
                j=outer_tri2[:, 1],
                k=outer_tri2[:, 2],
                opacity=0.01,
                name="Brain Shell",
                contour=dict(show=True, color="#000", width=15),
                showlegend=True,
            ))

    # ---- innerMask: ROI indices re-mapped to 0..len(label_index)-1 ----
    if flag:
        innerMask = np.zeros((2 * xdim, ydim, zdim), int)
        for i in range(xdim):
            for j in range(ydim):
                for k in range(zdim):
                    temp = mask[i, j, k]
                    if temp == 0:
                        continue
                    matches = np.where(label_index == temp)[0]
                    if matches.size > 0:
                        idx = matches[0]  # 0-based
                        innerMask[i, j, k] = idx
                        innerMask[i + xdim, j, k] = idx
    else:
        innerMask = np.zeros((xdim, ydim, zdim), int)
        for i in range(xdim):
            for j in range(ydim):
                for k in range(zdim):
                    temp = mask[i, j, k]
                    if temp == 0:
                        continue
                    matches = np.where(label_index == temp)[0]
                    if matches.size > 0:
                        idx = matches[0]
                        innerMask[i, j, k] = idx

    # ---- Robust detection: 1D vs 3D p-values ----
    pval_arr = np.asarray(pval)

    # Treat (N,), (N,1), (1,N) as 1D ROI-level p-values
    if pval_arr.ndim == 1 or (pval_arr.ndim == 2 and 1 in pval_arr.shape):
        # -------- 1D p-value branch --------
        pval_1d = pval_arr.ravel()
        n_roi = len(pval_1d)

        # Color choices
        if top_num is None:
            color_choice = _make_palette(n_roi, color_pal)
        else:
            color_choice = _make_palette(top_num, color_pal)
        color_choice = color_choice[::-1]  # reverse

        oldPval = pval_1d
        order = np.argsort(oldPval)  # indices sorted by p-value
        newPval = oldPval[order]     # not strictly needed, just like R
        colorPval = np.zeros(n_roi, dtype=int)

        # Assign ranks 1..n_roi according to sorted order
        colorPval[order] = np.arange(1, n_roi + 1)
        if top_num is not None:
            colorPval[colorPval > top_num] = -1  # mark as not drawn

        # ranking = ROI order to draw in
        if rank is not None and rank == "value":
            ranking = order       # sort by p-values
        else:
            ranking = np.arange(n_roi)  # 0..n_roi-1

        # Draw each ROI surface
        for roi_idx in ranking:
            if colorPval[roi_idx] <= 0:
                continue

            newMask_roi = (innerMask == roi_idx).astype(int)
            xs, ys, zs = np.where(newMask_roi == 1)
            if xs.size == 0:
                continue

            pts = np.vstack([xs, ys, zs]).T.astype(float)
            tri = Delaunay(pts)
            faceColor = color_choice[colorPval[roi_idx] - 1]

            fig.add_trace(go.Mesh3d(
                x=pts[:, 0],
                y=pts[:, 1],
                z=pts[:, 2],
                i=tri.simplices[:, 0],
                j=tri.simplices[:, 1],
                k=tri.simplices[:, 2],
                opacity=1.0,
                name=label_name[roi_idx],
                hovertext=[f"p-value: {oldPval[roi_idx]:.3g}"] * len(pts),
                facecolor=faceColor,
                contour=dict(show=True, color="#000", width=15),
                showlegend=True,
            ))

        fig.update_layout(
            scene=dict(
                xaxis_title="x",
                yaxis_title="y",
                zaxis_title="z",
            )
        )
        return fig

    # -------- 3D p-value branch --------
    if pval_arr.ndim != 3:
        raise ValueError(
            "3D p-values must be supplied as a (X, Y, Z) array; "
            f"got shape {pval_arr.shape}"
        )

    dim_pval = pval_arr.shape
    xs = np.arange(dim_pval[0])
    ys = np.arange(dim_pval[1])
    zs = np.arange(dim_pval[2])
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")

    pval_df = pd.DataFrame({
        "x": X.ravel(),
        "y": Y.ravel(),
        "z": Z.ravel(),
        "p_val": pval_arr.ravel()
    })

    # Process 3D p-values according to method
    if method == "scale_p":
        pval_df = pval_df[pval_df["p_val"] <= p_threshold].copy()
        if pval_df.empty:
            fig.update_layout(
                scene=dict(
                    xaxis_title="x",
                    yaxis_title="y",
                    zaxis_title="z",
                )
            )
            return fig

        edges, labels = _scale_p_bins(multi_pranges)
        bin_idx = np.digitize(pval_df["p_val"].to_numpy(), edges, right=True)
        K = len(edges) - 1
        bin_idx[(bin_idx < 1) | (bin_idx > K)] = np.nan
        pval_df["colorgrp"] = bin_idx

    elif method == "low5_percent":
        quantile5 = pval_df["p_val"].quantile(0.05)
        pval_df = pval_df[pval_df["p_val"] <= quantile5].copy()
        if pval_df.empty:
            fig.update_layout(
                scene=dict(
                    xaxis_title="x",
                    yaxis_title="y",
                    zaxis_title="z",
                )
            )
            return fig

        p_min = pval_df["p_val"].min()
        p_max = pval_df["p_val"].max()
        if p_max - p_min != 0:
            cut_pts = p_min + np.arange(10) * (p_max - p_min) / 9.0
            cut_pts[-1] = ceiling_dec(cut_pts[-1], 2)
            cut_pts[0] = floor_dec(cut_pts[0], 2)
            cut_pts = np.unique(np.round(cut_pts, 3))
            bin_idx = np.digitize(pval_df["p_val"].to_numpy(), cut_pts, right=True)
            pval_df["colorgrp"] = bin_idx
        else:
            pval_df["colorgrp"] = 1
    else:
        raise ValueError("method must be 'scale_p' or 'low5_percent'")

    # Choose colors for groups
    if multi_pranges:
        color_choice = _make_palette(9, color_pal)[::-1]
    else:
        full = _make_palette(9, color_pal)[::-1]
        color_choice = full

    colorgrp = pval_df["colorgrp"].to_numpy().astype(int)
    colorgrp[colorgrp <= 0] = 1
    colorgrp[colorgrp > len(color_choice)] = len(color_choice)
    pval_df["corresp_color"] = [color_choice[c - 1] for c in colorgrp]

    # Group name (ROI) for each voxel based on innerMask
    groupname = []
    groupindex = set()
    for x, y, z in zip(pval_df["x"], pval_df["y"], pval_df["z"]):
        roi_idx = innerMask[int(x), int(y), int(z)]
        groupindex.add(roi_idx)
        groupname.append(label_name[roi_idx])
    pval_df["groupname"] = groupname
    groupindex = sorted(groupindex)

    # Add markers per ROI
    for name in sorted(pval_df["groupname"].unique()):
        pts_grp = pval_df[pval_df["groupname"] == name].copy()
        pts_grp = pts_grp.sort_values("colorgrp")
        sizes = []
        for cg in pts_grp["colorgrp"]:
            sizes.append(len(color_choice) - cg + 1 + 2 * int(not multi_pranges) + 2)
        fig.add_trace(go.Scatter3d(
            x=pts_grp["x"],
            y=pts_grp["y"],
            z=pts_grp["z"],
            mode="markers",
            legendgroup=name,
            marker=dict(
                opacity=0.6,
                symbol="circle",
                size=sizes,
                color=pts_grp["corresp_color"],
                line=dict(color=pts_grp["corresp_color"], width=0.3),
            ),
            showlegend=False,
            name=name,
        ))

    # Add ROI shells in ranking order
    if rank is not None:
        ranking = [i for i in rank if i in groupindex]
    else:
        ranking = groupindex

    for roi_idx in ranking:
        newMask_roi = (innerMask == roi_idx).astype(int)
        xs, ys, zs = np.where(newMask_roi == 1)
        if xs.size == 0:
            continue
        pts = np.vstack([xs, ys, zs]).T.astype(float)
        tri = Delaunay(pts)
        faceColor = "#F0FFFF"
        fig.add_trace(go.Mesh3d(
            x=pts[:, 0],
            y=pts[:, 1],
            z=pts[:, 2],
            i=tri.simplices[:, 0],
            j=tri.simplices[:, 1],
            k=tri.simplices[:, 2],
            opacity=0.0,
            name=label_name[roi_idx],
            legendgroup=label_name[roi_idx],
            facecolor=faceColor,
            contour=dict(show=True, color="#000", width=15),
            showlegend=True,
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="z",
        )
    )
    return fig
