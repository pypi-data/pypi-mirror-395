import pytest
from generic_exporters.dataset import Dataset
from generic_exporters.timeseries import TimeSeries

from tests.fixtures import *

@pytest.mark.asyncio
async def test_dataset_init(time_series):
    dataset = Dataset(time_series)
    assert dataset._data == time_series

@pytest.mark.asyncio
async def test_dataset_not_implemented_methods(time_series):
    dataset = Dataset(time_series)

    with pytest.raises(NotImplementedError):
        dataset.plot()

    with pytest.raises(NotImplementedError):
        dataset.to_csv()

    with pytest.raises(NotImplementedError):
        dataset.export(None)