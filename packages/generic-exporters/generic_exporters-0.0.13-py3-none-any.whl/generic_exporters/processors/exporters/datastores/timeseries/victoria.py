
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, NewType

from aiohttp import ClientSession
from generic_exporters.processors.exporters.datastores.timeseries._base import TimeSeriesDataStoreBase

LabelName = NewType('LabelName', str)
LabelValue = NewType('LabelValue', Any)

class VictoriaMetrics(TimeSeriesDataStoreBase):
    def __init__(self, url: str, key_label_name: LabelName, extra_labels: Dict[LabelName, LabelValue]) -> None:
        self.url = url
        self.key_label_name = key_label_name
        self.extra_labels = extra_labels

    async def data_exists(self, key: LabelValue, ts: datetime) -> bool:
        """Returns True if `data_query` returns results from your Victoria Metrics db, False if not."""
        # TODO: check vm
        labels = {self.key_label_name: key, "ts": ts, **self.extra_labels}
        data_query = str(labels)
        return await self._post(data_query)
    
    async def push(self, key: LabelValue, ts: datetime, data: Decimal) -> None:
        """Exports `data` to Victoria Metrics using `key` somehow. lol"""
        # TODO: send to vm
        labels = {self.key_label_name: key, "ts": ts, **self.extra_labels}
        value = data
        return await self._post([labels, value])
    
    async def _post(self, data: bytes) -> Any:
        async with ClientSession() as session:
            async with session.post(self.url, data=data) as response:
                return await response.json()
