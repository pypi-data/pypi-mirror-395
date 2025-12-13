import pytest
from decimal import Decimal
from datetime import datetime
from generic_exporters.metric import Constant, _AdditionMetric, _SubtractionMetric, _MultiplicationMetric, _TrueDivisionMetric, _FloorDivisionMetric, _PowerMetric

from tests.fixtures import *


@pytest.mark.asyncio
async def test_constant_metric():
    value = 10
    constant = Constant(value)
    assert constant.key == "constant"
    assert await constant.produce(datetime.utcnow()) == Decimal(value)

@pytest.mark.asyncio
async def test_addition_metric(dummy_metric):
    metric2 = Constant(5)
    addition_metric = _AdditionMetric(dummy_metric, metric2)
    result = await addition_metric.produce(datetime.utcnow())
    assert result == Decimal(15)

# Additional tests for subtraction, multiplication, division, etc. would follow a similar pattern.
# The following are placeholders for those tests.

@pytest.mark.asyncio
async def test_subtraction_metric(dummy_metric):
    metric2 = Constant(5)
    subtraction_metric = _SubtractionMetric(dummy_metric, metric2)
    result = await subtraction_metric.produce(datetime.utcnow())
    assert result == Decimal(5)

@pytest.mark.asyncio
async def test_multiplication_metric(dummy_metric):
    metric2 = Constant(5)
    multiplication_metric = _MultiplicationMetric(dummy_metric, metric2)
    result = await multiplication_metric.produce(datetime.utcnow())
    assert result == Decimal(50)

@pytest.mark.asyncio
async def test_true_division_metric(dummy_metric):
    metric2 = Constant(5)
    true_division_metric = _TrueDivisionMetric(dummy_metric, metric2)
    result = await true_division_metric.produce(datetime.utcnow())
    assert result == Decimal(2)

@pytest.mark.asyncio
async def test_floor_division_metric(dummy_metric):
    metric2 = Constant(5)
    floor_division_metric = _FloorDivisionMetric(dummy_metric, metric2)
    result = await floor_division_metric.produce(datetime.utcnow())
    assert result == Decimal(2)  # Assuming DummyMetric produces Decimal(10)

@pytest.mark.asyncio
async def test_power_metric(dummy_metric):
    metric2 = Constant(2)
    power_metric = _PowerMetric(dummy_metric, metric2)
    result = await power_metric.produce(datetime.utcnow())
    assert result == Decimal(100)

@pytest.mark.asyncio
async def test_constant_init():
    value = 10
    constant = Constant(value)
    assert constant.value == Decimal(value)

@pytest.mark.asyncio
async def test_constant_produce():
    value = 10
    constant = Constant(value)
    result = await constant.produce(None)  # Timestamp is irrelevant for Constant
    assert result == Decimal(value)