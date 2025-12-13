import pytest
from datetime import datetime
from decimal import Decimal

from aiohttp.client_exceptions import ContentTypeError

from generic_exporters.processors.exporters.datastores.timeseries.victoria import VictoriaMetrics

@pytest.fixture
def victoria_metrics():
    return VictoriaMetrics(url="http://localhost:8428", key_label_name="test_key", extra_labels={})

@pytest.mark.asyncio
async def test_victoria_metrics_methods(victoria_metrics):
    key = 'test_key'
    ts = datetime.utcnow()
    data = Decimal(10)
    # wont work with no vm running
    with pytest.raises(ContentTypeError):
        await victoria_metrics.data_exists(key, ts)
    with pytest.raises(TypeError):
        await victoria_metrics.push(key, ts, data)  # No assert needed, just checking for exceptions