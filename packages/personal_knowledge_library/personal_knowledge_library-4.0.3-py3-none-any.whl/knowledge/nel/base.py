# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import abc
from enum import Enum
from typing import Optional, List

from knowledge.base.language import LocaleCode, EN_US, DE_DE, JA_JP
from knowledge.base.ontology import THING_CLASS, OntologyClassReference
from knowledge.services.base import WacomServiceAPIClient, RESTAPIClient, DEFAULT_MAX_RETRIES, DEFAULT_BACKOFF_FACTOR


class EntityType(Enum):
    """
    Represents different types of entities.

    This enumeration class categorizes entities into three distinct types: Public,
    Personal, and Named. These types help to identify whether the entity belongs
    to a globally accessible knowledge graph, a specific private knowledge source,
    or if it is a standalone named entity without a linkage to an external knowledge graph.

    Attributes
    ----------
    PUBLIC_ENTITY : int
        Public entity - Entity from a public knowledge graph.
    PERSONAL_ENTITY : int
        Personal entity - Entity from a personal or organizational knowledge
        graph.
    NAMED_ENTITY : int
        Simple entity - Entity type not linked to a knowledge graph.
    """

    PUBLIC_ENTITY = 0
    """Public entity - Entity from a public knowledge graph"""
    PERSONAL_ENTITY = 1
    """Personal entity - Entity from a personal / organisational knowledge graph"""
    NAMED_ENTITY = 2
    """Simple entity - Entity type not linked to a knowledge graph"""


class KnowledgeSource(Enum):
    """
    KnowledgeSource defines an enumeration for different knowledge sources.

    This enumeration lists predefined constants representing various sources
    of knowledge. It helps standardize and unify the representation of external
    knowledge systems used within an application. Each attribute corresponds
    to a specific knowledge source, represented as a string.

    Attributes
    ----------
    WIKIDATA : str
        Wikidata
    DBPEDIA : str
        dbpedia
    WACOM_KNOWLEDGE : str
        Wacom Personal Knowledge
    """

    WIKIDATA = "wikidata"
    """Wikidata"""
    DBPEDIA = "dbpedia"
    """dbpedia"""
    WACOM_KNOWLEDGE = "wacom"
    """Wacom Personal Knowledge"""


class BasicType(Enum):
    """
    Enumeration representing basic types of entities.

    Defines a set of basic entity types used for categorization and identification
    in various contexts. This enumeration allows for easy comparison, clarity, and
    definition of specific categories for entities that can be encountered in
    different scenarios.

    Attributes
    ----------
    UNKNOWN : str
        Represents an unknown or undefined type.
    MONEY : str
        Represents a monetary value or currency-related type.
    PERSON : str
        Represents a person or an entity associated with a human being.
    DATE : str
        Represents a calendar date.
    PLACE : str
        Represents a physical or geographical location.
    TIME : str
        Represents a specific point in time or a duration.
    NUMBER : str
        Represents a numerical value or type.
    """

    UNKNOWN = "Unknown"
    MONEY = "Money"
    PERSON = "Person"
    DATE = "Date"
    PLACE = "Place"
    TIME = "Time"
    NUMBER = "Number"


class EntitySource:
    """
    EntitySource
    ------------
    Source of the entity.

    Parameters
    ----------
    uri: str
        URI of entity
    source: KnowledgeSource
        Identifier where the entity originates.
    """

    def __init__(self, uri: str, source: KnowledgeSource):
        self.__uri = uri
        self.__source: KnowledgeSource = source

    @property
    def uri(self) -> str:
        """Identifier with the knowledge graph."""
        return self.__uri

    @property
    def source(self) -> KnowledgeSource:
        """Source of the entity."""
        return self.__source

    def __repr__(self):
        return f"{self.uri} ({self.source})"


class NamedEntity(abc.ABC):
    """
    NamedEntity
    -----------
    A named entity which is recognized by the recognition engine.
    The class contains information on the found entity, found in reference text.

    Parameters
    ----------
    ref_text: str
        Reference text. Entity found for this specific text
    start_idx: int
        Start index within the full reference text
    end_idx: int
        End index with the full reference text
    entity_type: EntityType
        Type of the entity.
    """

    def __init__(self, ref_text: str, start_idx: int, end_idx: int, entity_type: EntityType):
        self.__ref_text: str = ref_text
        self.__start_idx: int = start_idx
        self.__end_idx: int = end_idx
        self.__type: EntityType = entity_type

    @property
    def ref_text(self) -> str:
        """Reference text for which the entity has been found"""
        return self.__ref_text

    @property
    def start_idx(self) -> int:
        """Start an index within the text handed to the named entity recognition."""
        return self.__start_idx

    @property
    def end_idx(self) -> int:
        """End index within the text handed to the named entity recognition."""
        return self.__end_idx

    @property
    def entity_type(self) -> EntityType:
        """Type of the entity."""
        return self.__type

    def __repr__(self):
        return f"{self.ref_text} [{self.start_idx}-{self.end_idx}"


