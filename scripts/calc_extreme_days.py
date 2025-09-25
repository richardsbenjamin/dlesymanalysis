from __future__ import annotations

import xarray as xr

from dlesymanalysis._typing import TYPE_CHECKING
from dlesymanalysis.utils.datasets import get_preprocessed
from dlesymanalysis.utils.parsers import get_calc_extreme_days_parser_args

if TYPE_CHECKING:
    from dlesymanalysis._typing import Dataset, Namespace

def detect_extreme_days(
        quantiles: Dataset,
        predictions: Dataset,
    ) -> Dataset:

    def compare_with_threshold(pred_group):
        dayofyear_val = pred_group.step.dt.dayofyear.values[0]
        threshold_val = quantiles.sel(dayofyear=dayofyear_val)
        return pred_group > threshold_val

    extreme_days = predictions.groupby('step.dayofyear').map(compare_with_threshold)
    extreme_days_per_year = extreme_days.resample(step='YE').sum()
    return extreme_days_per_year

def calc_extreme_days(run_args: Namespace) -> None:
    ocean_ds = get_preprocessed(xr.open_zarr(run_args.ocean_store), "ocean")
    atmos_ds = get_preprocessed(xr.open_zarr(run_args.atmos_store), "atmos")

    ocean_percentiles = xr.open_zarr(run_args.ocean_quantiles_path)
    atmos_percentiles = xr.open_zarr(run_args.atmos_quantiles_path)

    ocean_extremes = detect_extreme_days(ocean_percentiles, ocean_ds)
    atmos_extremes = detect_extreme_days(atmos_percentiles, atmos_ds)

    ocean_extremes.to_zarr(run_args.ocean_output, mode="w")
    atmos_extremes.to_zarr(run_args.atmos_output, mode="w")

if __name__ == "__main__":
    run_args = get_calc_extreme_days_parser_args()
    calc_extreme_days(run_args)
