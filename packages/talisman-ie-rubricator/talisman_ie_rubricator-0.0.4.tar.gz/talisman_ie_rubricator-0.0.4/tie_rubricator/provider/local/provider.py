from typing import AsyncIterator, Iterable

from tie_rubricator.datamodel import Rubricator
from tie_rubricator.provider.abstract import AbstractRubricatorProvider


class LocalRubricatorProvider(AbstractRubricatorProvider):
    def __init__(self, rubricators: Iterable[Rubricator]):
        self._rubricators = tuple(rubricators)

    async def get_rubricators(self) -> AsyncIterator[Rubricator]:
        async def generator():
            for rubricator in self._rubricators:
                yield rubricator

        return generator()
