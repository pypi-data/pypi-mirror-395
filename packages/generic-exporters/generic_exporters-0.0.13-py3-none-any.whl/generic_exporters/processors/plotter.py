
from datetime import datetime
from typing import Optional

from bqplot import Axis, Figure, LinearScale, Lines

from generic_exporters.processors._base import _GatheringTimeSeriesProcessorBase


class Plotter(_GatheringTimeSeriesProcessorBase[Figure]):
    """
    Inherit from this class to plot any `Metric` on a line chart.

    You must define a start_timestamp method that will determine the start of the historical range, and a data_exists method that determines whether or not the datastore already contains data for the `Metric` at a particular timestamp. This class will handle the rest.
    """
    async def run(self, filename: str = "") -> None:
        """Exports the full history for this exporter's `Metric` to the datastore"""
        figure = await self.plot()
        now = datetime.utcnow()
        if not filename:
            filename = f"~/.generic_exporters/plots/{self.timeseries.metric.key}_{self.interval}_exported_at_{now.year}_{now.month}_{now.day}.png"
        figure.save_png(filename)
    
    async def plot(self) -> Figure:
        xscale = LinearScale()
        yscale = LinearScale()
        return Figure(
            marks=[await self._get_line(xscale, yscale)], 
            axes=[Axis(scale=xscale, label='timestamp'), Axis(scale=yscale)], 
            title=self.timeseries.metric.key,
        )
    
    async def _get_line(self, xscale: Optional[LinearScale] = None, yscale: Optional[LinearScale] = None) -> Lines:
        if xscale is None:
            xscale = LinearScale()
        if yscale is None: 
            yscale = LinearScale()
        data = await self._gather()
        return Lines(
            x=data.keys(), 
            y=data.values(), 
            scales={'x': xscale, 'y': yscale}, 
            labels=[field.key for field in self.timeseries.fields],
        )
