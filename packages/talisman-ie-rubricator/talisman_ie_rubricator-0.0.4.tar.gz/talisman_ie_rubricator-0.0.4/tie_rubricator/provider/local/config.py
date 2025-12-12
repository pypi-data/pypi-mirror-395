from pathlib import Path

from pydantic import TypeAdapter
from typing_extensions import Literal

from tie_rubricator.datamodel import Rubricator
from tie_rubricator.provider.abstract import AbstractRubricatorProviderConfig
from tie_rubricator.provider.local.provider import LocalRubricatorProvider


class LocalRubricatorProviderConfig(AbstractRubricatorProviderConfig):
    type: Literal['local'] = "local"

    path: Path

    async def get_provider(self) -> LocalRubricatorProvider:
        data = self.path.read_text(encoding="utf-8")
        rubricators: list[Rubricator] = TypeAdapter(list[Rubricator]).validate_json(data)
        return LocalRubricatorProvider(rubricators)
