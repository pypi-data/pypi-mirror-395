from dataclasses import dataclass

from tdm.datamodel.domain.types import AbstractConceptType


@dataclass(frozen=True)
class StoryType(AbstractConceptType):
    """
    Concept domain type for story representation
    """
    pass
