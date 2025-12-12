from typing import Literal

from talisman_api import CompositeTalismanAPIClient
from talisman_api.api_client import GQLClientConfig
from tie_rubricator.provider.abstract import AbstractRubricatorProviderConfig
from tie_rubricator.provider.api.provider import APIRubricatorProvider


class APIRubricatorProviderConfig(AbstractRubricatorProviderConfig):
    type: Literal['api'] = "api"

    clients: dict[str, GQLClientConfig]

    async def get_provider(self) -> APIRubricatorProvider:
        return await APIRubricatorProvider.get_compatible_api(
            client=CompositeTalismanAPIClient(self.clients)
        )
