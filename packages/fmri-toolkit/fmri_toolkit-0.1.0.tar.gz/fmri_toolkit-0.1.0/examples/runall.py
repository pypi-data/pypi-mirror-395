import scipy.io as sio
import numpy as np
import pyreadr
import pandas as pd
import xarray as xr
from scipy.ndimage import gaussian_filter
from fmri_toolkit.utils.image import fmri_image
from fmri_toolkit.timeseries.analysis import fmri_time_series
from fmri_toolkit.timeseries.forecast import fmri_ts_forecast
from fmri_toolkit.simulate import fmri_simulate_func
from fmri_toolkit.core.stimulus_detect import fmri_stimulus_detect
from fmri_toolkit.core.post_hoc import fmri_post_hoc
from fmri_toolkit.visualization.visual_3d import fmri_3dvisual
from fmri_toolkit.visualization.visual_2d import fmri_2dvisual
from fmri_toolkit.visualization.comparison_3d import fmri_pval_comparison_3d
from fmri_toolkit.visualization.comparison_2d import fmri_pval_comparison_2d
from fmri_toolkit.roi.phase1 import fmri_ROI_phase1
from fmri_toolkit.roi.phase2 import fmri_ROI_phase2
from fmri_toolkit.visualization.visual_3d_region import fmri_3dvisual_region

mat = sio.loadmat("./test_data/subj1_run1_complex_all.mat")
bigim1 = mat["bigim"][:, ::-1, :, :]   
bigim1_mod = np.abs(bigim1) 
smoothmod = gaussian_filter(bigim1_mod, sigma=(1, 1, 1, 0), mode="nearest")
result = pyreadr.read_r("./test_data/mask.rda")
mask = result[list(result.keys())[0]]  # extract the first object
res_mask = pyreadr.read_r("./test_data/mask.rda")
mask_obj = next(iter(res_mask.values()))
mask = mask_obj.values if isinstance(mask_obj, xr.DataArray) else np.asarray(mask_obj)
mask = mask.astype(bool)  # shape should match (X,Y,Z) of your data
result = pyreadr.read_r("./test_data/hemody.rda")
hemody = result[list(result.keys())[0]]
result_label = pyreadr.read_r("./test_data/mask_label.rda")
mask_label = next(iter(result_label.values()))
result_dict = pyreadr.read_r("./test_data/mask_dict.rda")
mask_dict = next(iter(result_dict.values()))   # should be a pandas.DataFrame
label_index = mask_dict["index"].to_numpy()
label_name = mask_dict["name"].astype(str).to_numpy()
label_mask = mask_label



# 5.1 fmri_image
# fmri_image(bigim1_mod,"manually",[40,40,30],time=4)

# 5.2 fMRI Time Series Visualization
# # Visualize time series for a specific voxel (with complex data)
# fig = fmri_time_series(bigim1, voxel_location=[20, 30, 20], is_4d=True)
# fig.show()
#
# # With reference signal
# reference_signal = bigim1[10, 20, 30, :]
# fig = fmri_time_series(bigim1, voxel_location=[20, 30, 20], is_4d=True, ref=reference_signal)
# fig.show()

# 5.3 Forecasting with time series
# fig = fmri_ts_forecast(smoothmod,[20,30,20])
# fig.show()

#6.1 fMRI data simulation
# fmri_generate = fmri_simulate_func(dim_data = [64, 64, 40], mask = mask, 
#                                    ons = [1, 21, 41, 61, 81, 101, 121, 141], 
#                                    dur = [10, 10, 10, 10, 10, 10, 10, 10])

# #6.2 Stimulus detection
# #6.2.1 Examples
# T = bigim1_mod.shape[-1]  # 160
# pattern = np.r_[np.ones(10, bool), np.zeros(10, bool)]
# stimulus_idx = np.tile(pattern, T // pattern.size)[:T]

# p_val1 = fmri_stimulus_detect(
#     fmridata=bigim1_mod,
#     mask = mask,
#     stimulus_idx=stimulus_idx,
#     method="HRF",
#     ons=[1,21,41,61,81,101,121,141],
#     dur=[10,10,10,10,10,10,10,10],
#     )
# # print(p_val1.min(), p_val1.max(), p_val1.mean())

# p_val2 = fmri_stimulus_detect(
#     fmridata=bigim1_mod,
#     mask = mask,
#     stimulus_idx=stimulus_idx,
#     method="t-test",
#     )
# print(p_val2.min(), p_val2.max(), p_val2.mean())

# p_val3 = fmri_stimulus_detect(
#     fmridata=bigim1,
#     mask = mask,
#     stimulus_idx=stimulus_idx,
#     method="Wilks-Lambda",
#     )
# print(p_val3.min(), p_val3.max(), p_val3.mean())

