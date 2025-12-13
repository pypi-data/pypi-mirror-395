from datetime import datetime
from typing import TYPE_CHECKING, Dict, TypeVar

import a_sync
from bqplot import Figure

if TYPE_CHECKING:
    from generic_exporters.timeseries import TimeSeries, WideTimeSeries
    from generic_exporters.dataset import TimeDataRow

_DT = TypeVar("_DT", "TimeSeries", "WideTimeSeries", "TimeDataRow")

class Dataset(a_sync.ASyncGenericBase, Dict[datetime, _DT]):
    """A container for time series data, supporting various operations.

    This class extends the standard Python dictionary to create a specialized
    container for time series data. It is keyed by datetime objects and can
    hold TimeSeries, WideTimeSeries, or TimeDataRow instances as values. The
    Dataset class provides methods for plotting, exporting to CSV, and other
    operations useful in handling time series data.

    Args:
        Dict[datetime, _DT]: Inherits from the standard dictionary with datetime
                             keys and values of type TimeSeries, WideTimeSeries,
                             or TimeDataRow.
    """

    def __init__(self, data: _DT) -> None:
        """Initializes a new instance of the Dataset class.

        Args:
            data (_DT): The initial data to populate the Dataset. This can be an
                        instance of TimeSeries, WideTimeSeries, or TimeDataRow.
        """
        self._data = data

    async def plot(self) -> Figure:
        """Generates a plot for the dataset.

        This method is intended to provide a quick visualization of the time series
        data contained within the Dataset.

        Returns:
            Figure: an object containing the plotted data.
        """
        from generic_exporters import Plotter
        return await Plotter(self._data)

    async def to_csv(self, *to_csv_args, **to_csv_kwargs) -> None:
        """Exports the dataset to a CSV file.

        This method is intended to provide a way to export the time series data
        contained within the Dataset to a CSV file.
        """
        from generic_exporters import DataFramer
        df = await DataFramer(self._data)
        return df.to_csv(*to_csv_args, **to_csv_kwargs)

    async def export(self, datastore) -> None:
        """Exports the dataset to a specified datastore.

        This method is intended to provide a way to export the time series data
        contained within the Dataset to an external datastore.

        Args:
            datastore: The target datastore to which the Dataset should be exported.
        """
        from generic_exporters import TimeSeriesExporter
        return await TimeSeriesExporter(self._data, datastore)