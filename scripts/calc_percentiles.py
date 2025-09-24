from __future__ import annotations

import xarray as xr

from dlesymanalysis._typing import TYPE_CHECKING
from dlesymanalysis.utils.datasets import get_preprocessed
from dlesymanalysis.utils.parsers import get_calc_percentiles_parser

if TYPE_CHECKING:
    from dlesymanalysis._typing import Dataset, Namespace

PERCENTILES = [0.75, 0.90, 0.95, 0.99]

def get_quantiles(dataset: Dataset) -> Dataset:
    quantiles = dataset.groupby("step.dayofyear").quantile(PERCENTILES)
    return quantiles

def calc_percentiles(run_args: Namespace) -> None:
    ocean_ds = get_preprocessed(xr.open_zarr(run_args.ocean_store), "ocean")
    atmos_ds = get_preprocessed(xr.open_zarr(run_args.atmos_store), "atmos")

    ocean_quantiles = get_quantiles(ocean_ds)
    atmos_quantiles = get_quantiles(atmos_ds)

    ocean_quantiles.to_zarr(run_args.ocean_output, mode="w")
    atmos_quantiles.to_zarr(run_args.atmos_output, mode="w")

if __name__ == "__main__":
    run_args = get_calc_percentiles_parser()
    calc_percentiles(run_args)
