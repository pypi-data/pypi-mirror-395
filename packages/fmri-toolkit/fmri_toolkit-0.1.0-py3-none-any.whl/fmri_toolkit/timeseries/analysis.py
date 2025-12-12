"""Time series analysis functions for fMRI data.

This module provides visualization tools for analyzing fMRI time series data,
including real, imaginary, magnitude, and phase components.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import detrend
from scipy.ndimage import gaussian_filter1d


def _ksmooth(x, y, kernel="normal", bandwidth=5):
    """
    Kernel smoothing function similar to R's ksmooth.

    Parameters
    ----------
    x : array-like
        x coordinates of the data points
    y : array-like
        y coordinates of the data points
    kernel : str
        Kernel type (currently only "normal"/Gaussian supported)
    bandwidth : float
        Bandwidth for the kernel smoother

    Returns
    -------
    dict
        Dictionary with keys 'x' and 'y' containing smoothed coordinates
    """
    x = np.asarray(x)
    y = np.asarray(y)

    if kernel == "normal":
        # Use Gaussian smoothing with sigma = bandwidth
        y_smooth = gaussian_filter1d(y, sigma=bandwidth, mode='nearest')
        return {'x': x, 'y': y_smooth}
    else:
        raise ValueError(f"Kernel '{kernel}' not supported. Use 'normal'.")


def _gtsplot(data, unit="time point", ts_name=None, colors=None):
    """
    Create a time series plot (GTSplot equivalent from R).

    Parameters
    ----------
    data : array-like or DataFrame
        Time series data with original and smoothed values
    unit : str
        Unit for x-axis label
    ts_name : list of str
        Names for the time series traces
    colors : list of str
        Hex color codes for the traces

    Returns
    -------
    go.Figure
        Plotly figure object
    """
    if ts_name is None:
        ts_name = ["original", "smoothed"]
    if colors is None:
        colors = ["#3366CC", "#DC3912"]

    # Convert hex colors to rgb format if needed
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return f"rgb({int(hex_color[0:2], 16)},{int(hex_color[2:4], 16)},{int(hex_color[4:6], 16)})"

    colors_rgb = [hex_to_rgb(c) if c.startswith('#') else c for c in colors]

    fig = go.Figure()

    # Assume data is a 2-column array/dataframe
    data = np.asarray(data)
    x = np.arange(1, len(data) + 1)

    for i in range(min(data.shape[1], len(ts_name))):
        fig.add_trace(go.Scatter(
            x=x,
            y=data[:, i],
            mode='lines',
            name=ts_name[i],
            line=dict(color=colors_rgb[i])
        ))

    fig.update_layout(
        xaxis_title=unit,
        yaxis_title="Value",
        hovermode='x unified'
    )

    return fig


def fmri_time_series(fmridata, voxel_location=None, is_4d=True, ref=None):
    """
    Visualization of fMRI data (real, imaginary, magnitude, and phase) in time series.

    Creates four interactive time series graphs for the real, imaginary, magnitude,
    and phase parts of fMRI spatiotemporal data.

    Parameters
    ----------
    fmridata : np.ndarray
        4D array containing fMRI spatiotemporal image data (X, Y, Z, T) with complex values,
        or a 1D complex-valued vector if is_4d=False.
    voxel_location : array-like of length 3, optional
        Spatial location [x, y, z] of the voxel (1-based indexing to match R).
        Required if is_4d=True, should be None if is_4d=False.
    is_4d : bool, default=True
        If True, expects 4D array input and extracts time series at voxel_location.
        If False, expects 1D complex vector input.
    ref : array-like, optional
        Optional reference time series to include as a fifth subplot.
        Can be complex-valued (will plot magnitude) or real-valued.

    Returns
    -------
    plotly.graph_objects.Figure
        Interactive time series plot with 4 or 5 subplots

    Examples
    --------
    >>> # With 4D data
    >>> fig = fmri_time_series(fmri_4d_data, voxel_location=[20, 30, 20], is_4d=True)
    >>> fig.show()

    >>> # With 1D vector
    >>> fig = fmri_time_series(voxel_timeseries, is_4d=False)
    >>> fig.show()

    Notes
    -----
    This function is a Python translation of the R function from the SOCR fMRI package.
    It applies detrending and kernel smoothing to visualize temporal patterns in fMRI data.
    """
    # Extract time series based on input type
    if is_4d:
        if voxel_location is None or len(voxel_location) != 3:
            raise ValueError("voxel_location must be provided as [x, y, z] for 4D data")

        x, y, z = voxel_location
        # Use 1-based indexing (subtract 1 for Python's 0-based indexing)
        realnum = np.real(fmridata[x-1, y-1, z-1, :])
        imgnum = np.imag(fmridata[x-1, y-1, z-1, :])
        phasenum = np.angle(fmridata[x-1, y-1, z-1, :])
        modnum = np.abs(fmridata[x-1, y-1, z-1, :])
    else:
        # 1D vector input
        fmridata = np.asarray(fmridata)
        realnum = np.real(fmridata)
        imgnum = np.imag(fmridata)
        phasenum = np.angle(fmridata)
        modnum = np.abs(fmridata)

    # Get time series length
    tlength = len(realnum)

    # Create breakpoints for detrending (matching R: seq(21, tlength, by=20))
    bp = list(range(21, tlength, 20)) if tlength > 21 else []

    # Process real component
    realnum1 = detrend(realnum, bp=bp) if bp else detrend(realnum)
    ksmthrealnum = _ksmooth(list(range(1, tlength + 1)), realnum1,
                            kernel="normal", bandwidth=5)
    ksthrealnum = np.column_stack([realnum1, ksmthrealnum['y']])
    TScore_realnum = _gtsplot(ksthrealnum, unit="time point",
                              ts_name=["real_original", "real_ksmooth"],
                              colors=["#FFCC33", "#00CCFF"])

    # Process imaginary component
    imgnum1 = detrend(imgnum, bp=bp) if bp else detrend(imgnum)
    ksmthimgnum = _ksmooth(list(range(1, tlength + 1)), imgnum1,
                           kernel="normal", bandwidth=5)
    ksthimgnum = np.column_stack([imgnum1, ksmthimgnum['y']])
    TScore_imgnum = _gtsplot(ksthimgnum, unit="time point",
                             ts_name=["img_original", "img_ksmooth"],
                             colors=["#FF9966", "#0099FF"])

    # Process phase component
    phasenum1 = detrend(phasenum, bp=bp) if bp else detrend(phasenum)
    ksmthphasenum = _ksmooth(list(range(1, tlength + 1)), phasenum1,
                             kernel="normal", bandwidth=5)
    ksthphasenum = np.column_stack([phasenum1, ksmthphasenum['y']])
    TScore_phasenum = _gtsplot(ksthphasenum, unit="time point",
                               ts_name=["phase_original", "phase_ksmooth"],
                               colors=["#FF6633", "#0066FF"])

    # Process magnitude component
    modnum1 = detrend(modnum, bp=bp) if bp else detrend(modnum)
    ksmthmodnum = _ksmooth(list(range(1, tlength + 1)), modnum1,
                           kernel="normal", bandwidth=5)
    ksthmodnum = np.column_stack([modnum1, ksmthmodnum['y']])
    TScore_modnum = _gtsplot(ksthmodnum, unit="time point",
                             ts_name=["mod_original", "mod_ksmooth"],
                             colors=["#CC3300", "#0033FF"])

    # Combine subplots
    if ref is None:
        # Create subplot with 4 rows
        result = make_subplots(
            rows=4, cols=1,
            subplot_titles=("Real", "Imaginary", "Phase", "Magnitude"),
            vertical_spacing=0.08
        )

        # Add traces from each component
        for trace in TScore_realnum.data:
            result.add_trace(trace, row=1, col=1)
        for trace in TScore_imgnum.data:
            result.add_trace(trace, row=2, col=1)
        for trace in TScore_phasenum.data:
            result.add_trace(trace, row=3, col=1)
        for trace in TScore_modnum.data:
            result.add_trace(trace, row=4, col=1)

        result.update_xaxes(title_text="time point", row=4, col=1)

    else:
        # Create subplot with 5 rows including reference
        result = make_subplots(
            rows=5, cols=1,
            subplot_titles=("Real", "Imaginary", "Phase", "Magnitude", "Reference"),
            vertical_spacing=0.06
        )

        # Add traces from each component
        for trace in TScore_realnum.data:
            result.add_trace(trace, row=1, col=1)
        for trace in TScore_imgnum.data:
            result.add_trace(trace, row=2, col=1)
        for trace in TScore_phasenum.data:
            result.add_trace(trace, row=3, col=1)
        for trace in TScore_modnum.data:
            result.add_trace(trace, row=4, col=1)

        # Add reference
        ref = np.asarray(ref)
        if np.iscomplexobj(ref):
            ref = np.abs(ref)
        x_ref = np.arange(1, len(ref) + 1)
        result.add_trace(
            go.Scatter(x=x_ref, y=ref, mode='lines', name='reference'),
            row=5, col=1
        )

        result.update_xaxes(title_text="time point", row=5, col=1)

    # Set height based on number of rows
    num_rows = 4 if ref is None else 5
    result.update_layout(
        height=300 * num_rows,
        showlegend=True,
        title_text="fMRI Time Series Analysis"
    )

    return result
