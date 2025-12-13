
from pandas import DataFrame

from generic_exporters.processors._base import _GatheringTimeSeriesProcessorBase


class DataFramer(_GatheringTimeSeriesProcessorBase[DataFrame]):
    """
    Inherit from this class to turn any `Dataset` into a pandas DataFrame.

    You must define a start_timestamp method that will determine the start of the historical range, and a data_exists method that determines whether or not the datastore already contains data for the `Metric` at a particular timestamp. This class will handle the rest.
    """
    async def run(self) -> DataFrame:
        """Exports the full history for this exporter's `Metric` to the datastore"""
        return DataFrame(await self._gather)
