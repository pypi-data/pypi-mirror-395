# DONE
import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Any

from generic_exporters.processors.exporters.datastores.timeseries._base import TimeSeriesDataStoreBase


class TimeSeriesMultiDataStore(TimeSeriesDataStoreBase):
    def __init__(self, *datastores: TimeSeriesDataStoreBase) -> None:
        self.datastores = datastores
    async def data_exists(self, key: Any, ts: datetime) -> bool:
        """Returns True if the datapoint exists in all datastores, False if not."""
        return all(await asyncio.gather(*[ds.data_exists(key, ts) for ds in self.datastores]))
    async def push(self, key: Any, ts: datetime, data: Decimal) -> None:
        """Exports one datapoint to all datastores. NOTE: Will swallow any exceptions that may occur. They will not raise."""
        return await asyncio.gather(*[ds.push(key, ts, data) for ds in self.datastores], return_exceptions=True)
