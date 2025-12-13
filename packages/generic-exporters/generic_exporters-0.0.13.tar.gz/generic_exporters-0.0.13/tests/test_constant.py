
from decimal import Decimal
from generic_exporters import Constant


class TestConstant:
    def test_constant_value(self):
        const_value = 5
        constant = Constant(5)
        assert constant.value == Decimal(const_value)

    def test_constant_produce(self):
        const_value = 5
        constant = Constant(5)
        result = constant.produce(None, sync=True)  # Timestamp is irrelevant for Constant
        assert result == Decimal(const_value)

    def test_singleton_instance(self):
        instance1 = Constant(10)
        instance2 = Constant(10)
        assert instance1 is instance2

        instance3 = Constant(20)
        assert instance1 is not instance3