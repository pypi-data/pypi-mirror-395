from __future__ import annotations

from collections import defaultdict
from typing import Iterable, overload

from .description import RubricDescription
from .rubric import Rubric


class Rubricator:
    def __init__(
            self,
            id_: str,
            name: str,
            transformator_id: str | None,
            rubrics: Iterable[RubricDescription],
    ) -> None:
        self._id = id_
        self._name = name
        self._transformator_id = transformator_id

        self._id2rubric: dict[str, Rubric] = {}
        self._transformator_id2rubric: dict[str, Rubric] = {}
        self._children: dict[str, set[str]] = defaultdict(set)
        self._parents: dict[str, str] = {}

        self._roots: set[str] = set()

        rubric_ids = set()  # mentioned rubric ids
        for description in rubrics:
            rubric = Rubric(description.id, description.name, description.transformator_id, self)
            rubric_id = _put_if_no_exist(self._id2rubric, rubric)
            rubric_ids.add(rubric_id)

            if rubric.transformator_id is not None:
                self._transformator_id2rubric[rubric.transformator_id] = rubric

            rubric_ids.update(description.children)
            self._children[rubric_id].update(description.children)
            for child_id in description.children:
                if child_id in self._parents and self._parents[child_id] != rubric_id:
                    raise ValueError(
                        f"The structure of the rubrics is not a tree. "
                        f"[{child_id}] has several parents: [{rubric_id}], [{self._parents[child_id]}]"
                    )
                self._parents[child_id] = rubric_id

        if set(self._id2rubric) != rubric_ids:
            raise ValueError

        self._roots = {rubric_id for rubric_id in self._id2rubric if rubric_id not in self._parents}

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def transformator_id(self) -> str | None:
        return self._transformator_id

    @property
    def rubrics(self) -> Iterable[Rubric]:
        return self._id2rubric.values()

    @property
    def roots(self) -> set[str]:
        return set(self._roots)

    @overload
    def rubric(self, *, rubric_id: str) -> Rubric:
        pass

    @overload
    def rubric(self, *, transformator_id: str) -> Rubric:
        pass

    def rubric(self, *, rubric_id: str = None, transformator_id: str = None) -> Rubric:
        if (rubric_id is None) == (transformator_id is None):
            raise ValueError
        if rubric_id is not None:
            return self._id2rubric[rubric_id]
        return self._transformator_id2rubric[transformator_id]

    def parent(self, rubric_id: str) -> str | None:
        return self._parents.get(rubric_id, None)

    def children(self, rubric_id: str) -> set[str]:
        return set(self._children.get(rubric_id, set()))

    def as_str(self) -> str:
        rubrics = {r.id: r for r in self.rubrics}

        def dfs(rubric_id: str, level: int) -> list[str]:
            rubric = rubrics[rubric_id]
            indent = '  ' * level
            lines = [f"{indent}- {rubric.name}"]

            children_ids = self.children(rubric_id)
            for child_id in children_ids:
                lines.extend(dfs(child_id, level + 1))
            return lines

        result_lines = []
        for root_id in self.roots:
            result_lines.extend(dfs(root_id, 0))

        return "\n".join(result_lines)


def _put_if_no_exist(id2rubric: dict[str, Rubric], rubric: Rubric) -> str:
    if rubric.id in id2rubric and rubric != id2rubric[rubric.id]:
        raise ValueError(f"Ambiguity for {rubric.id} rubric: {id2rubric[rubric.id]} != {rubric}")
    id2rubric[rubric.id] = rubric
    return rubric.id
