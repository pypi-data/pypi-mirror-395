from typing import AsyncIterator, Iterable

from tdm.abstract.datamodel import AbstractDomainType
from tdm.abstract.datamodel.domain import AbstractLinkDomainType
from tdm.datamodel.domain import AccountType, Domain, PlatformType
from tdm.datamodel.domain.types import ConceptType, DocumentType

from talisman_api import APISchema
from tie_domain.domain.api import TalismanDomainAPI
from tp_interfaces.domain.abstract import AbstractIdentifyingPropertyType, AbstractLiteralValueType, AbstractPropertyType, \
    AbstractRelationPropertyType, AbstractRelationType
from tp_interfaces.domain.types import StoryType


class TalismanDomainAPIImpl(TalismanDomainAPI):

    @classmethod
    def _required_apis(cls) -> Iterable[APISchema]:
        return (APISchema.KB_UTILS,)

    async def concept_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items('paginationConceptTypeIE'):
            yield i

    async def document_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items('paginationDocumentTypeIE'):
            yield i

    async def platform_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items(operation_name='paginationPlatformTypeIE'):
            yield i

    async def account_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items(operation_name='paginationAccountTypeIE'):
            yield i

    async def story_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items(operation_name='paginationStoryTypeIE'):
            yield i

    async def literal_value_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items('paginationValueTypeIE'):
            yield i

    async def composite_value_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items('paginationCompositeValueTypeIE'):
            yield i

    async def relation_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items('paginationRelationTypeIE'):
            yield i

    async def all_property_types(self) -> AsyncIterator[dict]:
        async for i in self._client(APISchema.KB_UTILS).paginate_items(operation_name='paginationPropertyTypeIE'):
            yield i

    async def property_type_extras(self, prop_type: AbstractPropertyType) -> dict:
        return await self._relext_based_type(prop_type, 'propertyTypeExtrasIE')

    async def relation_property_type_extras(self, rel_prop_type: AbstractRelationPropertyType) -> dict:
        return await self._relext_based_type(rel_prop_type, 'relationPropertyTypeExtrasIE')

    async def relation_type_extras(self, rel_type: AbstractRelationType) -> dict:
        return await self._relext_based_type(rel_type, 'relationTypeExtrasIE')

    async def _relext_based_type(self, type_: AbstractLinkDomainType, operation: str) -> dict:
        return await self._load_object(operation, {'source_type_id': type_.source.id, 'name': type_.id})

    async def id_property_type_extras(
            self,
            prop_type: AbstractIdentifyingPropertyType,
            regexp: bool = False,
            black_regexp: bool = False,
            pretrained_models: bool = False,
            dictionary: bool = False,
            black_list: bool = False
    ) -> dict:
        if isinstance(prop_type.source, ConceptType):
            operation = 'conceptTypeExtrasIE'
        elif isinstance(prop_type.source, DocumentType):
            operation = 'documentTypeExtrasIE'
        elif isinstance(prop_type.source, PlatformType):
            operation = 'platformTypeExtrasIE'
        elif isinstance(prop_type.source, AccountType):
            operation = 'accountTypeExtrasIE'
        elif isinstance(prop_type.source, StoryType):
            operation = 'storyTypeExtrasIE'
        else:
            raise ValueError
        variables = {
            'name': prop_type.source.id,
            'regexp': regexp,
            'black_regexp': black_regexp,
            'pretrained_models': pretrained_models,
            'dictionary': dictionary,
            'black_list': black_list
        }
        return await self._load_object(operation, variables)

    async def literal_value_type_extras(
            self,
            value_type: AbstractLiteralValueType,
            regexp: bool = False,
            black_regexp: bool = False,
            pretrained_models: bool = False,
            dictionary: bool = False,
            black_list: bool = False
    ) -> dict:
        variables = {
            'name': value_type.id,
            'regexp': regexp,
            'black_regexp': black_regexp,
            'pretrained_models': pretrained_models,
            'dictionary': dictionary,
            'black_list': black_list
        }
        return await self._load_object('valueTypeExtrasIE', variables)

    async def domain_update_info(self) -> set[tuple[str, int]]:
        return {
            (update['name'], update['updateDate'])
            for update in (await self._client(APISchema.KB_UTILS).execute('domainUpdateInfoIE'))['info']
        }

    async def _load_object(self, operation_name: str, variables: dict) -> dict:
        result = await self._find_object(operation_name, variables)
        if result is None:
            raise ValueError(f"no type found [operation: {operation_name}, variables: {variables}]")
        return result

    async def _find_object(self, operation_name: str, variables: dict) -> dict | None:
        if 'offset' in variables:
            raise ValueError
        offset = 0
        total = 1
        while offset < total:
            vs = {"offset": offset}
            vs.update(variables)
            result = (await self._client(APISchema.KB_UTILS).execute(operation_name, variables=vs))['result']
            if result['total'] == 0:
                return None
            total = result['total']
            for item in result['list']:
                if item['id'] == vs['name']:
                    return item
            offset += len(result['list'])

    def generate_types(self, domain: Domain) -> Iterable[AbstractDomainType]:
        from tie_domain.domain._synthetic._category import generate_types
        return generate_types(domain)
