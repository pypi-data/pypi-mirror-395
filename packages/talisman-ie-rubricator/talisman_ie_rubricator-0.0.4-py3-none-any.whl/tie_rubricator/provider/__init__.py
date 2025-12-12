__all__ = [
    'AbstractRubricatorProvider', 'AbstractRubricatorProviderConfig',
    'APIRubricatorProviderConfig',
    'LocalRubricatorProviderConfig',
    'RubricatorProviderConfig'
]

from typing import Annotated

from pydantic import Field

from .abstract import AbstractRubricatorProvider, AbstractRubricatorProviderConfig
from .api import APIRubricatorProviderConfig
from .local import LocalRubricatorProviderConfig

RubricatorProviderConfig = Annotated[LocalRubricatorProviderConfig | APIRubricatorProviderConfig, Field(discriminator='type')]
