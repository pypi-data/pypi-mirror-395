from typing import AsyncIterator, Iterable

from talisman_api import APISchema, version
from tie_rubricator.datamodel.description import RubricDescription
from tie_rubricator.provider.api.provider import APIRubricatorProvider, RubricatorInfo


@version('0.17.0')
class _Impl170(APIRubricatorProvider):
    @classmethod
    def _required_apis(cls) -> Iterable[APISchema]:
        return APISchema.PUBLIC,

    async def rubrics(self, rubricator_id: str) -> AsyncIterator[RubricDescription]:
        async for info in self._client(APISchema.PUBLIC).paginate_items('paginationRubricIE', variables={'rubricator_id': rubricator_id}):
            yield RubricDescription(
                id=info['id'],
                name=info['name'],
                transformator_id=info['transformatorId'],
                children=tuple(child['id'] for child in info['children']),
            )

    async def rubricators(self) -> AsyncIterator[RubricatorInfo]:
        # Here `rubricator_id` should not be set. But GQL request fails even for paginationRubricatorsIE query.
        async for info in self._client(APISchema.PUBLIC).paginate_items('paginationRubricatorsIE', variables={'rubricator_id': ""}):
            yield RubricatorInfo(
                id=info['id'],
                name=info['name'],
                transformator_id=info['transformatorId']
            )
