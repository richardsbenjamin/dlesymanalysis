from __future__ import annotations

from netCDF4 import num2date
from pandas import to_datetime

from dlesymanalysis._typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dlesymanalysis._typing import Dataset


def get_annual_averages(dataset: Dataset) -> Dataset:
    annual_averages = (
        dataset.resample(step='YE')
        .mean(dim=['step', 'face', 'height', 'width'])
        .isel(step=slice(None, -1))
    )
    return annual_averages.compute()

def get_dataset_with_dates(dataset: Dataset, factor: float = 1000.0) -> Dataset:
    start_date = str(dataset["time"].values[0])
    dates = num2date(
        dataset.step.values / factor,
        units=f"microseconds since {start_date}",
        calendar='gregorian',
        only_use_cftime_datetimes=False,
    )
    return dataset.assign_coords(step=to_datetime(dates))

