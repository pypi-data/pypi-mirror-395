import numpy as np
from scipy import signal
import plotly.graph_objects as go

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller


def _suggest_d(y, max_d=2):
    """Pick differencing order d via ADF: keep differencing until stationary or max_d."""
    d = 0
    y_curr = np.asarray(y, dtype=float)
    for _ in range(max_d + 1):
        try:
            pval = adfuller(y_curr, autolag="AIC")[1]
        except Exception:
            return d
        if pval < 0.05:  # stationary
            return d
        if d < max_d:
            y_curr = np.diff(y_curr)
            d += 1
    return d


def _select_arima_order(y, max_p=3, max_q=3, d=None):
    """Tiny AIC grid search for SARIMAX(p,d,q) on a univariate series."""
    y = np.asarray(y, dtype=float)
    if d is None:
        d = _suggest_d(y)

    best = {"aic": np.inf, "order": None, "res": None}
    for p in range(max_p + 1):
        for q in range(max_q + 1):
            if p == 0 and d == 0 and q == 0:
                continue
            try:
                m = SARIMAX(y, order=(p, d, q),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
                res = m.fit(disp=False)
                if res.aic < best["aic"]:
                    best = {"aic": res.aic, "order": (p, d, q), "res": res}
            except Exception:
                continue

    if best["res"] is None:
        # conservative fallback
        m = SARIMAX(y, order=(1, 1, 0),
                    enforce_stationarity=False,
                    enforce_invertibility=False)
        best["res"] = m.fit(disp=False)
        best["order"] = (1, 1, 0)
    return best["res"], best["order"]


def fmri_ts_forecast(fmridata, voxel_location, cut=10):
    """
    Forecast an fMRI voxel time series with ARIMA (statsmodels) and plot the result.

    Parameters
    ----------
    fmridata : ndarray, shape (X, Y, Z, T)
        4D fMRI magnitude data.
    voxel_location : tuple/list of 3 ints
        (i, j, k) indices of the voxel.
    cut : int
        Spacing for piecewise-detrend breakpoints; R's seq(21, N, by=cut).

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plot with train/test, forecast mean, and 80%/95% confidence bands.
    """
    # 1) Extract series
    i, j, k = voxel_location
    fdata = np.asarray(fmridata[i, j, k, :], dtype=float)
    N = fdata.shape[0]

    # 2) Piecewise linear detrend with breakpoints ~ seq(21, N, by=cut)
    if cut is not None and cut > 0:
        bp = [b for b in range(21, N, cut) if 0 < b < N - 1] or None
    else:
        bp = None
    y = signal.detrend(fdata, bp=bp)

    # 3) Train/test split (80/20 like the R code)
    trainsize = int(np.floor(N * 0.8))
    y_train = y[:trainsize]
    y_test = y[trainsize:]
    t_train = np.arange(1, trainsize + 1)              # 1-based feel (cosmetic)
    t_test = np.arange(trainsize + 1, N + 1)

    # 4) Fit ARIMA via small AIC grid search
    res, order = _select_arima_order(y_train, max_p=3, max_q=3, d=None)

    # 5) Forecast the remaining horizon (multi-step to match R's auto.arima+forecast)
    steps = len(y_test)
    fc = res.get_forecast(steps=steps)
    pred_mean = np.asarray(fc.predicted_mean)
    conf95 = np.asarray(fc.conf_int(alpha=0.05))   # (steps, 2)
    conf80 = np.asarray(fc.conf_int(alpha=0.20))

    # 6) Plot (TSplot-style)
    fig = go.Figure(layout=dict(
        title=f"Forecast (SARIMAX{order}) at voxel {tuple(voxel_location)}",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Value"),
        margin=dict(l=60, r=10, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    ))

    # train
    fig.add_trace(go.Scatter(x=t_train, y=y_train, mode="lines",
                             name="train (observed)", line=dict(width=2, color="green")))
    # test (truth)
    fig.add_trace(go.Scatter(x=t_test, y=y_test, mode="lines",
                             name="test (true)", line=dict(width=2, color="gray")))
    # forecast mean
    fig.add_trace(go.Scatter(x=t_test, y=pred_mean, mode="lines",
                             name="forecast (ARIMA)", line=dict(width=3, color="red")))

    # 95% band (draw first)
    fig.add_trace(go.Scatter(x=t_test, y=conf95[:, 1], mode="lines",
                             line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=t_test, y=conf95[:, 0], mode="lines", fill="tonexty",
                             name="95% CI", line=dict(width=0), hoverinfo="skip",
                             fillcolor="rgba(100,149,237,0.35)"))

    # 80% band (on top)
    fig.add_trace(go.Scatter(x=t_test, y=conf80[:, 1], mode="lines",
                             line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=t_test, y=conf80[:, 0], mode="lines", fill="tonexty",
                             name="80% CI", line=dict(width=0), hoverinfo="skip",
                             fillcolor="rgba(255,99,132,0.30)"))

    return fig
