import threading
from collections import defaultdict
from typing import TYPE_CHECKING, Any, DefaultDict, Dict, Tuple, TypeVar

from a_sync.a_sync._meta import ASyncMeta

if TYPE_CHECKING:
    from generic_exporters import Constant

_T = TypeVar('_T')

class ConstantSingletonMeta(ASyncMeta):
    """A metaclass for creating singleton `Constant` instances.

    This metaclass ensures that only one instance of a `Constant` value exists within
    the application to conserve memory. It is thread-safe, ensuring that concurrent
    access does not lead to the creation of multiple instances for the same value.

    Attributes:
        __instances (DefaultDict[_T, Dict[bool, object]]): A dictionary that stores
                      singleton instances. The keys are constant values, and the
                      values are dictionaries mapping from a boolean (representing
                      whether the instance is synchronous or asynchronous) to the
                      instance itself.
        __lock (threading.Lock): A lock to ensure thread-safe access and creation
                                 of singleton instances.

    Args:
        ASyncMeta: Inherits from ASyncMeta to provide dual-function sync/async capabilities.
    """

    def __init__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> None:
        """Initializes the ConstantSingletonMeta metaclass.

        Args:
            name (str): The name of the class.
            bases (Tuple[type, ...]): A tuple containing the base classes of the class.
            namespace (Dict[str, Any]): A dictionary containing the namespace of the class.
        """
        cls.__instances: DefaultDict[_T, Dict[bool, object]] = defaultdict(dict)
        cls.__lock = threading.Lock()
        super().__init__(name, bases, namespace)

    def __call__(cls, value: _T) -> "Constant":
        """Returns a singleton instance for the given value.

        This method checks if a singleton instance already exists for the given value.
        If not, it creates a new instance, ensuring thread-safe access and creation.

        Args:
            value (_T): The constant value for which a singleton instance is requested.

        Returns:
            Constant: A singleton instance corresponding to the given value.
        """
        is_sync = cls.__a_sync_instance_will_be_sync__((value), {})  # type: ignore [attr-defined]
        if is_sync not in cls.__instances[value]:
            with cls.__lock:
                # Check again in case `__instance` was set while we were waiting for the lock.
                if is_sync not in cls.__instances[value]:
                    cls.__instances[value][is_sync] = super().__call__(value)
        return cls.__instances[value][is_sync]
