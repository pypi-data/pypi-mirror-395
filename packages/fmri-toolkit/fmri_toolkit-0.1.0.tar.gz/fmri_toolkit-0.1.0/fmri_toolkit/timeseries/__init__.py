"""Time series analysis and forecasting functions.

This module contains tools for analyzing and forecasting fMRI time series data.
"""

from .analysis import fmri_time_series
from .forecast import fmri_ts_forecast

__all__ = [
    "fmri_time_series",
    "fmri_ts_forecast",
]