class KnowledgeGraphEntity(NamedEntity):
    """
    Knowledge graph entity
    ----------------------
    Entity from a knowledge graph.

    Parameters
    ----------
    ref_text: str
        Reference text. Entity found for this specific text
    start_idx: int
        Start index within the full reference text
    end_idx: int
        End index with the full reference text
    label: str
        Main label of the entity.
    confidence: float
        Confidence value if available
    source: EntitySource
        Source of the entity
    content_link: str
        Link to side with content
    ontology_types: List[str]
        List of ontology types (class names)
    entity_type: EntityType
        Type of the entity.
    tokens: Optional[List[str]] (default:=None)
        List of tokens used to identify the entity.
    token_indexes: Optional[List[int]] (default:=None)
        List of token indexes used to identify the entity.
    """

    def __init__(
        self,
        ref_text: str,
        start_idx: int,
        end_idx: int,
        label: str,
        confidence: float,
        source: EntitySource,
        content_link: str,
        ontology_types: List[str],
        entity_type: EntityType = EntityType.PUBLIC_ENTITY,
        tokens: Optional[List[str]] = None,
        token_indexes: Optional[List[int]] = None,
    ):
        super().__init__(ref_text, start_idx, end_idx, entity_type)
        self.__source: EntitySource = source
        self.__content_link: str = content_link
        self.__label: str = label
        self.__confidence: float = confidence
        self.__description: Optional[str] = None
        self.__thumbnail: Optional[str] = None
        self.__ontology_types: List[str] = ontology_types
        self.__relevant_type: OntologyClassReference = THING_CLASS
        self.__tokens: Optional[List[str]] = tokens
        self.__token_indexes: Optional[List[int]] = token_indexes

    @property
    def entity_source(self) -> EntitySource:
        """Source of the entity."""
        return self.__source

    @property
    def label(self) -> str:
        """Label of the entity from the knowledge graph."""
        return self.__label

    @property
    def confidence(self) -> float:
        """Confidence level of the system that links the entities."""
        return self.__confidence

    @confidence.setter
    def confidence(self, value: float):
        self.__confidence = value

    @property
    def description(self) -> Optional[str]:
        """Description of the entity if available."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def thumbnail(self) -> Optional[str]:
        """Thumbnail to describe the entity."""
        return self.__thumbnail

    @thumbnail.setter
    def thumbnail(self, value: str):
        self.__thumbnail = value

    @property
    def content_link(self) -> str:
        """Link to content page."""
        return self.__content_link

    @property
    def ontology_types(self) -> List[str]:
        """List of ontology types."""
        return self.__ontology_types

    @property
    def relevant_type(self) -> OntologyClassReference:
        """Most relevant ontology type. That like to Wacom's personal knowledge base ontology."""
        return self.__relevant_type

    @relevant_type.setter
    def relevant_type(self, value: OntologyClassReference):
        self.__relevant_type = value

    @property
    def tokens(self) -> Optional[List[str]]:
        """List of tokens used to identify the entity."""
        return self.__tokens

    @property
    def token_indexes(self) -> Optional[List[int]]:
        """List of token indexes used to identify the entity."""
        return self.__token_indexes

    def __repr__(self):
        return f"{self.ref_text} [{self.start_idx}-{self.end_idx}] -> {self.entity_source} [{self.entity_type}]"


class BasicNamedEntity(NamedEntity):
    """
    Basic named entity
    ------------------
    Entity found by Named entity recognition.

    Parameters
    ----------
    ref_text: str
        Reference text. Entity found for this specific text
    start_idx: int
        Start index within the full reference text
    end_idx: int
        End index with the full reference text
    basic_type: BasicType
        Type of the entity.
    """

    def __init__(self, ref_text: str, start_idx: int, end_idx: int, basic_type: BasicType):
        super().__init__(ref_text, start_idx, end_idx, EntityType.NAMED_ENTITY)
        self.__basic_type: BasicType = basic_type

    @property
    def basic_type(self) -> BasicType:
        """Basic type that is recognized."""
        return self.__basic_type

    def __repr__(self):
        return f"{self.ref_text} [{self.start_idx}-{self.end_idx}] -> {self.basic_type}"


