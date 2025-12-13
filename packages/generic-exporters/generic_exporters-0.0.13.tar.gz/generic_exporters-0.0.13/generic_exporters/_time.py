
from functools import cached_property
from typing import TYPE_CHECKING, Iterable, List

import a_sync

from generic_exporters import _types

if TYPE_CHECKING:
    from generic_exporters import Metric

class _TimeDataBase(a_sync.ASyncGenericBase):
    """A base class for representing time series data, both materialized and not-yet-materialized.

    This class serves as a foundational component for time series data handling within the library.
    It is designed to be subclassed by more specific time series data structures that require
    a common interface for handling fields related to time series data.

    Attributes:
        fields (list): A list of fields that represent the data points or metrics within the time series.
        sync (bool): A flag indicating whether operations should be performed synchronously or asynchronously.

    Args:
        fields (Iterable[_types.SingleProcessable]): An iterable of fields, typically metrics or other
                                                     processable units, that make up the time series data.
        sync (bool, optional): Specifies if operations should be executed synchronously. Defaults to True.
    """
    metrics: List["Metric"]
    def __init__(self, fields: Iterable[_types.SingleProcessable], *, sync: bool = True) -> None:
        """Initializes a new instance of the _TimeDataBase class.

        Args:
            fields (Iterable[_types.SingleProcessable]): An iterable of fields that represent the data points
                                                         or metrics within the time series.
            sync (bool, optional): Specifies if operations should be executed synchronously. Defaults to True.
        """
        # dodge a circular import
        from generic_exporters import Metric, TimeSeries
        self.metrics = []
        for f in fields:
            if isinstance(f, TimeSeries):
                self.metrics.append(f.metric)
            elif isinstance(f, Metric): #, Attribute): TODO
                self.metrics.append(f)
            else:
                raise TypeError(f"each item in `fields` must be either `Metric` or `TimeSeries`. You passed {f}")
        self.sync = sync
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} for {self.keys}>"
    @cached_property
    def keys(self) -> List[str]:
        """Returns a list of keys representing the fields in the dataset."""
        return [field.key for field in self.metrics]
