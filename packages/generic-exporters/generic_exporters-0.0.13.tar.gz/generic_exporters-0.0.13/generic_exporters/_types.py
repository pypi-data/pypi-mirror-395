
from decimal import Decimal
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from generic_exporters import Metric, TimeSeries, WideTimeSeries

Numeric = Union[int, float, Decimal]
Numericish = Union[Numeric, "Metric"]
SingleProcessable = Union["Metric", "TimeSeries"]
Processable = Union[SingleProcessable, "WideTimeSeries"]
