import numpy as np
import pandas as pd
import plotly.graph_objects as go
from .visual_3d import fmri_3dvisual

def fmri_pval_comparison_3d(
    pval_3d_ls,                 # [pval1, pval2]  (each (X,Y,Z) array of p-values)
    mask,                       # (X,Y,Z) mask array or NIfTI (your fmri_3dvisual already handles both)
    p_threshold_ls,             # [thr1, thr2]  (floats or None if 'low5_percent')
    method_ls,                  # ['scale_p'|'low5_percent', 'scale_p'|'low5_percent']
    color_pal_ls=("YlOrRd", "YlGnBu"),
    multi_pranges=True,
    titles=("Map 1", "Map 2"),
    first_map_keep_markers=True # keep the markers fmri_3dvisual put for map 1
):
    """
    Build a single 3D comparison figure by reusing fmri_3dvisual:

    - Call fmri_3dvisual for the first map to get the brain shell + its markers.
    - Call fmri_3dvisual for the second map to get its pval_df (no need to reuse its fig).
    - Overlay the second map as triangle markers sized by bin rank (R-style).

    Returns
    -------
    dict with:
      fig        : Plotly Figure
      pval_df_1  : DataFrame from fmri_3dvisual map 1
      pval_df_2  : DataFrame from fmri_3dvisual map 2
    """
    if len(pval_3d_ls) != 2 or len(p_threshold_ls) != 2 or len(method_ls) != 2:
        raise ValueError("Provide exactly two volumes, thresholds, and methods.")

    pval1, pval2 = pval_3d_ls
    thr1,  thr2  = p_threshold_ls
    meth1, meth2 = method_ls
    pal1,  pal2  = color_pal_ls

    # 1) Base fig (shell + first map) via fmri_3dvisual
    res1 = fmri_3dvisual(
        pval=pval1,
        mask=mask,
        p_threshold=thr1,
        method=meth1,
        color_pal=pal1,
        multi_pranges=multi_pranges,
        title=titles[0]
    )
    fig = res1["fig"]
    df1 = res1["pval_df"]

    # Optional: if you want to remove map-1 markers and re-add them with a uniform size,
    # you could filter fig.data and rebuild, but by default we keep them.
    if not first_map_keep_markers:
        # keep only the first trace (isosurface shell) and remove scatter markers
        shell_traces = [tr for tr in fig.data if isinstance(tr, go.Isosurface)]
        fig.data = tuple(shell_traces)
        # re-add map1 markers with a fixed size
        if not df1.empty:
            fig.add_trace(go.Scatter3d(
                x=df1["x"], y=df1["y"], z=df1["z"],
                mode="markers",
                marker=dict(size=4, color=df1["color"], opacity=0.6,
                            line=dict(color=df1["color"], width=0.3)),
                name=titles[0]
            ))

    # 2) Second map via fmri_3dvisual (reuse only the pval_df; avoid duplicating the shell)
    res2 = fmri_3dvisual(
        pval=pval2,
        mask=mask,
        p_threshold=thr2,
        method=meth2,
        color_pal=pal2,
        multi_pranges=multi_pranges,
        title=titles[1]
    )
    df2 = res2["pval_df"]

    # 3) Overlay second map as triangle markers, grouped by p-bin with size by reversed rank
    if not df2.empty:
        # bins are ordered via 'colorgrp' (1..K). We want largest size for most-significant (smallest p),
        # which corresponds to highest colorgrp if your bin ordering is ascending in p.
        groups = sorted(df2["colorgrp"].unique())
        K = len(groups)
        bump = 2 if (multi_pranges is False) else 0
        # map each group to its label/color once
        grp_label = df2.groupby("colorgrp")["bin"].first().to_dict()
        grp_color = df2.groupby("colorgrp")["color"].first().to_dict()

        for rank, grp in enumerate(groups, start=1):
            rev_rank = K - rank + 1
            size = rev_rank + bump
            pts = df2[df2["colorgrp"] == grp]
            fig.add_trace(go.Scatter3d(
                x=pts["x"], y=pts["y"], z=pts["z"],
                mode="markers",
                marker=dict(
                    symbol="circle",
                    size=int(size),
                    opacity=0.6,
                    color=grp_color[grp],
                    line=dict(color=grp_color[grp], width=0.3)
                ),
                name=f"p value in {grp_label[grp]}"
            ))

    # Final layout polish
    fig.update_layout(
        title=f"{titles[0]} + {titles[1]} (3D comparison)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    fig.update_scenes(aspectmode="data", xaxis_title="x", yaxis_title="y", zaxis_title="z")

    return {"fig": fig, "pval_df_1": df1, "pval_df_2": df2}
