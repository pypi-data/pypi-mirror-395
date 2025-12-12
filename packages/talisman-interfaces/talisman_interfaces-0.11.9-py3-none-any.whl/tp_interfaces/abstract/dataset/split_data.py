from abc import ABCMeta, abstractmethod
from typing import Generic, Iterable, TypeVar

_ItemType = TypeVar('_ItemType')


class AbstractSplitData(Generic[_ItemType], metaclass=ABCMeta):

    @property
    @abstractmethod
    def roles(self) -> set[str]:
        ...

    @abstractmethod
    def get_data(self, role: str | None = None) -> Iterable[_ItemType]:
        ...
