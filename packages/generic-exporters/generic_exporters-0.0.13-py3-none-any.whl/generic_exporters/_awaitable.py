
import asyncio
from abc import abstractmethod
from functools import cached_property
from typing import TYPE_CHECKING, Awaitable, TypeVar

import a_sync

if TYPE_CHECKING:
    from generic_exporters.dataset import Dataset

_T = TypeVar('_T')

class _AwaitableMixin(a_sync.ASyncGenericBase, Awaitable[_T]):
    """A mixin class to make objects awaitable in asynchronous operations.

    This mixin class allows objects to be used with the 'await' syntax in asynchronous
    code, making it easier to integrate with asynchronous workflows. It requires the
    subclass to implement the `_materialize` method, which defines the asynchronous
    operation to be awaited.

    Attributes:
        _task (asyncio.Task): A task that executes the await logic, cached for efficiency.

    Methods:
        __await__: Enables the use of 'await' on instances of the class.
        _materialize: Abstract method to be implemented by subclasses, defining the
                      asynchronous operation.

    Args:
        Awaitable[_T]: A generic type indicating the result type of the await operation.
    """

    def __await__(self) -> _T:
        """Enables the use of 'await' on instances of this class.

        Returns:
            _T: The result of the awaitable operation, as defined by the subclass's
                implementation of `_materialize`.
        """
        return self._task.__await__()

    @cached_property
    def _task(self) -> "asyncio.Task[Dataset[_T]]":
        """A cached asyncio.Task that executes the await logic.

        This property lazily creates and caches an asyncio.Task upon first access.
        The task is responsible for executing the subclass's implementation of
        `_materialize`, which defines the actual awaitable operation.

        Returns:
            asyncio.Task[Dataset[_T]]: The task that executes the await logic.
        """
        return asyncio.create_task(self._materialize())  # TODO: name the task with some heuristic

    @abstractmethod
    def _materialize(self) -> _T:
        """Abstract method that subclasses must implement to define the awaitable operation.

        This method should contain the asynchronous logic that is to be executed when
        an instance of the subclass is awaited. It must be implemented by subclasses.

        Returns:
            _T: The result of the asynchronous operation.
        """