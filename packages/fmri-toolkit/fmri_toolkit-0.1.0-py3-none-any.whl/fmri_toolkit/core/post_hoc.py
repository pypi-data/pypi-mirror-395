import numpy as np
from scipy.ndimage import label, generate_binary_structure
import matplotlib.pyplot as plt


def _fdr_bh(pvals):
    """
    Benjamini–Hochberg FDR correction (vectorized, dependency-free).
    Returns pvals adjusted to q-values, same shape as input.
    """
    p = np.asarray(pvals, dtype=float).ravel()
    n = p.size
    order = np.argsort(p)
    ranked_p = p[order]
    # BH: q_i = p_(i) * n / i, then take cumulative min from the end, clamp to [0,1]
    ranks = np.arange(1, n + 1, dtype=float)
    q = ranked_p * n / ranks
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0.0, 1.0)
    # restore original order
    q_full = np.empty_like(q)
    q_full[order] = q
    return q_full.reshape(pvals.shape)


def _cluster_filter_significant(pvals, thr, min_size, connectivity=1):
    """
    Keep only voxels that belong to significant clusters.

    Parameters
    ----------
    pvals : 3D ndarray of p-values
    thr : float, p-value threshold (e.g., 0.05)
    min_size : int, minimum cluster size to keep
    connectivity : int, 1 => 6-neighborhood; 2 => 18; 3 => 26

    Returns
    -------
    mask_keep : 3D boolean mask where True means voxel survives clustering.
    """
    if pvals.ndim != 3:
        raise ValueError("pvals must be a 3D array.")
    # Significant voxels: p <= thr
    sig = pvals <= thr

    # Define neighborhood: generate_binary_structure(3,1) == 6-neighborhood
    # 1 -> faces (6), 2 -> faces+edges (18), 3 -> faces+edges+corners (26)
    structure = generate_binary_structure(rank=3, connectivity=min(max(connectivity, 1), 3))

    labeled, n_clusters = label(sig, structure=structure)
    if n_clusters == 0:
        return np.zeros_like(sig, dtype=bool)

    # Count cluster sizes
    # labels go from 0..n_clusters; 0 is background
    counts = np.bincount(labeled.ravel())
    # keep labels where size >= min_size
    keep_labels = np.flatnonzero(counts >= int(min_size))
    # exclude background label 0
    keep_labels = keep_labels[keep_labels != 0]

    mask_keep = np.isin(labeled, keep_labels)
    return mask_keep


def fmri_post_hoc(
    p_val_3d,
    fdr_corr=None,
    spatial_cluster_thr=None,
    spatial_cluster_size=None,
    show_comparison=False,
    connectivity=1,
    **hist_kwargs
):
    """
    Post-hoc processing for a 3D p-value array: FDR correction and spatial clustering.

    Parameters
    ----------
    p_val_3d : np.ndarray
        3D array of p-values from fMRI stats.
    fdr_corr : str or None
        Use 'fdr' for Benjamini–Hochberg FDR correction. None to skip.
    spatial_cluster_thr : float or None
        P-value threshold for defining significant voxels in clustering (e.g., 0.05).
    spatial_cluster_size : int or None
        Minimum size of a contiguous cluster to keep.
    show_comparison : bool
        If True, shows hist comparison of raw vs processed p-values.
    connectivity : int
        Neighborhood connectivity for clustering. 1=6, 2=18, 3=26.
    **hist_kwargs :
        Extra kwargs forwarded to matplotlib.pyplot.hist (e.g., bins=50).

    Returns
    -------
    p_processed : np.ndarray
        3D p-values after optional FDR and spatial clustering.
        Clustering preserves original p-values inside kept clusters and sets others to 1.
    """
    p_val_3d = np.asarray(p_val_3d, dtype=float)
    if p_val_3d.ndim != 3:
        raise ValueError("p_val_3d must be a 3D array.")

    p_raw = p_val_3d.copy()
    p_proc = p_val_3d.copy()

    # 1) FDR correction (Benjamini–Hochberg), if requested
    if fdr_corr is not None:
        key = str(fdr_corr).strip().lower()
        if key in {"fdr", "fdr_bh", "bh"}:
            p_proc = _fdr_bh(p_proc)
        else:
            raise ValueError(
                "Unsupported fdr_corr value. Use 'fdr' for Benjamini–Hochberg."
            )

    # 2) Spatial clustering, if requested
    if spatial_cluster_thr is not None and spatial_cluster_size is not None:
        mask_keep = _cluster_filter_significant(
            p_proc, thr=float(spatial_cluster_thr), min_size=int(spatial_cluster_size), connectivity=connectivity
        )
        # In R code: p' = 1 - ((1 - p) * filter), which sets outside-cluster voxels to 1
        p_proc = 1.0 - ((1.0 - p_proc) * mask_keep.astype(float))

    # 3) Optional comparison plot
    if show_comparison:
        # Histogram of raw vs processed p-values, shown one after the other (no subplots)
        # Requirement: one chart per figure.
        plt.figure()
        plt.hist(p_raw.ravel(), alpha=0.5, label="raw p-values", **hist_kwargs)
        plt.legend()
        plt.title("Raw p-values")
        plt.xlabel("p")
        plt.ylabel("count")
        plt.show()

        plt.figure()
        plt.hist(p_proc.ravel(), alpha=0.5, label="post-hoc p-values", **hist_kwargs)
        plt.legend()
        plt.title("Post-hoc p-values")
        plt.xlabel("p")
        plt.ylabel("count")
        plt.show()

    return p_proc
