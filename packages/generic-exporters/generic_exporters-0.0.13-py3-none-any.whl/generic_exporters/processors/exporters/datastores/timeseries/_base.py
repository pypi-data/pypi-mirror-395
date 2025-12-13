# DONE
from abc import ABCMeta, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Any


class TimeSeriesDataStoreBase(metaclass=ABCMeta):
    @abstractmethod
    async def data_exists(self, key: Any, ts: datetime) -> bool:
        """Returns True if the datapoint exists in the datastore, False if not."""
    @abstractmethod
    async def push(self, key: Any, ts: datetime, data: Decimal) -> None:
        """Exports one datapoint to the datastore."""
