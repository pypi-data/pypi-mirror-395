import pytest
from datetime import datetime, timedelta
from generic_exporters.dataset import Dataset
from generic_exporters.plan import QueryPlan, TimeDataRow
from generic_exporters.timeseries import TimeSeries

from tests.fixtures import *


@pytest.mark.asyncio
async def test_query_plan_initialization(time_series):
    start_timestamp = datetime.utcnow() - timedelta(days=1)
    end_timestamp = datetime.utcnow()
    interval = timedelta(minutes=1)
    query_plan = QueryPlan(time_series, start_timestamp, end_timestamp, interval, sync=False)
    assert query_plan.dataset == time_series
    assert query_plan._start_timestamp == start_timestamp
    assert await query_plan.start_timestamp() == start_timestamp
    assert query_plan.end_timestamp == end_timestamp
    assert query_plan.interval == interval

@pytest.mark.asyncio
async def test_query_plan_await(query_plan):
    dataset = await query_plan
    assert isinstance(dataset, Dataset)

@pytest.mark.asyncio
async def test_query_plan_getitem(query_plan):
    timestamp = datetime.utcnow() - timedelta(hours=1)
    time_data_row = query_plan[timestamp]
    assert isinstance(time_data_row, TimeDataRow)
    assert time_data_row.timestamp == timestamp

@pytest.mark.asyncio
async def test_query_plan_aiter(query_plan):
    async for row in query_plan:
        assert isinstance(row, TimeDataRow)