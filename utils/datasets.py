from __future__ import annotations

import xarray as xr
from netCDF4 import num2date
from pandas import to_datetime

from dlesymanalysis._typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dlesymanalysis._typing import Dataset

CHUNKS = {
    "ocean": {"time": -1, "step": -1, "face": 6, "height": 32, "width": 32},
    "atmos": {"time": -1, "step": -1, "face": 6, "height": 16, "width": 16},
}


def get_dataset_with_dates(dataset: Dataset, factor: float = 1000.0) -> Dataset:
    start_date = str(dataset["time"].values[0])
    dates = num2date(
        dataset.step.values / factor,
        units=f"microseconds since {start_date}",
        calendar='gregorian',
        only_use_cftime_datetimes=False,
    )
    return dataset.assign_coords(step=to_datetime(dates))

def get_preprocessed(dataset: Dataset, type_: str) -> Dataset:
    dataset = get_dataset_with_dates(dataset)
    dataset = dataset.chunk(CHUNKS[type_])
    return dataset

def read_edh(edh_path: str) -> Dataset:
    return xr.open_dataset(
        edh_path,
        storage_options={"client_kwargs":{"trust_env":True}},
        chunks={"time": 1},
        engine="zarr",
    )
