from __future__ import annotations

import numpy as np
import xarray as xr
from scipy.stats import linregress

from dlesymanalysis._typing import TYPE_CHECKING
from dlesymanalysis.utils.datasets import get_dataset_with_dates
from dlesymanalysis.utils.parsers import get_spatial_lin_regress_parser

if TYPE_CHECKING:
    from dlesymanalysis._typing import Namespace

# For this script we need to chunk the data spatially
# rather than temporally
OCEAN_CHUNK_DICT = {"time": -1, "step": -1, "face": 6, "height": 32, "width": 32}
ATMOS_CHUNK_DICT = {"time": -1, "step": -1, "face": 6, "height": 16, "width": 16}

def run_spatial_lin_regress(run_args: Namespace) -> None:
    ocean_ds = xr.open_zarr(run_args.ocean_store)
    atmos_ds = xr.open_zarr(run_args.atmos_store)

    ocean_ds = get_dataset_with_dates(ocean_ds)
    atmos_ds = get_dataset_with_dates(atmos_ds)

    ocean_ds = ocean_ds.chunk(OCEAN_CHUNK_DICT)
    atmos_ds = atmos_ds.chunk(ATMOS_CHUNK_DICT)

    def calc_trend(y, time_in_years):
        if np.isnan(y).all():
            return np.nan
        try:
            slope, _, _, _, _ = linregress(time_in_years, y)
        except:
            return np.nan
        return slope
    
    ocean_time_in_years = ocean_ds.step.dt.year + ocean_ds.step.dt.dayofyear / 365.25
    atmos_time_in_years = atmos_ds.step.dt.year + atmos_ds.step.dt.dayofyear / 365.25

    ocean_trend_slope = xr.apply_ufunc(
        lambda x: calc_trend(x, ocean_time_in_years),           
        ocean_ds,                  
        input_core_dims=[['step']], 
        output_core_dims=[[]],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[float]
    )
    ocean_trend_slope_computed = ocean_trend_slope.compute()
    ocean_trend_slope_computed.to_zarr(run_args.ocean_output, mode="w")

    atmos_trend_slope = xr.apply_ufunc(
        lambda x: calc_trend(x, atmos_time_in_years),           
        ocean_ds,                  
        input_core_dims=[['step']], 
        output_core_dims=[[]],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[float]
    )
    atmos_trend_slope_computed = atmos_trend_slope.compute()
    atmos_trend_slope_computed.to_zarr(run_args.atmos_output, mode="w")


if __name__ == "__main__":
    run_args = get_spatial_lin_regress_parser()
    run_spatial_lin_regress(run_args)
