from __future__ import annotations

import xarray as xr

from dlesymanalysis._typing import TYPE_CHECKING
from dlesymanalysis.utils.parsers import get_stats_calc_parse_args

if TYPE_CHECKING:
    from dlesymanalysis._typing import Dataset, Namespace

# For this script we need to chunk the data spatially
# rather than temporally
OCEAN_CHUNK_DICT = {"time": -1, "step": -1, "face": 6, "height": 32, "width": 32}
ATMOS_CHUNK_DICT = {"time": -1, "step": -1, "face": 6, "height": 16, "width": 16}

QUANTILES = [0.75, 0.90, 0.95, 0.99]

def get_stats(ds: Dataset, qs: list[float] = QUANTILES) -> Dataset:
    ds_array = ds.to_array()
    reduce_dims = [d for d in ds_array.dims if d != "variable"]
    stats = xr.Dataset({
        "mean": ds_array.mean(dim=reduce_dims),
        "min": ds_array.min(dim=reduce_dims),
        "max": ds_array.max(dim=reduce_dims),
        "median": ds_array.median(dim=reduce_dims),
        "std": ds_array.std(dim=reduce_dims),
    })
    quantiles = ds_array.quantile(q=qs, dim=reduce_dims)
    for q in qs:
        stats[f"q{int(q*100)}"] = quantiles.sel(quantile=q)
    return stats.compute()

def run_stats_calc(run_args: Namespace) -> None:
    ocean_ds = xr.open_zarr(run_args.ocean_store)
    atmos_ds = xr.open_zarr(run_args.atmos_store)

    ocean_ds = ocean_ds.chunk(OCEAN_CHUNK_DICT)
    atmos_ds = atmos_ds.chunk(ATMOS_CHUNK_DICT)

    ocean_stats = get_stats(ocean_ds)
    atmos_stats = get_stats(atmos_ds)

    ocean_stats.to_zarr(run_args.ocean_output)
    atmos_stats.to_zarr(run_args.atmos_output)

if __name__ == "__main__":
    run_args = get_stats_calc_parse_args()
    run_stats_calc(run_args)
