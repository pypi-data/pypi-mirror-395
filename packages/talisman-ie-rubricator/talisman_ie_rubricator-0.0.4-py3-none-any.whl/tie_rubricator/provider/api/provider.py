from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator

from talisman_api import AbstractTalismanAPI
from tie_rubricator.datamodel.description import RubricDescription
from tie_rubricator.datamodel.rubricator import Rubricator
from tie_rubricator.provider.abstract import AbstractRubricatorProvider


@dataclass(frozen=True)
class RubricatorInfo:
    id: str
    name: str
    transformator_id: str


class APIRubricatorProvider(AbstractTalismanAPI, AbstractRubricatorProvider, metaclass=ABCMeta):
    @abstractmethod
    async def rubrics(self, rubricator_id: str) -> AsyncIterator[RubricDescription]:
        pass

    @abstractmethod
    async def rubricators(self) -> AsyncIterator[RubricatorInfo]:
        pass

    async def get_rubricators(self) -> AsyncIterator[Rubricator]:
        async for rubricator_info in self.rubricators():
            rubrics = []
            async for rubric_description in self.rubrics(rubricator_info.id):
                rubrics.append(rubric_description)
            yield Rubricator(rubricator_info.id, rubricator_info.name, rubricator_info.transformator_id, rubrics)
