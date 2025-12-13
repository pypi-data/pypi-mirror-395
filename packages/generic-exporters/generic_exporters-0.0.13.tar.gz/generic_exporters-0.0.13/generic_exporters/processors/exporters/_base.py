
from abc import abstractmethod, abstractproperty
from typing import TYPE_CHECKING, Optional, TypeVar

from generic_exporters.processors._base import _ProcessorBase, _TimeSeriesProcessorBase
from generic_exporters.processors.exporters.datastores.timeseries._base import TimeSeriesDataStoreBase
from generic_exporters.processors.exporters.datastores.timeseries.sql import SQLTimeSeriesKeyValueStore

if TYPE_CHECKING:
    from generic_exporters import QueryPlan


_T = TypeVar('_T')

class _ExporterBase(_ProcessorBase[None]):
    @abstractmethod
    async def data_exists(self) -> bool:
        """Returns True if data exists, False if it does not and must be produced."""


class _TimeSeriesExporterBase(_TimeSeriesProcessorBase, _ExporterBase):
    """I dont remember why I made this base class. Maybe I will"""
    def __init__(
        self, 
        query_plan: "QueryPlan", 
        datastore: Optional[TimeSeriesDataStoreBase], 
        *, 
        concurrency: Optional[int] = None,
        sync: bool = True,
    ) -> None:
        super().__init__(query_plan, concurrency=concurrency, sync=sync)
        if isinstance(datastore, TimeSeriesDataStoreBase):
            self.datastore = datastore
        elif datastore is None:
            self.datastore = SQLTimeSeriesKeyValueStore()
        else:
            raise TypeError(datastore)
        self.datastore = datastore


class _PropertyExporterBase(_TimeSeriesExporterBase):
    # TODO: implement
    output_type: _T
    @abstractproperty
    def property_name(self) -> str:
        pass
    @abstractmethod
    async def produce(self) -> _T:
        pass
