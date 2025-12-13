
import pytest

from generic_exporters.metric import Constant, Metric
from generic_exporters._mathable import _MathableBase

class DummyMathable(_MathableBase):
    def _validate_other(self, other):
        return other

@pytest.mark.asyncio
async def test_mathable_operations():
    dummy = DummyMathable()
    constant_five = Constant(5)

    # Test addition
    result = dummy + constant_five
    assert isinstance(result, Metric)

    # Test subtraction
    result = dummy - constant_five
    assert isinstance(result, Metric)

    # Test multiplication
    result = dummy * constant_five
    assert isinstance(result, Metric)

    # Test true division
    result = dummy / constant_five
    assert isinstance(result, Metric)

    # Test floor division
    result = dummy // constant_five
    assert isinstance(result, Metric)

    # Test power
    result = dummy ** constant_five
    assert isinstance(result, Metric)