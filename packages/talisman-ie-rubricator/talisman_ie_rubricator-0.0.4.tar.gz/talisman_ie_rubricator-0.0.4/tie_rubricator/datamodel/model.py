from typing_extensions import Self

from tp_interfaces.abstract import ImmutableBaseModel
from .description import RubricDescription
from .rubric import Rubric
from .rubricator import Rubricator


class RubricModel(ImmutableBaseModel):
    id: str
    name: str
    transformator_id: str | None = None

    children: tuple[str, ...]

    def deserialize(self) -> RubricDescription:
        return RubricDescription(
            id=self.id,
            name=self.name,
            transformator_id=self.transformator_id,
            children=self.children,
        )

    @classmethod
    def serialize(cls, rubric: Rubric) -> Self:
        return cls(
            id=rubric.id,
            name=rubric.name,
            transformator_id=rubric.transformator_id,
            children=tuple(rubric.rubricator.children(rubric.id))
        )


class RubricatorModel(ImmutableBaseModel):
    id: str
    name: str
    transformator_id: str | None = None

    rubrics: tuple[RubricModel, ...]

    def deserialize(self) -> Rubricator:
        return Rubricator(
            id_=self.id,
            name=self.name,
            transformator_id=self.transformator_id,
            rubrics=(rubric.deserialize() for rubric in self.rubrics)
        )

    @classmethod
    def serialize(cls, rubricator: Rubricator) -> Self:
        return cls(
            id=rubricator.id,
            name=rubricator.name,
            transformator_id=rubricator.transformator_id,
            rubrics=tuple(RubricModel.serialize(rubric) for rubric in rubricator.rubrics),
        )
