from typing import AsyncIterator, Iterable

from tdm.abstract.datamodel import AbstractDomainType
from tdm.datamodel.domain import Domain

from talisman_api import version
from ._abstract import TalismanDomainAPIImpl


@version('0.16.4')
class _ImplV164(TalismanDomainAPIImpl):
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
