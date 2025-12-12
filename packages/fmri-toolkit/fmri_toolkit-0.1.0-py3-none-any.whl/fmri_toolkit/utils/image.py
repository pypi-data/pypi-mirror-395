from scipy import signal
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from kern_smooth import densCols
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from plotly.tools import mpl_to_plotly as ggplotly
from ..simulate import fmri_simulate_func
from plotnine import ggplot, aes, geom_vline,geom_hline,coord_cartesian
import numpy as _np
for _name, _alias in {
    "int": int,
    "float": float,
    "bool": bool,
    "complex": complex,
    "object": object,
    "str": str,
    "long": int,      # rarely used
}.items():
    if not hasattr(_np, _name):
        setattr(_np, _name, _alias)

def fmri_image(fmridata, option="manually", voxel_location=None, time=None):
    fig = make_subplots(rows=2, cols=2)

    if option == "manually":
        x, y, z = voxel_location
        t = time
    else:
        raise NotImplementedError("Use option='manually' in this snippet.")

    try1 = fmridata[x, y, z, :]
    try1 = signal.detrend(try1, bp=[a for a in range(21, 160, 20)])
    dates = list(range(1, len(try1) + 1))
    ts = pd.Series(try1, index=dates)
    ksmth = densCols(np.array(dates), ts.values, bandwidth=5)
    fig.add_trace(go.Scatter(y=ksmth, x=dates, name="ksmooth"), row=1, col=1)
    fig.add_trace(go.Scatter(y=ts.values, x=dates, name="original"), row=1, col=1)

    fmridata = np.array(fmridata)

    # ---- Z slice (row=1, col=2) ----
    zfmri = fmridata[:, :, z, t].T
    fig.add_trace(go.Contour(z=zfmri), row=1, col=2)
    fig.update_xaxes(range=[0, 64], row=1, col=2)
    fig.update_yaxes(range=[0, 64], row=1, col=2)
    # make units square here
    fig.update_yaxes(scaleanchor="x2", scaleratio=1, row=1, col=2)

    fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=40,
                  line=dict(color="RoyalBlue", width=3), row=1, col=2)
    fig.add_shape(type="line", y0=y, y1=y, x0=0, x1=64,
                  line=dict(color="RoyalBlue", width=3), row=1, col=2)

    # ---- X slice (row=2, col=1) ----
    xfmri = fmridata[x, :, :, t].T
    fig.add_trace(go.Contour(z=xfmri), row=2, col=1)
    fig.update_xaxes(range=[0, 64], row=2, col=1)
    fig.update_yaxes(range=[0, 40], row=2, col=1)
    # make units square here
    fig.update_yaxes(scaleanchor="x3", scaleratio=1, row=2, col=1)

    fig.add_shape(type="line", x0=z, x1=z, y0=0, y1=40,
                  line=dict(color="RoyalBlue", width=3), row=2, col=1)
    fig.add_shape(type="line", y0=y, y1=y, x0=0, x1=64,
                  line=dict(color="RoyalBlue", width=3), row=2, col=1)

    # ---- Y slice (row=2, col=2) ----
    yfmri = fmridata[:, y, :, t].T
    fig.add_trace(go.Contour(z=yfmri), row=2, col=2)
    fig.update_xaxes(range=[0, 64], row=2, col=2)
    fig.update_yaxes(range=[0, 40], row=2, col=2)
    # make units square here
    fig.update_yaxes(scaleanchor="x4", scaleratio=1, row=2, col=2)
    # --- top-right (row=1, col=2) ---
    fig.update_xaxes(range=[0, 64], constrain='domain', dtick=10, row=1, col=2)
    fig.update_yaxes(range=[0, 64], scaleanchor="x2", scaleratio=1, constrain='domain', dtick=10, row=1, col=2)

    # --- bottom-left (row=2, col=1) ---
    fig.update_xaxes(range=[0, 64], constrain='domain', dtick=10, row=2, col=1)
    fig.update_yaxes(range=[0, 40], scaleanchor="x3", scaleratio=1, constrain='domain', dtick=10, row=2, col=1)

    # --- bottom-right (row=2, col=2) ---
    fig.update_xaxes(range=[0, 64], constrain='domain', dtick=10, row=2, col=2)
    fig.update_yaxes(range=[0, 40], scaleanchor="x4", scaleratio=1, constrain='domain', dtick=10, row=2, col=2)

    return fig
