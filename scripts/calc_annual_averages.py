from __future__ import annotations

import xarray as xr

from dlesymanalysis._typing import TYPE_CHECKING
from dlesymanalysis.utils.datasets import get_annual_averages, get_dataset_with_dates
from dlesymanalysis.utils.parsers import get_calc_avgs_parser

if TYPE_CHECKING:
    from dlesymanalysis._typing import Namespace


def calc_annual_averages(run_args: Namespace) -> None:
    ocean_ds = xr.open_zarr(run_args.ocean_store)
    atmos_ds = xr.open_zarr(run_args.atmos_store)

    ocean_with_dates = get_dataset_with_dates(ocean_ds)
    atmos_with_dates = get_dataset_with_dates(atmos_ds)

    ocean_averages = get_annual_averages(ocean_with_dates)
    atmos_averages = get_annual_averages(atmos_with_dates)

    ocean_averages.to_zarr(run_args.ocean_output)
    atmos_averages.to_zarr(run_args.atmos_output)


if __name__ == "__main__":
    run_args = get_calc_avgs_parser()
    calc_annual_averages(run_args)
