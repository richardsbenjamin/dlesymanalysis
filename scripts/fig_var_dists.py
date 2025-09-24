from __future__ import annotations

import gcsfs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from numpy import timedelta64

from dlesymanalysis._typing import TYPE_CHECKING
from dlesymanalysis.utils.datasets import get_preprocessed, read_edh
from dlesymanalysis.utils.parsers import get_fig_var_dists_parser

if TYPE_CHECKING:
    from dlesymanalysis._typing import Dataset, Namespace, ndarray

ERA5_VARS = ["sst", "u10", "v10", "t2m"]
VAR_UNITS_AND_LONG_NAMES = {
    "sst": ("degC", "Sea Surface Temperature"),
    "t2m": ("degC", "2m Temperature"),
    "ws": ("m/s", "Wind Speed")
}

def get_first_last_decade(ds: Dataset, var_name: str) -> tuple:
    da = ds[var_name]
    first_decade = da.sel(step=slice(da.step[0], da.step[0] + timedelta64(3652, 'D')))
    last_decade = da.sel(step=slice(da.step[-1] - timedelta64(3652, 'D'), da.step[-1]))
    return first_decade.values.flatten(), last_decade.values.flatten()

def plot_var_dists(
        axes: ndarray,
        model_first_decade: ndarray,
        model_last_decade: ndarray,
        era5: ndarray,
        var_name: str,
        decade1_str: str = "2017-2027",
        decade2_str: str = "2107-2117",
        era5_str: str = "2007-2017"
    ) -> None:
    unit = VAR_UNITS_AND_LONG_NAMES[var_name][0]
    long_name = VAR_UNITS_AND_LONG_NAMES[var_name][-1]
    x_title = f"{long_name} {unit}"

    axes[0].hist(model_first_decade, bins=100, alpha=0.5, density=True,
            color='blue', label=f"Decade: {decade1_str}")
    axes[0].hist(model_last_decade, bins=100, alpha=0.5, density=True,
            color='red', label=f"Decade: {decade2_str}")
    axes[0].legend()
    axes[0].set_title(f"DLESyM {long_name} First and Last Decades")
    axes[0].set_xlabel(x_title)
    axes[0].set_ylabel("Density")

    axes[1].hist(era5[~np.isnan(era5)], bins=100, alpha=0.5, density=True, color="blue", label=f"ERA5: {era5_str}")
    axes[1].legend()
    axes[1].set_title(f"ERA5 {var_name} 2007-2017", fontsize=12)
    axes[1].set_xlabel(x_title)

def get_fig_var_dists(run_args: Namespace) -> None:
    ocean_ds = xr.open_zarr(run_args.ocean_store)
    atmos_ds = xr.open_zarr(run_args.atmos_store)

    ocean_ds = get_preprocessed(ocean_ds, "ocean")
    atmos_ds = get_preprocessed(atmos_ds, "atmos")

    sst_decade1, sst_decade2 = get_first_last_decade(ocean_ds, "sst")
    t2m_decade1, t2m_decade2 = get_first_last_decade(atmos_ds, "t2m0")
    ws10_decade1, ws10_decade2 = get_first_last_decade(atmos_ds, "ws10")

    edh_singles = read_edh(run_args.singles_path)
    era5 = (
        edh_singles[ERA5_VARS]
        .sel(valid_time=slice("2007-01-01", "2017-01-01"))
        .isel(valid_time=slice(None, None, 48))
    )
    era5 = era5.chunk(valid_time=150, latitude=721, longitude=1440)
    era5_coarse = era5.coarsen(latitude=4, longitude=4, boundary='trim').mean()
    era5_sst_flat = era5_coarse["sst"].values.flatten()
    era5_t2m_flat = era5_coarse["t2m"].values.flatten()
    era5_u10 = era5_coarse["u10"]
    era5_v10 = era5_coarse["v10"]
    era5_ws = np.sqrt(era5_u10**2 + era5_v10**2)
    era5_ws_flat = era5_ws.values.flatten()

    fig, axes = plt.subplots(3, 2, figsize=(24, 15))
    fig.suptitle('DLESyM Decadal Distributions', fontsize=16, fontweight='bold')
    plt.subplots_adjust(top=0.95)
    plot_var_dists(axes[0], sst_decade1, sst_decade2, era5_sst_flat - 273.75, "sst")
    plot_var_dists(axes[1], t2m_decade1, t2m_decade2, era5_t2m_flat - 273.75, "t2m")
    plot_var_dists(axes[2], np.abs(ws10_decade1), np.abs(ws10_decade2), era5_ws_flat, "ws")

    fig.savefig("./var_hists.png")

    fs = gcsfs.GCSFileSystem()
    with fs.open(f"{run_args.fig_save_path}/var_hists.png", "wb") as f:
        fig.savefig(f, format="png")



if __name__ == "__main__":
    run_args = get_fig_var_dists_parser()
    get_fig_var_dists(run_args)
