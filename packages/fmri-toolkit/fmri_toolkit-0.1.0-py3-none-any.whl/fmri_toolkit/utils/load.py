# --- Dependencies ---
# pip install numpy scipy pyreadr
import numpy as np
import scipy.io as sio
from scipy.ndimage import gaussian_filter
import pyreadr

# ---------- 1) Load the complex fMRI .mat ----------
# R: mat1 = readMat("./test_data/subj1_run1_complex_all.mat")
mat = sio.loadmat("./test_data/subj1_run1_complex_all.mat")

# R: bigim1 = mat1$bigim[,64:1,,]
#    -> flip the 2nd (Y) dimension like 64:1
bigim1 = mat["bigim"][:, ::-1, :, :]          # shape: (64, 64, 40, 160), complex128

# R comments:
# dim(bigim1) = 64 64 40
# bigim1 contains the complex image space
# dimensions are 64x*64y*40z*160t, corresponding to x,y,z,time

# ---------- 2) Complex modulus & spatial smoothing ----------
# R: bigim1_mod = Mod(bigim1)  # Modulus
bigim1_mod = np.abs(bigim1)    # (64, 64, 40, 160), float

# R: smoothmod = GaussSmoothArray(bigim1_mod, sigma = diag(3,3))
# Interpret sigma=diag(3,3) as ~3 voxels in X,Y,Z, and 0 along time (no temporal smoothing)
smoothmod = gaussian_filter(bigim1_mod, sigma=(3, 3, 3, 0), mode="nearest")

