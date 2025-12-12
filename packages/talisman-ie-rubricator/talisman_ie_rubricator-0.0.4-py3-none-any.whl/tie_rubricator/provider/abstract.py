from abc import ABCMeta, abstractmethod
from typing import AsyncIterator

from tie_rubricator.datamodel import Rubricator
from tp_interfaces.abstract import ImmutableBaseModel


class AbstractRubricatorProvider(metaclass=ABCMeta):
    @abstractmethod
    async def get_rubricators(self) -> AsyncIterator[Rubricator]:
        pass


class AbstractRubricatorProviderConfig(ImmutableBaseModel, metaclass=ABCMeta):
    type: str

    @abstractmethod
    async def get_provider(self) -> AbstractRubricatorProvider:
        pass
