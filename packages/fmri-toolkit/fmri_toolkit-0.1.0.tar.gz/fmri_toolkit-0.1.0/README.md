# FMRI Toolkit

A comprehensive Python toolkit for functional Magnetic Resonance Imaging (fMRI) data analysis and visualization.

## Features

### Core Analysis
- **Stimulus Detection**: Multiple statistical tests for detecting brain activation
  - Real-valued tests: t-test, Wilcoxon, on/off difference, HRF GLM
  - Complex-valued tests: Hotelling's T², Wilks-Lambda, generalized LRT
  - Support for 1D-4D data
- **Post-hoc Processing**: FDR correction and spatial clustering (6-, 18-, or 26-connectivity)
- **P-value Adjustment**: Multiple testing correction methods (Bonferroni, Holm, Benjamini-Hochberg)

### Visualization
- **3D Brain Visualization**: Interactive 3D brain maps using Plotly
- **2D Slice Visualization**: Sagittal, axial, and coronal slice views
- **Regional Visualization**: ROI-based 3D visualization
- **Comparison Tools**: Side-by-side comparison of multiple p-value maps (2D and 3D)

### ROI Analysis
- **Phase 1**: Detect activated regions of interest using statistical tests
- **Phase 2**: ROI-based tensor-on-tensor regression analysis

### Time Series Analysis
- **Time Series Visualization**: Interactive time series exploration
- **Forecasting**: Time series forecasting capabilities for fMRI data

### Data Simulation
- Generate synthetic fMRI data with specified activation regions and stimulus timing

## Installation

### From PyPI (when published)
```bash
pip install fmri-toolkit
```

### From source
```bash
git clone https://github.com/yourusername/fmri-toolkit.git
cd fmri-toolkit
pip install -e .
```

## Quick Start

```python
import fmri_toolkit as fmri

# Load fMRI data
data = fmri.fmri_load_mat('path/to/data.mat')

# Perform stimulus detection
result = fmri.fmri_stimulus_detect(
    fmridata=data,
    mask=mask,
    stimulus_idx=stimulus_indices,
    rest_idx=rest_indices,
    method='t-test'
)

# Apply post-hoc correction
processed = fmri.fmri_post_hoc(
    result,
    alpha=0.05,
    method='BH',
    spatial_cluster=True
)

# Visualize results in 3D
fmri.fmri_3dvisual(
    processed,
    title='Brain Activation Map',
    color_scheme='hot'
)
```

## Requirements

- Python >= 3.8
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- Pandas >= 1.3.0
- Matplotlib >= 3.4.0
- Plotly >= 5.0.0
- And other dependencies (see `pyproject.toml`)

## Documentation

For detailed documentation, examples, and API reference, visit the [documentation](https://github.com/yourusername/fmri-toolkit#readme).

## Examples

Check the `examples/` directory for complete usage examples:
- `runall.py`: Full analysis pipeline demonstration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this toolkit in your research, please cite:

```bibtex
@software{fmri_toolkit,
  title={FMRI Toolkit: A Python Package for fMRI Data Analysis},
  author={Johnny In},
  year={2024},
  url={https://github.com/yourusername/fmri-toolkit}
}
```

## Support

For issues, questions, or suggestions, please open an issue on [GitHub](https://github.com/yourusername/fmri-toolkit/issues).
