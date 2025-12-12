from typing import AsyncIterator, Iterable

from tdm.abstract.datamodel import AbstractDomainType
from tdm.datamodel.domain import Domain

from talisman_api import APISchema, version
from ._abstract import TalismanDomainAPIImpl


@version('0.14.10')
class _ImplV10(TalismanDomainAPIImpl):
    async def all_property_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).get_all_items('paginationConceptPropertyTypeIE'):
            yield i

        async for i in self._client(APISchema.KB_UTILS).get_all_items('paginationRelationPropertyTypeIE'):
            yield i

    async def platform_types(self) -> AsyncIterator[dict]:
        if False:
            yield {}

    async def account_types(self) -> AsyncIterator[dict]:
        if False:
            yield {}

    async def story_types(self) -> AsyncIterator[dict]:
        if False:
            yield {}

    def generate_types(self, domain: Domain) -> Iterable[AbstractDomainType]:
        from tie_domain.domain._synthetic import generate_types
        return generate_types(domain)
