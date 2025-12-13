
from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, Optional, TypeVar

import a_sync

from generic_exporters._awaitable import _AwaitableMixin
from generic_exporters.plan import QueryPlan

if TYPE_CHECKING:
    from generic_exporters import Metric

_T = TypeVar('_T')


class _ProcessorBase(_AwaitableMixin[_T], a_sync.ASyncGenericBase):
    def __init__(self, *, sync: bool = True):
        if not isinstance(sync, bool):
            raise TypeError(f'`sync` must be boolean. You passed {sync}')
        self.sync = sync
    @abstractmethod
    async def run(self) -> _T:
        """Runs the processor"""
    async def _materialize(self) -> _T:
        return await self.run(sync=False)


class _TimeSeriesProcessorBase(_ProcessorBase[_T]):
    def __init__(
        self, 
        query: QueryPlan, 
        *,
        concurrency: Optional[int] = None,
        sync: bool = True,
    ) -> None:
        super().__init__(sync=sync)
        if not isinstance(query, QueryPlan):
            raise TypeError(f'`query` must be `QueryPlan`. You passed {query}')
        self.query = query
        if concurrency is not None and not isinstance(concurrency, int):
            raise TypeError(f'`concurrency` must be int. You passed {concurrency}')
        self.concurrency = concurrency


class _GatheringTimeSeriesProcessorBase(_TimeSeriesProcessorBase[_T]):
    """Inherit from this class when you need to collect all the data before processing"""
    async def _gather(self) -> Dict[datetime, Dict["Metric", Decimal]]:
        return await a_sync.gather({ts: self.query[ts] async for ts in self.query._aiter_timestamps()})
