import numpy as np
import pandas as pd
import plotly.graph_objects as go
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

def fmri_2dvisual(
    omp2d,                 # 2D (1 - p) slice, shape (H, W)
    mask2d,                # 2D mask slice, same shape (bool or 0/1)
    p_threshold,           # float in (0, 0.05]
    multi_pranges,         # True → 9 bins, False → 4 bins
    color_pal,             # e.g., "YlOrRd"
    title, xlabel, ylabel,
    xs, ys,                # 1..N coordinates for plot axes
    legend_show=True,
    mask_width=1.5,
    hemody2d=None,         # NEW: optional 2D hemodynamic slice, same shape
    hemody_ncontours=8,    # NEW: number of contour lines
    hemody_color="blue",   # NEW: contour color
    hemody_width=0.7       # NEW: contour line width
):
    """
    Draw a discrete p-bin heatmap for a single slice with mask outline,
    and optionally overlay hemodynamic contours.
    """
    # Create p-values and threshold
    p2d = 1.0 - np.asarray(omp2d, float)
    keep = (p2d <= p_threshold) & np.isfinite(p2d)

    # Bin edges & labels (fixed scheme to match R)
    edges, labels = _scale_p_bins(multi_pranges)
    K = len(edges) - 1

    # Digitize p into bins. np.digitize returns 1..K for right=True ((a,b])
    bin_idx = np.digitize(p2d, edges, right=True)
    # Zero-out outside-range or filtered cells
    bin_idx[~keep] = 0
    bin_idx[(bin_idx < 1) | (bin_idx > K)] = 0

    # Z grid of bin indices; NaN for dropped cells so heatmap leaves them blank
    Z = np.where(bin_idx == 0, np.nan, bin_idx).astype(float)

    # Discrete colorscale mapping indices 1..K
    palette = _make_palette(K, color_pal)
    colorscale = []
    for k in range(1, K + 1):
        frac = (k - 1) / (K - 1) if K > 1 else 0.0
        colorscale.append([frac, palette[k - 1]])

    fig = go.Figure()

    # Heatmap over full grid (transpose so x=columns, y=rows)
    fig.add_trace(go.Heatmap(
        x=xs, y=ys,
        z=Z.T,
        colorscale=colorscale,
        zmin=1, zmax=K,
        showscale=True,
        colorbar=dict(
            title="p value",
            tickmode="array",
            tickvals=np.linspace(1, K, num=K),
            ticktext=labels,
            len=0.9
        ),
        hoverinfo="skip",
        xgap=0, ygap=0
    ))

    # Mask outline at ~0.5
    mask2d = np.asarray(mask2d, float)
    fig.add_trace(go.Contour(
        z=mask2d.T,
        x=xs, y=ys,
        contours=dict(start=0.5, end=0.5, size=1.0, coloring="none"),
        line=dict(color="black", width=mask_width),
        showscale=False,
        hoverinfo="skip",
        name="mask"
    ))

    # OPTIONAL: Hemodynamic contours
    if hemody2d is not None:
        hemody2d = np.asarray(hemody2d, float)
        if hemody2d.shape != mask2d.shape:
            raise ValueError("hemody2d must have the same shape as mask2d/omp2d.")
        fig.add_trace(go.Contour(
            z=hemody2d.T,
            x=xs, y=ys,
            ncontours=int(hemody_ncontours),            # move here
            contours=dict(coloring="none"),             # keep only coloring here
            line=dict(color=hemody_color, width=float(hemody_width)),
            showscale=False,
            hoverinfo="skip",
            name="hemodynamic"
        ))

    fig.update_layout(
        title=title,
        xaxis=dict(title=xlabel, scaleanchor="y", scaleratio=1),  # coord_fixed
        yaxis=dict(title=ylabel),
        margin=dict(l=60, r=10, t=40, b=50),
        showlegend=bool(legend_show)
    )
    return fig