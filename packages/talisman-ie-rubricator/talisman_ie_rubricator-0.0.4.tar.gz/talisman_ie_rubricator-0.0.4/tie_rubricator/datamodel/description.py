from dataclasses import dataclass


@dataclass(frozen=True)
class RubricDescription:
    id: str
    name: str
    transformator_id: str | None
    children: tuple[str, ...]
