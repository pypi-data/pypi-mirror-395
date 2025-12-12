import importlib
import inspect
import json
from abc import ABCMeta, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Generic, Iterable, TypeVar

from fsspec.implementations.local import LocalFileSystem
from fsspec.spec import AbstractFileSystem

from tp_interfaces.serializable import SerializableFS
from .split_data import AbstractSplitData

_ElementType = TypeVar('_ElementType')
ETC = "etc"
INFO = "info.json"


class AbstractDatasetManager(Generic[_ElementType], metaclass=ABCMeta):

    def __init__(self, path: str | PathLike, file_system: AbstractFileSystem | None = None):
        self._fs = file_system if file_system else LocalFileSystem()
        self._path = Path(path)
        self._extra_data = {}
        self._extra_path = self._path / ETC

    @abstractmethod
    def add(self, element: _ElementType) -> None:
        ...

    def update(self, elements: Iterable[_ElementType]) -> None:
        for element in elements:
            self.add(element)

    def add_extra_info(self, **kwargs: dict[str, SerializableFS]) -> None:
        if kwargs:
            self._extra_data = kwargs

    @abstractmethod
    def remove(self, element: _ElementType) -> None:
        ...

    @abstractmethod
    def save(self, version: str | None = None, exist_ok: bool = False) -> None:
        # TODO: reconsider the `version` parameter in the interface.
        #  It might be better to remove it from the interface and handle it via an implementation-level setter,
        #  since not all managers support the concept of versions.
        ...

    def save_extra_data(self) -> None:
        if self._extra_data:
            self._fs.makedirs(self._extra_path, exist_ok=True)

        for key, value in self._extra_data.items():
            extra_item_path = self._extra_path / key
            self._fs.makedirs(extra_item_path, exist_ok=True)
            value.save_fs(extra_item_path, self._fs)
            with self._fs.open(extra_item_path / INFO, "w", encoding="utf-8") as info_f:
                json.dump({
                    "module": inspect.getmodule(value).__name__,
                    "class": value.__class__.__name__
                }, info_f)

    def load_extra_data(self) -> None:
        if not self._fs.exists(self._extra_path):
            return

        for extra_item_path in self._fs.ls(self._extra_path, detail=False):
            extra_item_path = Path(extra_item_path)
            key = extra_item_path.stem
            with self._fs.open(extra_item_path / INFO, "r", encoding="utf-8") as info_f:
                info_dict = json.load(info_f)
            module = importlib.import_module(info_dict["module"])
            cls: type[SerializableFS] = getattr(module, info_dict["class"])
            self._extra_data[key] = cls.load_fs(extra_item_path, self._fs)

    @abstractmethod
    def get_dataset(self) -> AbstractSplitData:
        ...