# p_val4 = fmri_post_hoc(p_val1, fdr_corr="fdr", spatial_cluster_thr=0.05, spatial_cluster_size=5, show_comparison=False)
# print(p_val4.min(), p_val4.max(), p_val4.mean())

# #7 Motor area visualization
# #7.1 Visualization and comparison of p-value
# #7.1.1 3D visualization for p-value

# pval1_3d = fmri_3dvisual(
#     p_val1, mask,
#     p_threshold=0.05,
#     method="scale_p",
#     multi_pranges=True,              # TRUE -> True in Python
#     title="Accounting for HRF"
# )

# fig = pval1_3d["fig"]
# fig.show()

# pval4_3d = fmri_3dvisual(
#     p_val4, mask,
#     p_threshold=0.05,
#     method="scale_p",
#     multi_pranges=True,              # TRUE -> True in Python
#     title="Accounting for HRF"
# )

# fig = pval4_3d["fig"]
# fig.show()

# # 7.1.2 2D visualization for p-value
# one_minus_p_3d = 1.0 - p_val1

# # keep only voxels with p <= 0.05
# p_threshold = 0.05
# keep_mask = one_minus_p_3d >= (1.0 - p_threshold)   # True where p <= 0.05

# idx0 = 35 - 1

# omp2d = one_minus_p_3d[idx0, :, :]      # shape (Y, Z)
# mask2d = mask[idx0, :, :]
# xs = np.arange(1, omp2d.shape[0] + 1)   # y axis in the R plot's x-label
# ys = np.arange(1, omp2d.shape[1] + 1)   # z axis in the R plot's y-label
# fig = fmri_2dvisual(
#     omp2d=omp2d, mask2d=mask2d, p_threshold=0.05,
#     multi_pranges=True, color_pal="YlOrRd",
#     title=f"Sagittal View of Brain for x={35}",
#     xlabel="y", ylabel="z",
#     xs=xs, ys=ys, legend_show=True, mask_width=1.5, hemody2d=None,
# )
# fig.show()

# idx1 = 30 - 1

# omp2d = one_minus_p_3d[:, idx1, :]      # shape (Y, Z)
# mask2d = mask[:, idx1, :]
# xs = np.arange(1, omp2d.shape[0] + 1)   # y axis in the R plot's x-label
# ys = np.arange(1, omp2d.shape[1] + 1)   # z axis in the R plot's y-label
# fig = fmri_2dvisual(
#     omp2d=omp2d, mask2d=mask2d, p_threshold=0.05,
#     multi_pranges=True, color_pal="YlOrRd",
#     title=f"Sagittal View of Brain for y={30}",
#     xlabel="x", ylabel="z",
#     xs=xs, ys=ys, legend_show=True, mask_width=1.5, hemody2d=None,
# )
# fig.show()

# idx2 = 22-1

# omp2d = one_minus_p_3d[:, :, idx2]      # shape (Y, Z)
# mask2d = mask[:, :, idx2]
# xs = np.arange(1, omp2d.shape[0] + 1)   # y axis in the R plot's x-label
# ys = np.arange(1, omp2d.shape[1] + 1)   # z axis in the R plot's y-label
# fig = fmri_2dvisual(
#     omp2d=omp2d, mask2d=mask2d, p_threshold=0.05,
#     multi_pranges=True, color_pal="YlOrRd",
#     title=f"Sagittal View of Brain for z={22}",
#     xlabel="x", ylabel="y",
#     xs=xs, ys=ys, legend_show=True, mask_width=1.5,
#     hemody2d=None,
# )
# fig.show()

# idx0 = 35 - 1

# omp2d = one_minus_p_3d[idx0, :, :]      # shape (Y, Z)
# mask2d = mask[idx0, :, :]
# hemody2d = hemody[idx0, :, :]
# xs = np.arange(1, omp2d.shape[0] + 1)   # y axis in the R plot's x-label
# ys = np.arange(1, omp2d.shape[1] + 1)   # z axis in the R plot's y-label
# fig = fmri_2dvisual(
#     omp2d=omp2d, mask2d=mask2d, p_threshold=0.05,
#     multi_pranges=True, color_pal="YlOrRd",
#     title=f"Sagittal View of Brain for x={35}",
#     xlabel="y", ylabel="z",
#     xs=xs, ys=ys, legend_show=True, mask_width=1.5, hemody2d=hemody2d,
# )
# fig.show()

# idx1 = 30 - 1

