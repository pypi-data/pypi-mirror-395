import pytest
from datetime import datetime, timedelta

from tests.fixtures import *

def test_time_series_initialization(time_series, dummy_metric):
    assert time_series.metric == dummy_metric

@pytest.mark.asyncio
async def test_time_series_getitem(time_series):
    start = datetime.utcnow() - timedelta(days=1)
    end = datetime.utcnow()
    interval = timedelta(minutes=1)
    query_plan = time_series[start:end:interval]
    assert query_plan.start_timestamp == start
    assert query_plan.end_timestamp == end
    assert query_plan.interval == interval

@pytest.mark.asyncio
async def test_wide_time_series_getitem(wide_time_series):
    start = datetime.utcnow() - timedelta(days=1)
    end = datetime.utcnow()
    interval = timedelta(minutes=1)
    query_plan = wide_time_series[start:end:interval]
    assert isinstance(query_plan, QueryPlan)