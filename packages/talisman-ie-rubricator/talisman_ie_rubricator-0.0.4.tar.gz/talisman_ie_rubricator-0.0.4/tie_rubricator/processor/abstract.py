import logging
from abc import ABCMeta

from typing_extensions import Self

from tie_rubricator.datamodel import Rubricator
from tie_rubricator.provider import AbstractRubricatorProviderConfig, RubricatorProviderConfig
from tp_interfaces.abstract import AbstractConfigConstructableModel, AbstractDocumentProcessor, ImmutableBaseModel

logger = logging.getLogger(__name__)


class AbstractRubricatorConfig(ImmutableBaseModel):
    provider: RubricatorProviderConfig


class AbstractRubricatorProcessor(
    AbstractDocumentProcessor,
    AbstractConfigConstructableModel,
    metaclass=ABCMeta
):
    def __init__(self, provider_config: AbstractRubricatorProviderConfig):
        self._provider_config: AbstractRubricatorProviderConfig = provider_config

        self._transformator_id2rubric: dict[str, Rubricator] | None = None  # transformator id -> rubricator

    async def __aenter__(self) -> Self:
        provider = await self._provider_config.get_provider()

        self._transformator_id2rubric = {}
        async for rubricator in provider.get_rubricators():
            if rubricator.transformator_id is None:
                logger.warning(f"Rubricator [{rubricator.id}]({rubricator.name}) has no transformator id. It could not be used")
                continue
            self._transformator_id2rubric[rubricator.transformator_id] = rubricator
        return self

    async def __aexit__(self, exc_type, exc_value, traceback, /):
        self._transformator_id2rubric = None

    @classmethod
    def from_config(cls, config: dict) -> Self:
        config = AbstractRubricatorConfig.model_validate(config)
        return cls(provider_config=config.provider)