class PersonalEntityLinkingProcessor(WacomServiceAPIClient):
    """
    PersonalEntityLinkingProcessor
    ------------------------------
    Service that links entities to entities in a personal knowledge graph.

    Parameters
    ----------
    service_url: str
        URL where the service has been deployed
    verify_calls: bool (default:=False)
        Verifies all HTTPS calls and the associated certificate.
    """

    LANGUAGES: List[LocaleCode] = [DE_DE, EN_US, JA_JP]

    def __init__(
        self,
        service_url: str,
        application_name: str = "Semantic Search Client",
        base_auth_url: Optional[str] = None,
        service_endpoint: str = "vector/api/v1",
        verify_calls: bool = True,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ):
        super().__init__(
            service_url=service_url,
            application_name=application_name,
            base_auth_url=base_auth_url,
            service_endpoint=service_endpoint,
            verify_calls=verify_calls,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

    @abc.abstractmethod
    def link_personal_entities(
        self, text: str, language_code: LocaleCode = EN_US, auth_key: Optional[str] = None, max_retries: int = 5
    ) -> List[KnowledgeGraphEntity]:
        """
        Performs Named Entity Linking on a text. It only finds entities which are accessible by the user identified by
        the auth key.

        Parameters
        ----------
        text: str
            Text where the entities shall be tagged in.
        language_code: LanguageCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        auth_key: Optional[str] (default:=None)
            Auth key identifying a user within the Wacom personal knowledge service.
        max_retries: int (default:=5)
            Maximum number of retries, if the service is not available.
        Returns
        -------
        entities: List[KnowledgeGraphEntity]
            List of knowledge graph entities.
        """
        raise NotImplementedError

    @property
    def supported_language(self) -> List[str]:
        """List of supported languages."""
        return self.LANGUAGES

    def is_language_supported(self, language_code: LocaleCode) -> bool:
        """Is the language_code code supported by the engine.

        Parameters
        -----------
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.

        Returns
        -------
        flag: bool
            Flag if this language_code code is supported.
        """
        return language_code in self.supported_language

    def __repr__(self):
        return f"Personal Entity Linking:= {self.service_url}"


class NamedEntityRecognitionProcessor(WacomServiceAPIClient):
    """
    NamedEntityRecognitionProcessor
    -------------------------------
    Service that recognizes entities.

    Parameters
    ----------
    service_url: str
        URL where the service has been deployed
    supported_languages: List[str] = None
        List of supported languages
    verify_calls: bool (default:=False)
        Verifies all HTTPS calls and the associated certificate.
    """

    def __init__(self, service_url: str, supported_languages: List[LocaleCode] = None, verify_calls: bool = False):
        super().__init__(
            application_name="Named Entity Linking",
            service_url=service_url,
            service_endpoint="graph",
            verify_calls=verify_calls,
        )
        self.__supported_languages: List[LocaleCode] = supported_languages if supported_languages else []

    @abc.abstractmethod
    def named_entities(self, text: str, language_code: LocaleCode = EN_US) -> List[NamedEntity]:
        """
        Performs Named Entity Recognition on a text.

        Parameters
        ----------
        text: str
            Text where the entities shall be tagged in.
        language_code: LocaleCode (default:= 'en_US')
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.

        Returns
        -------
        entities: List[NamedEntity]
            List of knowledge named entities.
        """
        raise NotImplementedError

    @property
    def supported_language(self) -> List[LocaleCode]:
        """List of supported languages."""
        return self.__supported_languages

    def is_language_supported(self, language_code: LocaleCode) -> bool:
        """Is the language_code code supported by the engine.

        Parameters
        ----------
        language_code: LanguageCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.

        Returns
        -------
        flag: bool
            Flag if this language_code code is supported
        """
        return language_code in self.supported_language

    def __repr__(self):
        return f"Public entity linking:= {self.__service_url}"


class PublicEntityLinkingProcessor(RESTAPIClient):
    """
    Public Entity Linking
    ---------------------
    Service that links entities to a public entity in a knowledge graph.

    Parameters
    ----------
    service_url: str
        URL where the service has been deployed
    supported_languages: List[str] = None
        List of supported languages
    verify_calls: bool (default:=False)
        Verifies all HTTPS calls and the associated certificate.
    """

    def __init__(
        self,
        service_url: str,
        provider: str = "external",
        supported_languages: List[str] = None,
        verify_calls: bool = False,
    ):
        super().__init__(service_url=service_url, verify_calls=verify_calls)
        self.__provider: str = provider
        self.__supported_languages: List[str] = supported_languages if supported_languages else []

    @abc.abstractmethod
    def link_public_entities(self, text: str, language_code: LocaleCode = EN_US) -> List[KnowledgeGraphEntity]:
        """
        Performs Named Entity Linking on a text. It only finds entities within a large public knowledge graph.

        Parameters
        ----------
        text: str
            Text where the entities shall be tagged in.
        language_code: LanguageCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.

        Returns
        -------
        entities: List[KnowledgeGraphEntity]
            List of public knowledge entities.
        """
        raise NotImplementedError

    @property
    def supported_language(self) -> List[str]:
        """List of supported languages."""
        return self.__supported_languages

    def is_language_supported(self, language_code: LocaleCode) -> bool:
        """
        Is the language_code code supported by the engine.

        Parameters
        ----------
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.

        Returns
        -------
        flag: bool
            Flag if this language_code code is supported
        """
        return language_code in self.supported_language

    @property
    def provider(self) -> str:
        """Provider of the service."""
        return self.__provider

    def __repr__(self):
        return f"Public Entity Linking:= {self.service_url}"
