
from datetime import datetime, timedelta
from decimal import Decimal

from generic_exporters import Metric, TimeSeries, QueryPlan, WideTimeSeries
from generic_exporters.processors.exporters.datastores.timeseries._base import TimeSeriesDataStoreBase

import pytest


class DummyMetric(Metric):
    async def produce(self, timestamp: datetime) -> Decimal:
        return Decimal(10)
    @property
    def key(self) -> str:
        return "dummy_metric"

class DummyDataStore(TimeSeriesDataStoreBase):
    async def data_exists(self, key, ts):
        return True

    async def push(self, key, ts, data):
        pass

@pytest.fixture
def dummy_metric():
    return DummyMetric()

@pytest.fixture
def time_series(dummy_metric):
    return TimeSeries(dummy_metric)

@pytest.fixture
def wide_time_series(dummy_metric):
    return WideTimeSeries(dummy_metric, dummy_metric)

@pytest.fixture
def query_plan(time_series):
    start_timestamp = datetime.utcnow() - timedelta(days=1)
    end_timestamp = datetime.utcnow()
    interval = timedelta(minutes=1)
    return QueryPlan(time_series, start_timestamp, end_timestamp, interval)
    
@pytest.fixture
def dummy_data_store():
    return DummyDataStore()