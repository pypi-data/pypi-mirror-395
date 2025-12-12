import json
from pathlib import Path

from fsspec import AbstractFileSystem
from typing_extensions import Self

from tp_interfaces.serializable import SerializableFS
from .model import RubricatorModel


class SerializableRubricatorModel(RubricatorModel, SerializableFS):
    @classmethod
    def load_fs(cls, path: Path, fs: AbstractFileSystem) -> Self:
        with fs.open(str(path / "rubricator.json"), mode="r", encoding="utf-8") as file:
            data = json.load(file)
        return cls(**data)

    def save_fs(self, path: Path, fs: AbstractFileSystem, *, rewrite: bool = False) -> None:
        self._create_empty_dir(path, fs, clear=rewrite)
        with fs.open(str(path / "rubricator.json"), mode="w", encoding="utf-8") as file:
            json.dump(self.model_dump(), file, ensure_ascii=False, indent=2)
