from __future__ import annotations

import xarray as xr

from dlesymanalysis._typing import TYPE_CHECKING
from dlesymanalysis.utils.datasets import get_annual_averages, get_dataset_with_dates
from dlesymanalysis.utils.parsers import get_calc_avgs_parser

if TYPE_CHECKING:
    from dlesymanalysis._typing import Dataset, Namespace


def get_annual_averages(dataset: Dataset) -> Dataset:
    annual_averages = (
        dataset.resample(step='YE')
        .mean(dim=['step', 'face', 'height', 'width'])
        .isel(step=slice(None, -1))
    )
    return annual_averages.compute()

def calc_annual_averages(run_args: Namespace) -> None:
    ocean_ds = xr.open_zarr(run_args.ocean_store)
    atmos_ds = xr.open_zarr(run_args.atmos_store)

    # Need to convert the steps dimension to actualy datetimes
    ocean_ds = get_dataset_with_dates(ocean_ds)
    atmos_ds = get_dataset_with_dates(atmos_ds)

    ocean_averages = get_annual_averages(ocean_ds)
    atmos_averages = get_annual_averages(atmos_ds)

    ocean_averages.to_zarr(run_args.ocean_output)
    atmos_averages.to_zarr(run_args.atmos_output)


if __name__ == "__main__":
    run_args = get_calc_avgs_parser()
    calc_annual_averages(run_args)
