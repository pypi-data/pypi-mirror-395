"""FMRI Toolkit - A comprehensive toolkit for fMRI data analysis and visualization.

This package provides tools for:
- fMRI stimulus detection and statistical analysis
- Post-hoc processing (FDR correction, spatial clustering)
- 2D and 3D brain visualization
- ROI (Region of Interest) analysis
- Time series analysis and forecasting
- fMRI data simulation
"""

__version__ = "0.1.0"
__author__ = "Johnny In"
__email__ = "johnnyin@umich.edu"

# Import main functions for convenient access
from .core.stimulus_detect import fmri_stimulus_detect
from .core.post_hoc import fmri_post_hoc
from .visualization.visual_3d import fmri_3dvisual
from .visualization.visual_2d import fmri_2dvisual
from .simulate import fmri_simulate_func
from .utils.image import fmri_image
from .timeseries.analysis import fmri_time_series
from .timeseries.forecast import fmri_ts_forecast

__all__ = [
    "fmri_stimulus_detect",
    "fmri_post_hoc",
    "fmri_3dvisual",
    "fmri_2dvisual",
    "fmri_simulate_func",
    "fmri_image",
    "fmri_time_series",
    "fmri_ts_forecast",
]