# omp2d = one_minus_p_3d[:, idx1, :]      # shape (Y, Z)
# mask2d = mask[:, idx1, :]
# hemody2d = hemody[:, idx1, :]
# xs = np.arange(1, omp2d.shape[0] + 1)   # y axis in the R plot's x-label
# ys = np.arange(1, omp2d.shape[1] + 1)   # z axis in the R plot's y-label
# fig = fmri_2dvisual(
#     omp2d=omp2d, mask2d=mask2d, p_threshold=0.05,
#     multi_pranges=True, color_pal="YlOrRd",
#     title=f"Sagittal View of Brain for y={30}",
#     xlabel="x", ylabel="z",
#     xs=xs, ys=ys, legend_show=True, mask_width=1.5, hemody2d=hemody2d,
# )
# fig.show()

# idx2 = 22-1

# omp2d = one_minus_p_3d[:, :, idx2]      # shape (Y, Z)
# mask2d = mask[:, :, idx2]
# hemody2d = hemody[:, :, idx2]
# xs = np.arange(1, omp2d.shape[0] + 1)   # y axis in the R plot's x-label
# ys = np.arange(1, omp2d.shape[1] + 1)   # z axis in the R plot's y-label
# fig = fmri_2dvisual(
#     omp2d=omp2d, mask2d=mask2d, p_threshold=0.05,
#     multi_pranges=True, color_pal="YlOrRd",
#     title=f"Sagittal View of Brain for z={22}",
#     xlabel="x", ylabel="y",
#     xs=xs, ys=ys, legend_show=True, mask_width=1.5,
#     hemody2d=hemody2d,
# )
# fig.show()

# #7.2.1 3D p-value comparison
# res_cmp = fmri_pval_comparison_3d(
#     pval_3d_ls=[p_val1, p_val2],
#     mask=mask,
#     p_threshold_ls=[0.05, 0.05],
#     method_ls=["scale_p", "scale_p"],
#     color_pal_ls=("YlOrRd", "YlGnBu"),   # different palettes
#     multi_pranges=False,                  # match R's FALSE
#     titles=("Map 1", "Map 2")
# )
# fig = res_cmp["fig"]
# fig.show()

# #7.2.2 2D p-value comparison

# fig = fmri_pval_comparison_2d(
#     pval_ls=[p_val2, p_val1],
#     pval_name_ls=["t-test", "HRF"],
#     axis_i_lses=[[35, 33, 22], [40, 26, 33]],
#     hemody_data=None,
#     mask=mask,
#     p_threshold=0.05,
#     legend_show=False,
#     method="scale_p",
#     color_pal="YlOrRd_r",
#     multi_pranges=False,
# )

# fig.show()

#8 Tri-phase ROI-based Spacekime Analytics

# 8.1 Phase 1: Detect Potential Activated ROI

# Reproduce c(1:160)[rep(c(TRUE,FALSE), c(10,10))]
# Pattern: 10 ON, 10 OFF, repeated over 160 time points
pattern = np.tile(np.r_[np.ones(10, dtype=bool), np.zeros(10, dtype=bool)], 8)  # length 160
r_indices = np.arange(1, 161)          # 1..160 like in R
stimulus_idx = r_indices[pattern] - 1  # convert to 0-based indices for Python

phase1_pval = fmri_ROI_phase1(
    fmridata=bigim1_mod,
    label_mask=mask_label,
    label_dict=mask_dict,
    stimulus_idx=stimulus_idx
)

# print("phase1_pval shape:", np.asarray(phase1_pval).shape)

#8.2 Phase 2: ROI-Based Tensor-on-Tensor Regression

# stimulus_idx = np.array([0, 20, 40, 60, 80, 100, 120, 140], dtype=int)

# stimulus_dur = np.array([10] * 8, dtype=int)

# phase2_pval = fmri_ROI_phase2(
#     fmridata=bigim1_mod,
#     label_mask=mask_label,
#     label_dict=mask_dict,
#     stimulus_idx=stimulus_idx,
#     stimulus_dur=stimulus_dur,
#     rrr_rank=3,
#     fmri_design_order=2,
#     fmri_stimulus_TR=3,
#     method="t_test",
# )


#8.3 Phase 3: FDR Correction and Spatial Clustering
# phase3_pval = fmri_post_hoc(p_val1, fdr_corr="fdr", spatial_cluster_thr=0.05, spatial_cluster_size=5, show_comparison=False)


# 8.4 3D visualization based on the activated areas by regions
fig = fmri_3dvisual_region(
    pval=phase1_pval,      # TCIU::phase1_pval in R
    mask=label_mask,
    label_index=label_index,
    label_name=label_name,
    title="Phase 1 p-values",
    rank="value",
)

fig.show()


