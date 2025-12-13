
import pytest
from generic_exporters._time import _TimeDataBase

from tests.fixtures import *

class DummyTimeData(_TimeDataBase):
    pass

@pytest.mark.asyncio
async def test_time_data_base_init(dummy_metric):
    fields = [dummy_metric]
    time_data = DummyTimeData(fields)
    assert time_data.metrics == fields