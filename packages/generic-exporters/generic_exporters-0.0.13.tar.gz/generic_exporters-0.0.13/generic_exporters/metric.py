
import asyncio
from abc import abstractmethod, abstractproperty
from datetime import datetime
from decimal import Decimal
from functools import cached_property
from typing import Any

import inflection

from generic_exporters import _constant, _mathable, _types

class Metric(_mathable._MathableBase):
    sync=False
    """
    A `Metric` represents a numeric measurement taken periodically over time. It contains the logic for taking that measurement at a specific timestamp and generating a unique key for the result.

    You can perform math operations on two `Metric` objects, the result will be a new `Metric` that can produce the result of the math operation between the two input `Metric`s at any given timestamp.

    You can also slice a `Metric` object to return a `Timeseries` future-like object that can materialize data for a specific time range and perform operations with the outputs.
    """
    def __init__(self) -> None:
        self._dependants = 0
    @abstractproperty
    def key(self) -> str:
        """A human-readable label for the metric being exported that will also be used as a unique key to identify this `Metric` in the datastore"""
    @abstractmethod
    async def produce(self, timestamp: datetime) -> Decimal:
        """Computes and returns the measurement at `timestamp` for this particular `Metric`"""
    def __repr__(self) -> str:
        return f'<{type(self).__name__} key={self.key}>'
    def _validate_other(self, other) -> "Metric":
        if isinstance(other, (int, float, Decimal)):
            other = Constant(other)
        if not isinstance(other, Metric):
            raise TypeError(other)
        return other


class Constant(Metric, metaclass=_constant.ConstantSingletonMeta):  # TODO: make this a singleton
    """
    A `Constant` is a `Metric` object that produces the same result at any given timestamp. 
    These are used to perform math operations between a `Metric` object and a constant value to create a new `Metric` object that represents the result of the operation.
    """
    def __init__(self, value: _types.Numeric) -> None:
        if not isinstance(value, (int, Decimal)):
            raise TypeError(value)
        self.value = Decimal(value)
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self.value}>"
    @cached_property
    def key(self) -> None:
        return inflection.underscore(type(self).__name__)
    async def produce(self, timestamp: datetime) -> Decimal:
        return self.value



class _MathResultMetricBase(Metric):
    """These are created by the library when you perform math operations on `Metric` objects. You should not need to interact with this class directly"""
    def __init__(self, metric0: Metric, metric1: Metric) -> None:
        self.metric0 = metric0
        self.metric1 = metric1
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} for {self.metric0} {self._symbol} {self.metric1}>"
    async def produce(self, timestamp: datetime) -> Decimal:
       return self._do_math(*await asyncio.gather(self.metric0.produce(timestamp, sync=False), self.metric1.produce(timestamp, sync=False)))
    @cached_property
    def key(self) -> str:
        return f"({self.metric0.key}{self._symbol}{self.metric1.key})"
    @abstractproperty
    def _symbol(self) -> str:
        """The symbol of the math operation being performed"""
    @abstractmethod
    def _do_math(self, value0: Any, value1: Any) -> Any:
        """Performs the math operation"""


class _AdditionMetric(_MathResultMetricBase):
    """
    An `AdditionMetric` is a `Metric` that queries two input `Metrics` at any given timestamp, adds their outputs, and returns the sum.
    
    They are created by the library when you add two `Metric` objects. You should not need to interact with this class directly.
    """
    _symbol = '+'
    def _do_math(self, value0: Any, value1: Any) -> Any:
        return value0 + value1
    
class _SubtractionMetric(_MathResultMetricBase):
    """
    A `SubtractionMethod` is a `Metric` that queries two input `Metrics` at any given timestamp, subtracts their outputs, and returns the difference.
    
    They are created by the library when you subtract two `Metric` objects. You should not need to interact with this class directly.
    """
    _symbol = '-'
    def _do_math(self, value0: Any, value1: Any) -> Any:
        return value0 - value1
    
class _MultiplicationMetric(_MathResultMetricBase):
    """A `MultiplicationMetric` is a `Metric` that queries two input `Metrics` at any given timestamp, multiplies their outputs, and returns the product.
    
    They are created by the library when you multiply two `Metric` objects. You should not need to interact with this class directly.
    """
    _symbol = '*'
    def _do_math(self, value0: Any, value1: Any) -> Any:
        return value0 * value1
    
class _TrueDivisionMetric(_MathResultMetricBase):
    """A `TrueDivisionMetric` is a `Metric` that queries two input `Metrics` at any given timestamp, divides their outputs, and returns the true quotient.
    
    They are created by the library when you divide two `Metric` objects. You should not need to interact with this class directly.
    """
    _symbol = '/'
    def _do_math(self, value0: Any, value1: Any) -> Any:
        return value0 / value1
    
class _FloorDivisionMetric(_MathResultMetricBase):
    """A `FloorDivisionMetric` is a `Metric` that queries two input `Metrics` at any given timestamp, divides their outputs, and returns the floored quotient.
    
    They are created by the library when you divide two `Metric` objects. You should not need to interact with this class directly.
    """
    _symbol = '//'
    def _do_math(self, value0: Any, value1: Any) -> Any:
        return value0 // value1
    
class _PowerMetric(_MathResultMetricBase):
    """A `PowerMetric` is a `Metric` that queries two input `Metrics` at any given timestamp, raises the output of the first to the power of the output of the second, and returns the exponentiation.
    
    They are created by the library when you exponentiate two `Metric` objects. You should not need to interact with this class directly.
    """
    _symbol = '**'
    def _do_math(self, value0: Any, value1: Any) -> Any:
        return value0 ** value1
