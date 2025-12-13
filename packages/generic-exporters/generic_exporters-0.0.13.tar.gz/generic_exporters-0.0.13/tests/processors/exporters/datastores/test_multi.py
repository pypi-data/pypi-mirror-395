import pytest
from generic_exporters.processors.exporters.datastores.timeseries.multi import TimeSeriesMultiDataStore

from tests.fixtures import *


def test_time_series_multi_data_store_initialization(dummy_data_store):
    multi_data_store = TimeSeriesMultiDataStore(dummy_data_store, dummy_data_store)
    assert dummy_data_store in multi_data_store.datastores

@pytest.mark.asyncio
async def test_time_series_multi_data_store_methods(dummy_data_store):
    multi_data_store = TimeSeriesMultiDataStore(dummy_data_store, dummy_data_store)
    key = 'test_key'
    ts = datetime.utcnow()
    data = Decimal(10)
    exists = await multi_data_store.data_exists(key, ts)
    assert exists is True
    await multi_data_store.push(key, ts, data)  # No assert needed, just checking for exceptions