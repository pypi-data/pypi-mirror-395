from abc import abstractmethod
from functools import cached_property
from typing import TYPE_CHECKING, Generic, Tuple, Type, TypeVar

import a_sync

from generic_exporters import _types

if TYPE_CHECKING:
    from generic_exporters.metric import (_AdditionMetric, _SubtractionMetric,
                                          _MultiplicationMetric, _TrueDivisionMetric,
                                          _FloorDivisionMetric, _PowerMetric)

_T = TypeVar('_T')

class _MathableBase(a_sync.ASyncGenericBase, Generic[_T]):
    """A base class providing arithmetic operation capabilities.

    This class defines the ability to perform arithmetic operations on objects
    that inherit from it. It requires subclasses to implement the `_validate_other`
    method to ensure compatibility of operands and uses the `__math_classes__`
    property to define the result types of these operations.

    The arithmetic operations supported are addition, subtraction, multiplication,
    true division, floor division, and exponentiation.

    Args:
        Generic[_T]: A generic type parameter that specifies the type of the operands.
    """

    def __add__(self, other: _types.Numericish) -> "_AdditionMetric":
        """Performs addition with another numeric-like object.

        Args:
            other (_types.Numericish): The other operand for the addition.

        Returns:
            _AdditionMetric: The result of the addition operation.
        """
        return self.__math_classes__[0](self, self._validate_other(other))

    def __sub__(self, other: _types.Numericish) -> "_SubtractionMetric":
        """Performs subtraction with another numeric-like object.

        Args:
            other (_types.Numericish): The other operand for the subtraction.

        Returns:
            _SubtractionMetric: The result of the subtraction operation.
        """
        return self.__math_classes__[1](self, self._validate_other(other))

    def __mul__(self, other: _types.Numericish) -> "_MultiplicationMetric":
        """Performs multiplication with another numeric-like object.

        Args:
            other (_types.Numericish): The other operand for the multiplication.

        Returns:
            _MultiplicationMetric: The result of the multiplication operation.
        """
        return self.__math_classes__[2](self, self._validate_other(other))

    def __truediv__(self, other: _types.Numericish) -> "_TrueDivisionMetric":
        """Performs true division with another numeric-like object.

        Args:
            other (_types.Numericish): The other operand for the division.

        Returns:
            _TrueDivisionMetric: The result of the true division operation.
        """
        return self.__math_classes__[3](self, self._validate_other(other))

    def __floordiv__(self, other: _types.Numericish) -> "_FloorDivisionMetric":
        """Performs floor division with another numeric-like object.

        Args:
            other (_types.Numericish): The other operand for the floor division.

        Returns:
            _FloorDivisionMetric: The result of the floor division operation.
        """
        return self.__math_classes__[4](self, self._validate_other(other))

    def __pow__(self, other: _types.Numericish) -> "_PowerMetric":
        """Performs exponentiation with another numeric-like object.

        Args:
            other (_types.Numericish): The other operand for the exponentiation.

        Returns:
            _PowerMetric: The result of the exponentiation operation.
        """
        return self.__math_classes__[5](self, self._validate_other(other))

    @abstractmethod
    def _validate_other(self, other) -> _T:
        """Validates the other operand to ensure it is compatible for arithmetic operations.

        This method must be implemented by subclasses to define how operands are validated.

        Args:
            other: The operand to validate.

        Returns:
            _T: The validated operand, potentially converted or wrapped to ensure compatibility.
        """
        ...

    @cached_property
    def __math_classes__(self) -> Tuple[Type[_T], Type[_T], Type[_T], Type[_T], Type[_T], Type[_T]]:
        """Defines the result types for each arithmetic operation.

        This property should be overridden by subclasses if custom result types are needed.

        Returns:
            Tuple[Type[_T], Type[_T], Type[_T], Type[_T], Type[_T], Type[_T]]: A tuple containing
            the classes used for addition, subtraction, multiplication, true division, floor division,
            and exponentiation results, respectively.
        """
        from generic_exporters.metric import (_AdditionMetric, _SubtractionMetric,
                                              _MultiplicationMetric, _TrueDivisionMetric,
                                              _FloorDivisionMetric, _PowerMetric)
        return _AdditionMetric, _SubtractionMetric, _MultiplicationMetric, _TrueDivisionMetric, _FloorDivisionMetric, _PowerMetric