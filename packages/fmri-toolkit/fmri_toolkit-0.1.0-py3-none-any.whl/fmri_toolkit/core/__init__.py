"""Core statistical analysis functions for fMRI data.

This module contains the main stimulus detection and post-hoc processing functions.
"""

from .stimulus_detect import fmri_stimulus_detect
from .stimulus_helper import (
    fmri_p_val,
    fmri_complex_p_val,
    fmri_hrf_p_val,
    fmri_on_off_volume,
)
from .post_hoc import fmri_post_hoc

__all__ = [
    "fmri_stimulus_detect",
    "fmri_p_val",
    "fmri_complex_p_val",
    "fmri_hrf_p_val",
    "fmri_on_off_volume",
    "fmri_post_hoc",
]
