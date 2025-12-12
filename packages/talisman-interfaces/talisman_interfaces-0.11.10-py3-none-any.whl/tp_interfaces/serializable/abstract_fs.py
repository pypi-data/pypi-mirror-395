from abc import abstractmethod
from pathlib import Path

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from typing_extensions import Self

from tp_interfaces.serializable.abstract import Serializable


class SerializableFS(Serializable):
    @classmethod
    @abstractmethod
    def load_fs(cls, path: Path, fs: AbstractFileSystem) -> Self:
        pass

    @abstractmethod
    def save_fs(self, path: Path, fs: AbstractFileSystem, *, rewrite: bool = False) -> None:
        pass

    @classmethod
    def load(cls, path: Path) -> Self:
        fs = LocalFileSystem()
        return cls.load_fs(path, fs)

    def save(self, path: Path, *, rewrite: bool = False) -> None:
        fs = LocalFileSystem()
        self.save_fs(path, fs, rewrite=rewrite)

    @staticmethod
    def _create_empty_dir(directory: Path, *args, clear: bool = False) -> None:
        fs = args[0]
        if fs.exists(directory):
            if not fs.isdir(directory):
                raise ValueError(f'Provided path {directory} is not a directory!')
            if clear:
                fs.rm(str(directory), recursive=True)

        fs.makedirs(str(directory), exist_ok=True)
