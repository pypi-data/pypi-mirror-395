from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from tdm.abstract.datamodel import AbstractFact, FactStatus
from tdm.datamodel.facts import AtomValueFact, ConceptFact, PropertyFact
from tdm.datamodel.values import StringValue
from typing_extensions import Protocol

from .domain import RUBRIC, RUBRICATOR_ID, RUBRIC_ID, STR_VALUE


class Rubricator(Protocol):
    @property
    def transformator_id(self) -> str:
        pass

    def rubric(self, *, rubric_id: str) -> Rubric:
        pass

    def children(self, rubric_id: str) -> set[str]:
        pass

    def parent(self, rubric_id: str) -> str | None:
        pass


@dataclass(frozen=True)
class Rubric:
    id: str
    name: str
    transformator_id: str | None
    rubricator: Rubricator

    @property
    def as_facts(self) -> Iterable[AbstractFact]:
        if self.transformator_id is None or self.rubricator.transformator_id is None:
            return ()  # log warning
        return (
            rubric := ConceptFact(FactStatus.AUTO, RUBRIC),
            rubric_id := AtomValueFact(FactStatus.AUTO, STR_VALUE, StringValue(self.transformator_id)),
            PropertyFact(FactStatus.AUTO, RUBRIC_ID, rubric, rubric_id),
            rubricator_id := AtomValueFact(FactStatus.AUTO, STR_VALUE, StringValue(self.rubricator.transformator_id)),
            PropertyFact(FactStatus.AUTO, RUBRICATOR_ID, rubric, rubricator_id)
        )

    @property
    def root_path(self) -> tuple[Rubric, ...]:
        result = []
        current = self
        while current is not None:
            result.append(current)
            current = current.parent
        return tuple(result)

    @property
    def children(self) -> set[Rubric]:
        return {self.rubricator.rubric(rubric_id=child) for child in self.rubricator.children(self.id)}

    @property
    def parent(self) -> Rubric | None:
        parent_id = self.rubricator.parent(self.id)
        if parent_id is None:
            return None
        return self.rubricator.rubric(rubric_id=parent_id)

    @property
    def is_root(self) -> bool:
        return self.rubricator.parent(self.id) is None
