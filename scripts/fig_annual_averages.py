from __future__ import annotations

import matplotlib.pyplot as plt
import xarray as xr 
from sklearn.linear_model import LinearRegression

VARS = ['sst', 't2m0', 'ws10'] 
TITLES = ['Surface Sea Temperature', '2-metre Temperature', '10-metre Wind Speed'] 
COLOURS = ['blue', 'orange', 'green']


def plot_drift(
        ax: "Axes",
        data: xr.DataArray,
        title: str,
        colour: str,
        var_name: str,
    ) -> None:
    lin = LinearRegression()
    time = data.step.values
    X = time.astype("datetime64[D]").astype(float).reshape(-1, 1)
    y = data.values
    lin.fit(X, y)
    regression_line = lin.predict(X)
    slope = lin.coef_[0]
    ax.plot(time, data.values, '-', color=colour, alpha=0.7, markersize=4, label='Model Output')
    ax.plot(time, regression_line, '-', color='black', linewidth=2, 
            label=f'Drift: {slope[0]:.3e}')
    ax.set_title(f'{title}', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel(var_name)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')

def generate_annual_averages_plot(fig_name: str) -> None:
    atmos_global_averages = xr.open_zarr("gs://dlesym-storage/atmos_global_averages.zarr")
    ocean_global_averages = xr.open_zarr("gs://dlesym-storage/ocean_global_averages.zarr")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('DLESyM 100 year Variable Drift', fontsize=16, fontweight='bold')

    for i, (var_name, title, color, ax) in enumerate(zip(VARS, TITLES, COLOURS, axes)):
        if var_name == 'sst':
            data = ocean_global_averages[var_name]
        else:
            data = atmos_global_averages[var_name]
        
        plot_drift(ax, data, title, color, var_name)

    plt.tight_layout()
    plt.subplots_adjust(top=0.85) 
    plt.savefig(fig_name)