from abc import ABCMeta, abstractmethod
from typing import Literal, Sequence, Type, TypeVar

from tp_interfaces.abstract.schema import ImmutableBaseModel
from .processor import AbstractProcessor


class EntityModel(ImmutableBaseModel):
    type: Literal["document", "concept"]
    id: str


class S3Result(ImmutableBaseModel):
    bucket: str
    path: str


class ExporterResult(ImmutableBaseModel):
    message: str
    result: S3Result | None


_Config = TypeVar('_Config', bound=ImmutableBaseModel)


class AbstractExporter(AbstractProcessor[_Config, EntityModel, ExporterResult], metaclass=ABCMeta):
    async def process_doc(self, document: EntityModel, config: _Config) -> ExporterResult:
        return await self.process_docs([document], config)

    @abstractmethod
    async def process_docs(self, documents: Sequence[EntityModel], config: _Config) -> ExporterResult:
        pass

    @property
    def input_type(self) -> Type[EntityModel]:
        return EntityModel

    @property
    def output_type(self) -> Type[ExporterResult]:
        return ExporterResult
