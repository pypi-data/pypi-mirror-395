from typing import AsyncIterator

from talisman_api import version
from ._abstract import TalismanDomainAPIImpl


@version('0.17.0')
class _ImplV170(TalismanDomainAPIImpl):
    async def story_types(self) -> AsyncIterator[dict]:
        if False:
            yield {}
