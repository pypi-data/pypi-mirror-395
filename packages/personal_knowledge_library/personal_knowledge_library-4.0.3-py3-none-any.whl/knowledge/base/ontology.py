# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import abc
import enum
from datetime import datetime
from json import JSONEncoder
from typing import Union, Optional, Any, List, Dict, Tuple, Set

import loguru
from rdflib import Literal, RDFS, OWL, URIRef, RDF, Graph

from knowledge.base.access import TenantAccessRight
from knowledge.base.entity import (
    EntityStatus,
    Label,
    Description,
    URI_TAG,
    IMAGE_TAG,
    DESCRIPTIONS_TAG,
    LABELS_TAG,
    TYPE_TAG,
    STATUS_FLAG_TAG,
    DATA_PROPERTIES_TAG,
    OBJECT_PROPERTIES_TAG,
    GROUP_IDS,
    OWNER_TAG,
    OWNER_ID_TAG,
    SOURCE_REFERENCE_ID_TAG,
    SOURCE_SYSTEM_TAG,
    TENANT_RIGHTS_TAG,
    LOCALE_TAG,
    IS_MAIN_TAG,
    USE_NEL_TAG,
    VALUE_TAG,
    DATA_PROPERTY_TAG,
    VISIBILITY_TAG,
    INFLECTION_CASE_SENSITIVE,
    INFLECTION_SETTING,
    INFLECTION_CONCEPT_CLASS,
    LANGUAGE_TAG,
    CONTENT_TAG,
    DATA_TYPE_TAG,
    RELATION_TAG,
    INCOMING_TAG,
    OUTGOING_TAG,
    COMMENT_TAG,
    LocalizedContent,
    COMMENTS_TAG,
    USE_VECTOR_INDEX_TAG,
    SEND_VECTOR_INDEX_TAG,
    USE_FULLTEXT_TAG,
    TARGETS_TAG,
    INDEXING_NEL_TARGET,
    INDEXING_VECTOR_SEARCH_TARGET,
    INDEXING_FULLTEXT_TARGET,
    USE_VECTOR_DOCUMENT_INDEX_TAG,
    INDEXING_VECTOR_SEARCH_DOCUMENT_TARGET,
    EXTERNAL_USER_ID_TAG,
    DESCRIPTION_TAG,
)
from knowledge.base.language import EN_US, SUPPORTED_LOCALES, EN, LanguageCode, LocaleCode

# ---------------------------------------------- Vocabulary base URI ---------------------------------------------------
PREFIX: str = "xsd"
BASE_URI: str = "http://www.w3.org/2001/XMLSchema#"
RESOURCE: str = "http://www.w3.org/2000/01/rdf-schema#Resource"
# ---------------------------------------------------- Constants -------------------------------------------------------
SUB_CLASS_OF_TAG: str = "subClassOf"
TENANT_ID: str = "tenantId"
NAME_TAG: str = "name"
SEND_TO_NEL: str = "sendToNEL"
# ---------------------------------------------------- RDFLib ----------------------------------------------------------
PREFERRED_LABEL: URIRef = URIRef("wacom:core#prefLabel")
logger = loguru.logger


# ---------------------------------------------------- Ontology --------------------------------------------------------
class PropertyType(enum.Enum):
    """
    PropertyType
    -----------
    Within the ontology two different property types are defined. A data- and an object property.
    """

    OBJECT_PROPERTY = "Relation"
    DATA_PROPERTY = "Literal"


INVERSE_PROPERTY_TYPE: Dict[str, PropertyType] = {pt.value: pt for pt in PropertyType}


class DataPropertyType(enum.Enum):
    """
    DataPropertyType.
    -----------------
    Data types that are used by Datatype properties.
    """

    STRING = BASE_URI + "string"
    """Character strings (but not all Unicode character strings) """
    BOOLEAN = BASE_URI + "boolean"
    """boolean: true, false"""
    DECIMAL = BASE_URI + "decimal"
    """Arbitrary-precision decimal numbers"""
    INTEGER = BASE_URI + "integer"
    """Arbitrary-size integer numbers"""
    DOUBLE = BASE_URI + "double"
    """64-bit floating point numbers incl. ±Inf, ±0, NaN"""
    FLOAT = BASE_URI + "float"
    """32-bit floating point numbers incl. ±Inf, ±0, NaN"""
    DATE = BASE_URI + "date"
    """Dates (yyyy-mm-dd) with or without timezone"""
    TIME = BASE_URI + "time"
    """Times (hh:mm:ss.sss…) with or without timezone"""
    DATE_TIME = BASE_URI + "dateTime"
    """Date and time with or without timezone"""
    DATE_TIMESTAMP = BASE_URI + "dateTimeStamp"
    """Date and time with required timezone """
    G_YEAR = BASE_URI + "gYear"
    """Gregorian calendar year"""
    G_MONTH = BASE_URI + "gMonth"
    """Gregorian calendar month"""
    G_DAY = BASE_URI + "gDay"
    """Gregorian calendar day of the month"""
    G_YEAR_MONTH = BASE_URI + "gYearMonth"
    """Gregorian calendar year and month"""
    G_MONTH_DAY = BASE_URI + "gMonthDay"
    """Gregorian calendar month and day"""
    DURATION = BASE_URI + "duration"
    """Duration of time"""
    YEAR_MONTH_DURATION = BASE_URI + "yearMonthDuration"
    """Duration of time (months and years only)"""
    DAYTIME_DURATION = BASE_URI + "dayTimeDuration"
    """Duration of time (days, hours, minutes, seconds only)"""
    BYTES = BASE_URI + "byte"
    """-128…+127 (8 bit)"""
    SHORT = BASE_URI + "short"
    """-32768… + 32767 (16 bit)"""
    INT = BASE_URI + "int"
    """-2147483648…+2147483647 (32 bit)"""
    LONG = BASE_URI + "long"
    """-9223372036854775808…+9223372036854775807 (64 bit)"""
    UNSIGNED_BYTE = BASE_URI + "unsignedByte"
    """0 … 255 (8 bit)"""
    UNSIGNED_SHORT = BASE_URI + "unsignedShort"
    """0 … 65535 (16 bit)"""
    UNSIGNED_INT = BASE_URI + "unsignedInt"
    """ 0 … 4294967295 (32 bit)"""
    UNSIGNED_LONG = BASE_URI + "unsignedLong"
    """  0 … 18446744073709551615 (64 bit)"""
    POSITIVE_INTEGER = BASE_URI + "positiveInteger"
    """Integer numbers > 0 """
    NON_NEGATIVE_INTEGER = BASE_URI + "nonNegativeInteger"
    """Integer numbers ≥ 0"""
    NEGATIVE_INTEGER = BASE_URI + "negativeInteger"
    """Integer numbers ≤ 0"""
    NON_POSITIVE_INTEGER = BASE_URI + "nonPositiveInteger"
    """Integer numbers ≤ 0"""
    HEX_BINARY = BASE_URI + "hexBinary"
    """Hex-encoded binary data"""
    BASE64_BINARY = BASE_URI + "base64Binary"
    """Base64-encoded binary data"""
    ANY_URI = BASE_URI + "anyURI"
    """Absolute or relative URIs and IRIs"""
    LANGUAGE = BASE_URI + "language_code"
    """Language tags per http://tools.ietf.org/html/bcp47"""
    NORMALIZED = BASE_URI + "normalizedString"
    """Whitespace-normalized strings"""
    TOKEN = BASE_URI + "token"
    """Tokenized strings"""
    NM_TOKEN = BASE_URI + "NMTOKEN"
    """XML NMTOKENs"""
    NAME = BASE_URI + "Name"
    """XML Names"""
    NC_NAME = BASE_URI + "NCName"
    """XML NCNames"""


INVERSE_DATA_PROPERTY_TYPE_MAPPING: Dict[str, DataPropertyType] = {
    str(lit_type.value): lit_type for lit_type in DataPropertyType
}
"""Maps the string representation of the XSD data types to the data types enum constants."""


# ------------------------------------------ Ontology References -------------------------------------------------------


class OntologyLabel(LocalizedContent):
    """
    Ontology Label
    --------------
    Label that is multilingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LanguageCode (default:= 'en')
        Language code of content
    main: bool (default:=False)
        Main content
    """

    def __init__(self, content: str, language_code: LanguageCode = EN, main: bool = False):
        self.__main: bool = main
        super().__init__(content, language_code)

    @property
    def main(self) -> bool:
        """Flag if the content is the  main content or an alias."""
        return self.__main

    @staticmethod
    def create_from_dict(
        dict_label: Dict[str, Any], tag_name: str = CONTENT_TAG, locale_name: str = LOCALE_TAG
    ) -> "OntologyLabel":
        """
        Create a label from a dictionary.

        Parameters
        ----------
        dict_label: Dict[str, Any]
            Dictionary with the label information
        tag_name: str
            Tag name of the content
        locale_name: str
            Tag name of the language code

        Returns
        -------
        instance: OntologyLabel
            Instance of the label
        """
        if tag_name not in dict_label:
            raise ValueError("Dict is does not contain a localized label.")
        if locale_name not in dict_label:
            raise ValueError("Dict is does not contain a language code")
        if IS_MAIN_TAG in dict_label:
            return OntologyLabel(dict_label[tag_name], LanguageCode(dict_label[locale_name]), dict_label[IS_MAIN_TAG])
        return OntologyLabel(dict_label[tag_name], LanguageCode(dict_label[locale_name]))

    @staticmethod
    def create_from_list(param: List[dict]) -> List["OntologyLabel"]:
        """
        Create a list of labels from a list of dictionaries.
        Parameters
        ----------
        param: List[dict]
            List of dictionaries with the label information

        Returns
        -------
        instances: List[OntologyLabel]
            List of label instances
        """
        return [OntologyLabel.create_from_dict(p) for p in param]

    def __dict__(self):
        return {CONTENT_TAG: self.content, LOCALE_TAG: self.language_code, IS_MAIN_TAG: self.main}


class OntologyObjectReference(abc.ABC):
    """
    Ontology class type
    ------------------
    Associated to an entity to link the type of the entity.

    Parameters
    ----------
    scheme: str
        Scheme or owner of the ontology object
    context: str
        Context of ontology object
    name: str
        Ontology object reference name
    """

    def __init__(self, scheme: str, context: str, name: str):
        self.__scheme: str = scheme
        self.__context: str = context
        self.__name: str = name

    @property
    def scheme(self):
        """Scheme."""
        return self.__scheme

    @property
    def context(self):
        """Context."""
        return self.__context

    @property
    def name(self):
        """Name."""
        return self.__name

    @property
    def iri(self):
        """Internationalized Resource Identifier (IRI) encoded ontology class name."""
        return f"{self.scheme}:{self.context}#{self.name}"

    def __repr__(self):
        return self.iri

    @classmethod
    def parse_iri(cls, iri: str) -> Tuple[str, str, str]:
        """Parse an IRI into its components.

        Parameters
        ----------
        iri: str
            IRI to parse

        Returns
        -------
        Tuple[str, str, str]
            Scheme, context and name of the IRI
        """
        if iri is None:
            raise ValueError("IRI cannot be None")
        if ":" not in iri or "#" not in iri:
            raise ValueError(f"Invalid IRI: {iri}")
        colon_idx: int = iri.index(":")
        hash_idx: int = iri.index("#")
        scheme: str = iri[:colon_idx]
        context: str = iri[colon_idx + 1 : hash_idx]
        name: str = iri[hash_idx + 1 :]
        return scheme, context, name


class OntologyClassReference(OntologyObjectReference):
    """
    Ontology class type
    -------------------
    Associated to an ontology class.

    Parameters
    ----------
    scheme: str
        Scheme or owner
    context: str
        Context of class
    class_name: str
        Class name
    """

    def __init__(self, scheme: str, context: str, class_name: str):
        super().__init__(scheme, context, class_name)

    @property
    def class_name(self):
        """Class name."""
        return self.name

    @classmethod
    def parse(cls, iri: str) -> "OntologyClassReference":
        """Parse IRI to create an ontology class reference.

        Parameters
        ----------
        iri: str
            IRI of ontology class reference

        Returns
        -------
        instance: OntologyClassReference
            Instance of ontology class reference
        """
        scheme, context, name = OntologyObjectReference.parse_iri(iri)
        return OntologyClassReference(scheme, context, name)

    def __eq__(self, other):
        if not isinstance(other, OntologyClassReference):
            return False
        return self.iri == other.iri

    def __hash__(self):
        return hash(self.iri)


class OntologyPropertyReference(OntologyObjectReference):
    """
    Property reference
    ------------------
    Associated to an ontology property.

    Parameters
    ----------
    scheme: str
        Scheme or owner
    context: str
        Context of class
    property_name: str
        Property name
    """

    def __init__(self, scheme: str, context: str, property_name: str):
        super().__init__(scheme, context, property_name)

    @property
    def property_name(self):
        """Property name."""
        return self.name

    @classmethod
    def parse(cls, iri: str) -> "OntologyPropertyReference":
        """Parses an IRI into an OntologyPropertyReference.

        Parameters
        ----------
        iri: str
            IRI to parse

        Returns
        -------
        instance: OntologyPropertyReference
            Instance of OntologyPropertyReference
        """
        scheme, context, name = OntologyObjectReference.parse_iri(iri)
        return OntologyPropertyReference(scheme, context, name)

    def __eq__(self, other):
        if not isinstance(other, OntologyPropertyReference):
            return False
        return self.iri == other.iri

    def __hash__(self):
        return hash(self.iri)


# ---------------------------------------------------- Classes Constants -----------------------------------------------
THING_CLASS: OntologyClassReference = OntologyClassReference("wacom", "core", "Thing")
# ---------------------------------------------------- Property Constants ----------------------------------------------
SYSTEM_SOURCE_SYSTEM: OntologyPropertyReference = OntologyPropertyReference("wacom", "core", "sourceSystem")
SYSTEM_SOURCE_REFERENCE_ID: OntologyPropertyReference = OntologyPropertyReference("wacom", "core", "sourceReferenceId")
CREATION_DATE: OntologyPropertyReference = OntologyPropertyReference.parse("wacom:core#creationDate")
LAST_UPDATE_DATE: OntologyPropertyReference = OntologyPropertyReference.parse("wacom:core#lastUpdate")


class Comment(LocalizedContent):
    """
    Comment
    -------
    Comment that is multi-lingual.

    Parameters
    ----------
    text: str
        Text value
    language_code: LanguageCode (default:= 'en')
        Language code of content
    """

    def __init__(self, text: str, language_code: LanguageCode = "en"):
        super().__init__(text, language_code)

    @staticmethod
    def create_from_dict(dict_description: Dict[str, Any]) -> "Comment":
        """
        Create a comment from a dictionary.
        Parameters
        ----------
        dict_description: Dict[str, Any]
            Dictionary containing the comment

        Returns
        -------
        instance: Comment
            Instance of comment
        """
        if VALUE_TAG not in dict_description or LANGUAGE_TAG not in dict_description:
            raise ValueError("Dict is does not contain a localized comment.")
        return Comment(dict_description[VALUE_TAG], dict_description[LANGUAGE_TAG])

    @staticmethod
    def create_from_list(param: List[Dict[str, Any]]) -> List["Comment"]:
        """
        Create a list of comments from a list of dictionaries.
        Parameters
        ----------
        param: List[Dict[str, Any]]
            List of dictionaries containing the comments

        Returns
        -------
        instances: List[Comment]
            List of instances of comments
        """
        return [Comment.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            COMMENT_TAG: self.content,
            LOCALE_TAG: self.language_code,
        }


class OntologyObject(abc.ABC):
    """
    Generic ontology object
    -----------------------

    Parameters
    ----------
    tenant_id: str
        Reference id for tenant
    iri: str
        IRI of the ontology object
    icon: str
        Icon assigned to object, visually representing it
    labels: List[Label]
        List of multi-language_code labels
    comments: List[Label]
        List of multi-language_code comments
    context: str
        Context
    """

    def __init__(
        self, tenant_id: str, iri: str, icon: str, labels: List[OntologyLabel], comments: List[Comment], context: str
    ):
        self.__tenant_id: str = tenant_id
        self.__labels: List[OntologyLabel] = labels
        self.__comments: List[Comment] = comments
        self.__iri: str = iri
        self.__icon: str = icon
        self.__context: str = context

    @property
    def tenant_id(self) -> str:
        """Tenant id."""
        return self.__tenant_id

    @property
    def iri(self) -> str:
        """IRI"""
        return self.__iri

    @property
    def context(self) -> str:
        """Context."""
        return self.__context

    @property
    def icon(self) -> str:
        """Icon."""
        return self.__icon

    @icon.setter
    def icon(self, value: str):
        self.__icon = value

    @property
    def labels(self) -> List[OntologyLabel]:
        """Labels related to ontology object."""
        return self.__labels

    def label_for_lang(self, language_code: LanguageCode) -> Optional[OntologyLabel]:
        """
        Get label for language_code.
        Parameters
        ----------
        language_code: LanguageCode
            Language code

        Returns
        -------
        label: Optional[OntologyLabel]
            Label for language_code
        """
        for label in self.labels:
            if label.language_code == language_code:
                return label
        return None

    @property
    def comments(self) -> List[Comment]:
        """Comment related to ontology object."""
        return self.__comments

    def comment_for_lang(self, language_code: LanguageCode) -> Optional[Comment]:
        """
        Get comment for language_code.
        Parameters
        ----------
        language_code: LanguageCode
            Language code

        Returns
        -------
        comment: Optional[Comment]
            Comment for language_code
        """
        for comment in self.comments:
            if comment.language_code == language_code:
                return comment
        return None


class OntologyContextSettings:
    """
    OntologyContextSettings
    -----------------------
    Describes the settings of the context, such as:
    - prefixes for RDF, RDFS and OWL
    - Base literal URI
    - Base class URI
    - Description literal name
    - depth
    """

    def __init__(
        self,
        rdf_prefix: str,
        rdfs_prefix: str,
        owl_prefix: str,
        base_literal_uri: str,
        base_class_uri: str,
        description_literal_name: str,
        depth: int,
    ):
        self.__rdf_prefix: str = rdf_prefix
        self.__rdfs_prefix: str = rdfs_prefix
        self.__owl_prefix: str = owl_prefix
        self.__base_literal_uri: str = base_literal_uri
        self.__base_class_uri: str = base_class_uri
        self.__description_literal_name: str = description_literal_name
        self.__depth: int = depth

    @property
    def rdf_prefix(self):
        """RDF prefix"""
        return self.__rdf_prefix

    @property
    def rdfs_prefix(self):
        """RDFS prefix"""
        return self.__rdfs_prefix

    @property
    def owl_prefix(self):
        """OWL prefix"""
        return self.__owl_prefix

    @property
    def base_literal_uri(self):
        """Base literal URI."""
        return self.__base_literal_uri

    @property
    def base_class_uri(self):
        """Base class URI."""
        return self.__base_class_uri

    @property
    def description_literal_name(self) -> str:
        """Literal name of the description."""
        return self.__description_literal_name

    @property
    def depth(self) -> int:
        """Depth."""
        return self.__depth


class OntologyContext(OntologyObject):
    """
    OntologyContext
    ----------------
    Ontology context representation.

    Parameters
    ----------
    cid: str
        Context id
    tenant_id: str
        Tenant id.
    name: str
        Name of the ontology context
    icon: str
        Icon or Base64 encoded
    labels: List[Label]
        List of labels
    comments: List[Comment]
        List of comments
    context: str
        context name
    base_uri: str
        Base URI
    concepts: List[str]
        List of classes / concepts
    properties: List[str]
        List of properties (data and object properties)
    """

    def __init__(
        self,
        cid: str,
        tenant_id: str,
        name: str,
        icon: str,
        labels: List[OntologyLabel],
        comments: List[Comment],
        date_added: datetime,
        date_modified: datetime,
        context: str,
        base_uri: str,
        version: int,
        orphaned: bool,
        concepts: List[str],
        properties: List[str],
    ):
        self.__id = cid
        self.__base_uri: str = base_uri
        self.__version: int = version
        self.__date_added: datetime = date_added
        self.__date_modified: datetime = date_modified
        self.__orphaned: bool = orphaned
        self.__concepts: List[str] = concepts
        self.__properties: List[str] = properties
        super().__init__(tenant_id, name, icon, labels, comments, context)

    @property
    def id(self) -> str:
        """Context id."""
        return self.__id

    @property
    def base_uri(self) -> str:
        """Base URI."""
        return self.__base_uri

    @property
    def orphaned(self) -> bool:
        """Orphaned."""
        return self.__orphaned

    @property
    def version(self) -> int:
        """Version."""
        return self.__version

    @property
    def date_added(self) -> datetime:
        """Date added."""
        return self.__date_added

    @property
    def date_modified(self) -> datetime:
        """Date modified."""
        return self.__date_modified

    @property
    def concepts(self) -> List[str]:
        """List of concepts."""
        return self.__concepts

    @property
    def properties(self) -> List[str]:
        """List of properties."""
        return self.__properties

    @classmethod
    def from_dict(cls, context_dict: Dict[str, Any]):
        """
        Create OntologyContext from dictionary.

        Parameters
        ----------
        context_dict: Dict[str, Any]
            Dictionary containing the context data.

        Returns
        -------
        instance: OntologyContext
            Instance of OntologyContext object.
        """
        context_data: Dict[str, Any] = context_dict["context"]
        labels: List[OntologyLabel] = (
            []
            if context_data["labels"] is None
            else [Label(content=la[VALUE_TAG], language_code=la[LANGUAGE_TAG]) for la in context_data["labels"]]
        )
        comments: List[Comment] = (
            []
            if context_data["comments"] is None
            else [Comment(text=la[VALUE_TAG], language_code=la[LANGUAGE_TAG]) for la in context_data["comments"]]
        )
        added: datetime = datetime.fromisoformat(context_data["dateAdded"])
        modified: datetime = datetime.fromisoformat(context_data["dateModified"])
        return OntologyContext(
            context_data["id"],
            context_data["tenantId"],
            context_data["name"],
            context_data["icon"],
            labels,
            comments,
            added,
            modified,
            context_data["context"],
            context_data["baseURI"],
            context_dict["version"],
            context_data["orphaned"],
            context_dict.get("concepts"),
            context_dict.get("properties"),
        )

    def __repr__(self):
        return f"<OntologyContext> - [id:={self.id}, iri:={self.iri}]"


class OntologyClass(OntologyObject):
    """
    OntologyClass
    ----------------
    Concept for ontology.

    Parameters
    ----------
    tenant_id: str
        Tenant id for ontology
    context: str
        Context
    reference: OntologyClassReference
        Reference for ontology class
    icon: str
        Icon representing concept
    labels: List[Label]
        List of labels
    comments: List[Comment]
        List of comments

    subclass_of: str (default: None)
        Subclass of ontology class
    """

    def __init__(
        self,
        tenant_id: str,
        context: str,
        reference: OntologyClassReference,
        subclass_of: OntologyClassReference = None,
        icon: Optional[str] = None,
        labels: Optional[List[OntologyLabel]] = None,
        comments: Optional[List[Comment]] = None,
    ):
        self.__subclass_of: OntologyClassReference = subclass_of
        self.__reference: OntologyClassReference = reference
        super().__init__(tenant_id, reference.iri, icon, labels, comments, context)

    @property
    def subclass_of(self) -> Optional[OntologyClassReference]:
        """
        Superclass of the class.
        """
        return self.__subclass_of

    @property
    def reference(self) -> OntologyClassReference:
        """
        Reference of ontology class.
        """
        return self.__reference

    def __repr__(self):
        return f"<OntologyClass> - [reference:={self.reference}, subclass_of:={self.subclass_of}]"

    @classmethod
    def from_dict(cls, concept_dict: Dict[str, Any]):
        """Create OntologyClass from dictionary.

        Parameters
        ----------
        concept_dict: Dict[str, Any]
            Dictionary containing the concept data.

        Returns
        -------
        instance: OntologyClass
            Instance of OntologyClass object.
        """
        labels: List[OntologyLabel] = (
            []
            if concept_dict[LABELS_TAG] is None
            else [
                OntologyLabel(content=la[VALUE_TAG], language_code=la[LANGUAGE_TAG]) for la in concept_dict[LABELS_TAG]
            ]
        )
        comments: List[Comment] = (
            []
            if concept_dict[COMMENTS_TAG] is None
            else [Comment(text=la[VALUE_TAG], language_code=la[LANGUAGE_TAG]) for la in concept_dict[COMMENTS_TAG]]
        )
        return OntologyClass(
            tenant_id=concept_dict[TENANT_ID],
            context=concept_dict["context"],
            reference=OntologyClassReference.parse(concept_dict[NAME_TAG]),
            subclass_of=(
                OntologyClassReference.parse(concept_dict[SUB_CLASS_OF_TAG])
                if SUB_CLASS_OF_TAG in concept_dict
                else None
            ),
            icon=concept_dict["icon"],
            labels=labels,
            comments=comments,
        )

    @classmethod
    def new(cls) -> "OntologyClass":
        """
        Create new ontology class.

        Returns
        -------
        instance: OntologyClass
            New ontology class.
        """
        return OntologyClass("", "", THING_CLASS)


class OntologyProperty(OntologyObject):
    """
    Ontology Property
    -----------------
    Property ontology object.

    Parameters
    ----------
    kind: str
        Kind of relation
    tenant_id: str
        Tenant id
    context: str
        Context
    name: OntologyPropertyReference
        Name of property object
    icon: str
        Icon describing the property
    property_domain: OntologyClassReference
        Domain for the property
    property_range: OntologyClassReference
        Range for the property
    labels: List[Label]
        List of labels (localized)
    comments: List[Comment],
        List of comments
    sub_property_of: str (default: = None)
        Sub property of.
    inverse_property_of: str (optional)
        Inverse property
    """

    def __init__(
        self,
        kind: PropertyType,
        tenant_id: str,
        context: str,
        name: OntologyPropertyReference,
        icon: str = None,
        property_domain: Optional[List[OntologyClassReference]] = None,
        property_range: Optional[List[Union[OntologyClassReference, DataPropertyType]]] = None,
        labels: Optional[List[OntologyLabel]] = None,
        comments: Optional[List[Comment]] = None,
        sub_property_of: Optional[OntologyPropertyReference] = None,
        inverse_property_of: Optional[OntologyPropertyReference] = None,
    ):
        self.__kind: PropertyType = kind
        self.__subproperty_of: OntologyPropertyReference = sub_property_of
        self.__inverse_property_of: OntologyPropertyReference = inverse_property_of
        self.__domains: List[OntologyClassReference] = property_domain if property_domain else []
        self.__ranges: List[Optional[Union[OntologyClassReference, DataPropertyType]]] = (
            property_range if property_range else []
        )
        self.__reference: OntologyPropertyReference = name
        super().__init__(tenant_id, name.iri, icon, labels, comments, context)

    @property
    def is_data_property(self) -> bool:
        """Check if property is data property.

        Returns
        -------
        is_data_property: bool
            True if property is data property, False otherwise.
        """
        return self.kind != PropertyType.OBJECT_PROPERTY

    @property
    def kind(self) -> PropertyType:
        """Kind of the property."""
        return self.__kind

    @property
    def reference(self) -> OntologyPropertyReference:
        """Reference to property"""
        return self.__reference

    @property
    def subproperty_of(self) -> Optional[OntologyPropertyReference]:
        """Reference to the super property"""
        return self.__subproperty_of

    @property
    def inverse_property_of(self) -> Optional[OntologyPropertyReference]:
        """Reference to the inverse property"""
        return self.__inverse_property_of

    @property
    def domains(self) -> List[OntologyClassReference]:
        """Domain of the property."""
        return self.__domains

    @property
    def ranges(self) -> List[Union[OntologyClassReference, DataPropertyType]]:
        """Ranges of the property."""
        return self.__ranges

    def __repr__(self):
        return (
            f"<OntologyProperty> - [name:= {self.iri} domain:={self.domains}, range:={self.ranges}, "
            f"sub-property_of:={self.subproperty_of}, type:={self.kind}]"
        )

    @classmethod
    def from_dict(cls, property_dict: Dict[str, Any]):
        """
        Create ontology property from dictionary.
        Parameters
        ----------
        property_dict: Dict[str, Any]
            Dictionary containing property information.

        Returns
        -------
        instance: OntologyProperty
            Ontology property instance.
        """
        labels: List[OntologyLabel] = (
            []
            if property_dict[LABELS_TAG] is None
            else [OntologyLabel.create_from_dict(la, locale_name=LANGUAGE_TAG) for la in property_dict[LABELS_TAG]]
        )
        comments: List[Comment] = (
            []
            if property_dict["comments"] is None
            else [Comment.create_from_dict(co) for co in property_dict["comments"]]
        )
        return OntologyProperty(
            INVERSE_PROPERTY_TYPE[property_dict["kind"]],
            property_dict["tenantId"],
            property_dict["context"],
            OntologyPropertyReference.parse(property_dict["name"]),
            property_dict["icon"],
            [OntologyClassReference.parse(domain) for domain in property_dict["domains"]],
            [OntologyClassReference.parse(domain) for domain in property_dict["ranges"]],
            labels,
            comments,
            (
                OntologyPropertyReference.parse(property_dict["subPropertyOf"])
                if property_dict.get("subPropertyOf") not in ["", None]
                else None
            ),
            (
                OntologyPropertyReference.parse(property_dict["inverseOf"])
                if property_dict.get("inverseOf") not in ["", None]
                else None
            ),
        )

    @classmethod
    def new(cls, kind: PropertyType) -> "OntologyProperty":
        """
        Create new ontology property.
        Parameters
        ----------
        kind: PropertyType
            Kind of property.

        Returns
        -------
        instance: OntologyProperty
            New ontology property.
        """
        return OntologyProperty(
            kind, "", "", OntologyPropertyReference.parse("http://www.w3.org/2002/07/owl#topObjectProperty")
        )


class EntityProperty(abc.ABC):
    """
    EntityProperty
    --------------
    Abstract class for the different types of properties.
    """


class DataProperty(EntityProperty):
    """
    DataProperty
    ------------
    Data property for entities.

    Parameter
    ---------
    content: Any
        Content
    literal_type: LiteralProperty
        OntologyPropertyReference type
    language_code: str
        Language code
    data_type: str
        Data type
    """

    def __init__(
        self,
        content: Any,
        property_ref: OntologyPropertyReference,
        language_code: LocaleCode = EN_US,
        data_type: DataPropertyType = None,
    ):
        self.__content: Any = content
        self.__language_code: LocaleCode = language_code
        self.__type: OntologyPropertyReference = property_ref
        self.__data_type: Optional[DataPropertyType] = data_type

    @property
    def data_property_type(self) -> OntologyPropertyReference:
        """Ontology type."""
        return self.__type

    @property
    def data_type(self) -> Optional[DataPropertyType]:
        """Data type (optional)."""
        return self.__data_type

    @property
    def value(self) -> Any:
        """Content of the data property."""
        return self.__content

    @property
    def language_code(self) -> LocaleCode:
        """Language code of the content."""
        return self.__language_code

    @staticmethod
    def create_from_dict(data_property_struct: dict):
        """
        Create data property from dictionary.

        Parameters
        ----------
        data_property_struct: dict
            Dictionary containing data property information.

        Returns
        -------
        instance: DataProperty
            Data property instance.
        """
        if (
            CONTENT_TAG not in data_property_struct
            or LOCALE_TAG not in data_property_struct
            and DATA_PROPERTY_TAG not in data_property_struct
        ):
            raise ValueError("Dict is does not contain a data_property structure.")
        data_property_type: str = data_property_struct[DATA_PROPERTY_TAG]
        data_type: DataPropertyType = DataPropertyType.STRING
        if DATA_TYPE_TAG in data_property_struct and data_property_struct[DATA_TYPE_TAG] is not None:
            if data_property_struct[DATA_TYPE_TAG] not in INVERSE_DATA_PROPERTY_TYPE_MAPPING:
                raise ValueError(f"DataProperty data type is not supported. Type: {data_type}")
            data_type = INVERSE_DATA_PROPERTY_TYPE_MAPPING[data_property_struct[DATA_TYPE_TAG]]
        return DataProperty(
            data_property_struct[CONTENT_TAG],
            OntologyPropertyReference.parse(data_property_type),
            data_property_struct[LOCALE_TAG],
            data_type,
        )

    def __dict__(self):
        return {
            CONTENT_TAG: self.value,
            LOCALE_TAG: self.language_code,
            DATA_PROPERTY_TAG: self.data_property_type.iri,
            DATA_TYPE_TAG: None if self.data_type is None else self.data_type.value,
        }

    def __repr__(self):
        return f"{self.value}@{self.language_code}<{self.data_property_type.name}>"

    @staticmethod
    def create_from_list(param: List[dict]) -> List["DataProperty"]:
        """
        Create data property list from dictionary list.

        Parameters
        ----------
        param: List[dict]
            List of dictionaries containing data property information.

        Returns
        -------
        instances: List[DataProperty]
            List of data property instances.
        """
        return [DataProperty.create_from_dict(p) for p in param]


class ObjectProperty(EntityProperty):
    """
    Object Property
    ---------------
    ObjectProperty for entities.

    Parameter
    ---------
    relation: OntologyPropertyReference
        The OntologyPropertyReference type
    incoming: List[str] (default:= [])
        Incoming relations
    outgoing: List[str] (default:= [])
        Outgoing relations
    """

    def __init__(
        self,
        relation: OntologyPropertyReference,
        incoming: Optional[List[Union[str, "ThingObject"]]] = None,
        outgoing: Optional[List[Union[str, "ThingObject"]]] = None,
    ):
        self.__relation: OntologyPropertyReference = relation
        self.__incoming: List[Union[str, "ThingObject"]] = incoming if incoming is not None else []
        self.__outgoing: List[Union[str, "ThingObject"]] = outgoing if outgoing is not None else []

    @property
    def relation(self) -> OntologyPropertyReference:
        """Reference from the ontology."""
        return self.__relation

    @property
    def incoming_relations(self) -> List[Union[str, "ThingObject"]]:
        """Incoming relation"""
        return self.__incoming

    @property
    def outgoing_relations(self) -> List[Union[str, "ThingObject"]]:
        """Outgoing relation"""
        return self.__outgoing

    @staticmethod
    def create_from_dict(relation_struct: Dict[str, Any]) -> Tuple[OntologyPropertyReference, "ObjectProperty"]:
        """
        Create object property from dictionary.

        Parameters
        ----------
        relation_struct: Dict[str, Any]
            Dictionary containing object property information.

        Returns
        -------
        relation_type: OntologyPropertyReference
            The OntologyPropertyReference type
        """
        relation_type: OntologyPropertyReference = OntologyPropertyReference.parse(relation_struct[RELATION_TAG])
        incoming: List[Union[str, ThingObject]] = []

        for incoming_relation in relation_struct[INCOMING_TAG]:
            if isinstance(incoming_relation, dict):
                incoming.append(ThingObject.from_dict(incoming_relation))
            elif isinstance(incoming_relation, str):
                incoming.append(incoming_relation)

        outgoing: List[Union[str, ThingObject]] = []
        for outgoing_relation in relation_struct[OUTGOING_TAG]:
            if isinstance(outgoing_relation, dict):
                outgoing.append(ThingObject.from_dict(outgoing_relation))
            elif isinstance(outgoing_relation, str):
                outgoing.append(outgoing_relation)
        return relation_type, ObjectProperty(relation_type, incoming, outgoing)

    def __dict__(self):
        outgoing_relations: List[str] = []
        incoming_relations: List[str] = []
        for e in self.incoming_relations:

            if isinstance(e, ThingObject):
                if e.uri is not None:
                    incoming_relations.append(e.uri)
                else:
                    incoming_relations.append(e.reference_id)
            else:
                incoming_relations.append(e)
        for e in self.outgoing_relations:
            if isinstance(e, ThingObject):
                if e.uri is not None:
                    outgoing_relations.append(e.uri)
                else:
                    outgoing_relations.append(e.reference_id)
            else:
                outgoing_relations.append(e)
        return {RELATION_TAG: self.relation.iri, INCOMING_TAG: incoming_relations, OUTGOING_TAG: outgoing_relations}

    def __repr__(self):
        return f"{self.relation.iri}, in:={self.incoming_relations}, out:={self.outgoing_relations}"

    @staticmethod
    def create_from_list(param: List[dict]) -> Dict[OntologyPropertyReference, "ObjectProperty"]:
        """
        Create object property list from dictionary list.
        Parameters
        ----------
        param: List[dict]
            List of dictionaries containing object property information.

        Returns
        -------
        instances: Dict[OntologyPropertyReference, ObjectProperty]
            Dictionary of object property instances.
        """
        return dict([ObjectProperty.create_from_dict(p) for p in param])


class Ontology:
    """
    Ontology
    --------
    The ontology consists of classes and properties.
    """

    def __init__(self):
        self.__classes: Dict[OntologyClassReference, OntologyClass] = {}
        self.__data_properties: Dict[str, OntologyProperty] = {}
        self.__object_properties: Dict[str, OntologyProperty] = {}

    def add_class(self, class_obj: OntologyClass):
        """
        Adding class object.

        Parameters
        ----------
        class_obj: OntologyClass
            Class object
        """
        self.__classes[class_obj.reference] = class_obj

    def add_properties(self, prop_obj: OntologyProperty):
        """
        Adding properties.

        Parameters
        ----------
        prop_obj: OntologyProperty
        """
        if prop_obj.is_data_property:
            self.__data_properties[prop_obj.reference.iri] = prop_obj
        else:
            self.__object_properties[prop_obj.reference.iri] = prop_obj

    @property
    def data_properties(self) -> List[OntologyProperty]:
        """All data properties."""
        return list(self.__data_properties.values())

    @property
    def object_properties(self) -> List[OntologyProperty]:
        """All object properties."""
        return list(self.__object_properties.values())

    @property
    def classes(self) -> List[OntologyClass]:
        """All classes."""
        return list(self.__classes.values())

    def __check_hierarchy__(self, clz: OntologyClassReference, domain: OntologyClassReference) -> bool:
        """
        Check if class is in domain.
        Parameters
        ----------
        clz: OntologyClassReference
            Class reference
        domain: OntologyClassReference
            Domain reference

        Returns
        -------
        result: bool
            True if class is in domain.
        """
        current_clz: Optional[OntologyClass] = self.get_class(clz)
        while current_clz is not None:
            if current_clz.reference == domain:
                return True
            current_clz = self.get_class(current_clz.subclass_of)
        return False

    def get_class(self, class_reference: OntologyClassReference) -> Optional[OntologyClass]:
        """
        Get class instance by reference.

        Parameters
        ----------
        class_reference: OntologyClassReference
            Class reference

        Returns
        --------
        instance: Optional[OntologyClass]
            Instance of ontology class.
        """
        return self.__classes.get(class_reference, None)

    def get_object_properties(self, property_reference: OntologyPropertyReference) -> Optional[OntologyProperty]:
        """
        Get object property instance by reference.

        Parameters
        ----------
        property_reference: OntologyPropertyReference
            Property reference

        Returns
        --------
        instance: Optional[OntologyProperty]
            Instance of ontology object property.
        """
        return self.__object_properties.get(property_reference.iri)

    def get_data_properties(self, property_reference: OntologyPropertyReference) -> Optional[OntologyProperty]:
        """
        Get object property instance by reference.

        Parameters
        ----------
        property_reference: OntologyPropertyReference
            Property reference

        Returns
        --------
        instance: Optional[OntologyProperty]
            Instance of ontology object property.
        """
        return self.__data_properties.get(property_reference.iri)

    def data_properties_for(self, cls_reference: OntologyClassReference) -> List[OntologyPropertyReference]:
        """
        Retrieve a list of data properties.

        Parameters
        ----------
        cls_reference: OntologyClassReference
            Class of the ontology

        Returns
        -------
        data_properties: List[OntologyPropertyReference]
            List of data properties, where domain fit for the class of one of its super classes.
        """
        data_properties: List[OntologyPropertyReference] = []
        clz: Optional[OntologyClass] = self.get_class(cls_reference)
        if clz is not None:
            for dp in self.data_properties:
                for domain in dp.domains:
                    if self.__check_hierarchy__(clz.reference, domain):
                        data_properties.append(dp.reference)
        return data_properties

    def object_properties_for(self, cls_reference: OntologyClassReference) -> List[OntologyPropertyReference]:
        """
        Retrieve a list of object properties.

        Parameters
        ----------
        cls_reference: OntologyClassReference
            Class of the ontology

        Returns
        -------
        object_properties: List[OntologyPropertyReference]
            List of object properties, where domain fit for the class of one of its super classes.
        """
        object_properties: List[OntologyPropertyReference] = []
        clz: Optional[OntologyClass] = self.get_class(cls_reference)
        if clz is not None:
            for dp in self.object_properties:
                for domain in dp.domains:
                    if self.__check_hierarchy__(clz.reference, domain):
                        object_properties.append(dp.reference)
        return object_properties

    def __repr__(self):
        return f"<Ontology> : classes:= {self.classes}"


class ThingObject:
    """
    ThingObject
    -----------
    Generic entity within the knowledge graph.

    Each entity is derived from this object, thus all entities share:
    - **uri**: A unique resource identity to identify the entity and reference it in relations
    - **label**: Human understandable label
    - **icon**: Visual representation of the entity
    - **description**: Description of entity
    - **concept_type**: Type of the concept
    - **concept_type_info**: Information on the concept type
    - **visibility**: Visibility of the entity
    - **use_for_nel**: Use the entity for named entity linking

    Parameters
    ----------
    label: List[Label]
        List of labels
    icon: str (optional)
        Icon
    description: List[Description] (optional)
        List of descriptions
    concept_type: OntologyClassReference
        Type of the concept
    uri: str
         URI for entity. For new entities the URI is None, as the knowledge graph backend assigns this.
    tenant_rights: TenantAccessRight
        Rights for tenants
    owner: bool
        Is the logged-in user the owner of the entity
    use_for_nel: bool
        Use the entity for named entity linking
    use_vector_index: bool
        Use vector index for labels
    use_vector_index_document: bool
        Use vector index for document
    use_full_text_index: bool
        Use full text index for entity
    """

    def __init__(
        self,
        label: List[Label] = None,
        concept_type: OntologyClassReference = THING_CLASS,
        description: Optional[List[Description]] = None,
        uri: Optional[str] = None,
        icon: Optional[str] = None,
        tenant_rights: TenantAccessRight = TenantAccessRight(),
        owner: bool = True,
        use_for_nel: bool = True,
        use_vector_index: bool = False,
        use_vector_index_document: bool = False,
        use_full_text_index: bool = True,
    ):
        self.__uri: str = uri
        self.__icon: Optional[str] = icon
        self.__label: List[Label] = label if label else []
        self.__description: List[Description] = description if description else []
        self.__alias: List[Label] = []
        self.__concept_type: OntologyClassReference = concept_type
        self.__data_properties: Dict[OntologyPropertyReference, List[DataProperty]] = {}
        self.__object_properties: Dict[OntologyPropertyReference, ObjectProperty] = {}
        self.__tenants_rights: TenantAccessRight = tenant_rights
        self.__status_flag: EntityStatus = EntityStatus.UNKNOWN
        self.__ontology_types: Optional[Set[str]] = None
        self.__owner: bool = owner
        self.__owner_id: Optional[str] = None
        self.__owner_external_user_id: Optional[str] = None
        self.__group_ids: List[str] = []
        self.__use_for_nel: bool = use_for_nel
        self.__use_vector_index: bool = use_vector_index
        self.__use_vector_index_document: bool = use_vector_index_document
        self.__use_full_text_index: bool = use_full_text_index
        self.__visibility: Optional[str] = None

    @property
    def uri(self) -> str:
        """Unique identifier for entity."""
        return self.__uri

    @uri.setter
    def uri(self, uri: str):
        self.__uri = uri

    @property
    def visibility(self) -> str:
        """Visibility."""
        return self.__visibility

    @visibility.setter
    def visibility(self, vis: str):
        self.__visibility = vis

    @property
    def use_for_nel(self) -> bool:
        """Use the entity for named entity linking."""
        return self.__use_for_nel

    @use_for_nel.setter
    def use_for_nel(self, use_for_nel: bool):
        self.__use_for_nel = use_for_nel

    @property
    def use_full_text_index(self) -> bool:
        """Use full text index for entity."""
        return self.__use_full_text_index

    @use_full_text_index.setter
    def use_full_text_index(self, use_full_text_index: bool):
        self.__use_full_text_index = use_full_text_index

    @property
    def use_vector_index(self) -> bool:
        """Use vector index for entity."""
        return self.__use_vector_index

    @use_vector_index.setter
    def use_vector_index(self, use_vector_index: bool):
        self.__use_vector_index = use_vector_index

    @property
    def use_vector_index_document(self) -> bool:
        """Use vector index for document."""
        return self.__use_vector_index_document

    @use_vector_index_document.setter
    def use_vector_index_document(self, use_vector_index_document: bool):
        self.__use_vector_index_document = use_vector_index_document

    @property
    def owner(self) -> bool:
        """Is current user the owner of the entity."""
        return self.__owner

    @property
    def owner_id(self) -> str:
        """Internal id of the owner."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self.__owner_id = value

    @property
    def owner_external_user_id(self) -> Optional[str]:
        """External user id of the owner."""
        return self.__owner_external_user_id

    @owner_external_user_id.setter
    def owner_external_user_id(self, value: str):
        self.__owner_external_user_id = value

    @property
    def group_ids(self) -> List[str]:
        """List of group ids."""
        return self.__group_ids

    @group_ids.setter
    def group_ids(self, value: List[str]):
        self.__group_ids = value

    @property
    def status_flag(self) -> EntityStatus:
        """Status flag."""
        return self.__status_flag

    @status_flag.setter
    def status_flag(self, flag: EntityStatus):
        self.__status_flag = flag

    @property
    def label(self) -> List[Label]:
        """Labels of the entity."""
        return self.__label

    @label.setter
    def label(self, value: List[Label]):
        self.__label = value

    def add_label(self, label: str, language_code: LocaleCode):
        """Adding a label for entity.

        Parameters
        ----------
        label: str
            Label
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        self.__label.append(Label(label, language_code, True))

    def update_label(self, value: str, language_code: LocaleCode):
        """Update or creates a label for a specific language.

        Parameters
        ----------
        value: str
            Value to be set
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        for label in self.label:
            if label.language_code == language_code:
                label.content = value
                return
        # Label with language does not exist, so create a new label
        self.add_label(value, language_code)

    def remove_label(self, language_code: LocaleCode):
        """
        Remove label for entity if it exists for language.

        Parameters
        ----------
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        for idx, label in enumerate(self.label):
            if label.language_code == language_code:
                del self.label[idx]
                break

    def remove_alias(self, label: Label):
        """
        Remove alias for entity if it exists for language.

        Parameters
        ----------
        label: Label
            Alias label
        """
        for idx, alias in enumerate(self.alias):
            if label.language_code == alias.language_code and label.content == alias.content:
                del self.alias[idx]
                break

    def label_lang(self, language_code: LocaleCode) -> Optional[Label]:
        """
        Get label for language_code code.

        Parameters
        ----------
        language_code: LocaleCode
            Requested language_code code
        Returns
        -------
        label: Optional[Label]
            Returns the label for a specific language code
        """
        for label in self.label:
            if label.language_code == language_code:
                return label
        return None

    def add_source_system(self, value: DataProperty):
        """
        Adding the source system  of the entity.

        Parameters
        -----------
        value: DataProperty
            Adds the source system as a Data Property. **Remark:** The data property must have the property type
            'wacom:core#sourceSystem'.
        """
        if value.data_property_type != SYSTEM_SOURCE_SYSTEM:
            raise ValueError(
                f"Data property {value.data_property_type.iri} not supported. " f"Expected:={SYSTEM_SOURCE_SYSTEM.iri}"
            )
        if SYSTEM_SOURCE_SYSTEM not in self.__data_properties:
            self.__data_properties[SYSTEM_SOURCE_SYSTEM] = []
        for idx in range(0, len(self.__data_properties[SYSTEM_SOURCE_SYSTEM])):
            if self.__data_properties[SYSTEM_SOURCE_SYSTEM][idx].language_code == value.language_code:
                del self.__data_properties[SYSTEM_SOURCE_SYSTEM][idx]
        self.__data_properties[SYSTEM_SOURCE_SYSTEM].append(value)

    @property
    def source_reference_id(self) -> Optional[List[DataProperty]]:
        """Reference id for to the source."""
        if SYSTEM_SOURCE_REFERENCE_ID in self.__data_properties:
            return self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID]
        return None

    def add_source_reference_id(self, value: DataProperty):
        """
        Adding the reference id from the source system of the entity.

        Parameters
        -----------
        value: DataProperty
            Adds the source system reference id as a Data Property.
            **Remark:** The data property must have the property type 'wacom:core#sourceReferenceId'.
        """
        if value.data_property_type != SYSTEM_SOURCE_REFERENCE_ID:
            raise ValueError(
                f"Data property {value.data_property_type.iri} not supported. "
                f"Expected:={SYSTEM_SOURCE_REFERENCE_ID.iri}"
            )
        if SYSTEM_SOURCE_REFERENCE_ID not in self.__data_properties:
            self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID] = []
        len_props: int = len(self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID])
        idx: int = 0
        while idx < len_props:
            if self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID][idx].language_code == value.language_code:
                del self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID][idx]
                len_props -= 1
            idx += 1
        self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID].append(value)

    @property
    def reference_id(self) -> Optional[str]:
        """Default reference id for the entity."""
        if SYSTEM_SOURCE_REFERENCE_ID in self.__data_properties:
            # The en_US is the default language for the source reference id
            for sr in self.data_properties[SYSTEM_SOURCE_REFERENCE_ID]:
                if sr.language_code == EN_US:
                    return sr.value
            if len(self.data_properties[SYSTEM_SOURCE_REFERENCE_ID]) > 0:
                return self.data_properties[SYSTEM_SOURCE_REFERENCE_ID][0].value
        return None

    @reference_id.setter
    def reference_id(self, value: str):
        """
        Setting the default reference id for the entity.

        Parameters
        ----------
        value: str
            Reference id to be set
        """
        if SYSTEM_SOURCE_REFERENCE_ID not in self.__data_properties:
            self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID] = []
        self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID].append(DataProperty(value, SYSTEM_SOURCE_REFERENCE_ID))

    @property
    def source_system(self) -> Optional[str]:
        """Default reference system for the entity."""
        if SYSTEM_SOURCE_SYSTEM in self.__data_properties:
            # The en_US is the default language for the source reference system
            for sr in self.data_properties[SYSTEM_SOURCE_SYSTEM]:
                if sr.language_code == EN_US:
                    return sr.value
            if len(self.data_properties[SYSTEM_SOURCE_SYSTEM]) > 0:
                return self.data_properties[SYSTEM_SOURCE_SYSTEM][0].value
        return None

    @source_system.setter
    def source_system(self, value: str):
        """
        Setting the default reference system for the entity.

        Parameters
        ----------
        value: str
            Reference id to be set
        """
        if SYSTEM_SOURCE_SYSTEM not in self.__data_properties:
            self.__data_properties[SYSTEM_SOURCE_SYSTEM] = []
        self.__data_properties[SYSTEM_SOURCE_SYSTEM].append(DataProperty(value, SYSTEM_SOURCE_SYSTEM))

    def default_source_reference_id(self, language_code: LocaleCode = EN_US) -> Optional[str]:
        """
        Getting the source reference id for a certain language code.

        Parameters
        ----------
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.

        Returns
        -------
        id: str
            Source reference id.
        """
        if SYSTEM_SOURCE_REFERENCE_ID in self.__data_properties:
            for sr in self.data_properties[SYSTEM_SOURCE_REFERENCE_ID]:
                if sr.language_code == language_code:
                    return sr.value
        return None

    def default_source_system(self, language_code: LocaleCode = EN_US) -> Optional[str]:
        """
        Getting the source system for a certain language code.

        Parameters
        ----------
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.

        Returns
        -------
        id: str
            Source system.
        """
        if SYSTEM_SOURCE_SYSTEM in self.__data_properties:
            for sr in self.data_properties[SYSTEM_SOURCE_SYSTEM]:
                if sr.language_code == language_code:
                    return sr.value
        return None

    @property
    def image(self) -> Optional[str]:
        """Image depicting the entities (optional)."""
        return self.__icon

    @image.setter
    def image(self, value: str):
        self.__icon = value

    @property
    def description(self) -> Optional[List[Description]]:
        """Description of the thing (optional)."""
        return self.__description

    @description.setter
    def description(self, value: List[Description]):
        self.__description = value

    def add_description(self, description: str, language_code: LocaleCode):
        """Adding the description for entity.

        Parameters
        ----------
        description: str
            Description
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        self.__description.append(Description(description=description, language_code=language_code))

    def update_description(self, value: str, language_code: LocaleCode):
        """Update or creates a description for a specific language.

        Parameters
        ----------
        value: str
            Value to be set
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        for desc in self.description:
            if desc.language_code == language_code:
                desc.content = value
                return
        # Description with language does not exist, so create a new description
        self.add_description(value, language_code)

    def description_lang(self, language_code: LocaleCode) -> Optional[Description]:
        """
        Get description for entity.

        Parameters
        ----------
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        Returns
        -------
        label: LocalizedContent
            Returns the  label for a specific language_code code
        """
        for desc in self.description:
            if desc.language_code == language_code:
                return desc
        return None

    def remove_description(self, language_code: LocaleCode):
        """
        Remove description for entity if it exists for language.

        Parameters
        ----------
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        for index, description in enumerate(self.description):
            if description.language_code == language_code:
                del self.__description[index]
                break

    @property
    def concept_type(self) -> OntologyClassReference:
        """Concept type."""
        return self.__concept_type

    @concept_type.setter
    def concept_type(self, value: OntologyClassReference):
        self.__concept_type = value

    @property
    def ontology_types(self) -> Set[str]:
        """Ontology types. For public entities."""
        return self.__ontology_types

    @ontology_types.setter
    def ontology_types(self, value: Set[str]):
        self.__ontology_types = value

    @property
    def data_properties(self) -> Dict[OntologyPropertyReference, List[DataProperty]]:
        """Literals of the concept."""
        return self.__data_properties

    @data_properties.setter
    def data_properties(self, data_properties: Dict[OntologyPropertyReference, List[DataProperty]]):
        """Literals of the concept."""
        self.__data_properties = data_properties

    @property
    def object_properties(self) -> Dict[OntologyPropertyReference, ObjectProperty]:
        """Relations of the concept."""
        return self.__object_properties

    @object_properties.setter
    def object_properties(self, relations: Dict[OntologyPropertyReference, ObjectProperty]):
        self.__object_properties = relations

    def data_property_lang(
        self, data_property: OntologyPropertyReference, language_code: LocaleCode
    ) -> List[DataProperty]:
        """
        Get data property for language_code code.

        Parameters
        ----------
        data_property: OntologyPropertyReference
            Data property.
        language_code: LocaleCode
            Requested language_code code
        Returns
        -------
        data_properties: List[DataProperty]
            Returns a list of data properties for a specific language code
        """
        return [d for d in self.data_properties.get(data_property, []) if d.language_code == language_code]

    def remove_data_property(self, data_property: OntologyPropertyReference):
        """Remove data property.

        Parameters
        ----------
        data_property: OntologyPropertyReference
            Data property to be removed.
        """
        self.__data_properties.pop(data_property, None)

    @property
    def alias(self) -> List[Label]:
        """Alternative labels of the concept."""
        return self.__alias

    @alias.setter
    def alias(self, alias: List[Label]):
        self.__alias = alias

    def alias_lang(self, language_code: LocaleCode) -> List[Label]:
        """
        Get alias for language_code code.

        Parameters
        ----------
        language_code: LocaleCode
            Requested language_code code
        Returns
        -------
        aliases: List[Label]
            Returns a list of aliases for a specific language code
        """
        aliases: List[Label] = []
        for alias in self.alias:
            if alias.language_code == language_code:
                aliases.append(alias)
        return aliases

    def update_alias(self, value: str, language_code: LocaleCode):
        """Update or creates an alias for a specific language.

        Parameters
        ----------
        value: str
            Value to be set
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        for a in self.alias:
            if a.language_code == language_code:
                a.content = value
                return
        # Label with language does not exist, so create a new label
        self.add_alias(value, language_code=language_code)

    def add_relation(self, prop: ObjectProperty):
        """Adding a relation to the entity.

        Parameters
        ----------
        prop: ObjectProperty
            Object property that is added
        """
        if prop.relation in self.object_properties:
            self.__object_properties[prop.relation].incoming_relations.extend(prop.incoming_relations)
            self.__object_properties[prop.relation].outgoing_relations.extend(prop.outgoing_relations)
        else:
            self.__object_properties[prop.relation] = prop

    def add_data_property(self, data_property: DataProperty):
        """Add data property to the entity.

        Parameters
        ----------
        data_property: DataProperty
            Data property that is added
        """
        if data_property.data_property_type not in self.__data_properties:
            self.__data_properties[data_property.data_property_type] = []
        self.__data_properties[data_property.data_property_type].append(data_property)

    def add_alias(self, alias: str, language_code: LocaleCode):
        """Adding an alias for entity.

        Parameters
        ----------
        alias: str
            Alias
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        self.__alias.append(Label(alias, language_code, False))

    @property
    def tenant_access_right(self) -> TenantAccessRight:
        """Access rights for tenant."""
        return self.__tenants_rights

    @tenant_access_right.setter
    def tenant_access_right(self, rights: TenantAccessRight):
        self.__tenants_rights = rights

    def __dict__(self):
        labels: List[Dict[str, Any]] = []
        labels.extend([la.__dict__() for la in self.label])
        labels.extend([la.__dict__() for la in self.alias])
        dict_object: Dict[str, Any] = {
            URI_TAG: self.uri,
            IMAGE_TAG: self.image,
            LABELS_TAG: labels,
            DESCRIPTIONS_TAG: [desc.__dict__() for desc in self.description],
            TYPE_TAG: self.concept_type.iri,
            STATUS_FLAG_TAG: self.status_flag.value,
            DATA_PROPERTIES_TAG: {},
            OBJECT_PROPERTIES_TAG: {},
            GROUP_IDS: self.group_ids,
            OWNER_TAG: self.owner,
            OWNER_ID_TAG: self.owner_id,
        }
        for literal_type, items in self.data_properties.items():
            dict_object[DATA_PROPERTIES_TAG][literal_type.iri] = [i.__dict__() for i in items]
        for relation_type, item in self.object_properties.items():
            dict_object[OBJECT_PROPERTIES_TAG][relation_type.iri] = item.__dict__()
        return dict_object

    def __import_format_dict__(
        self, group_ids: List[str] = None, external_user_id: Optional[str] = None, reference_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export the entity to a dictionary.
        Parameters
        ----------
        group_ids: List[str]
            List of group ids
        external_user_id: Optional[str]
            External user id
        reference_id: Optional[str]
            Override the reference id

        Returns
        -------
        dict_object: Dict[str, Any]
            Dictionary of the entity in the import format
        """
        labels: List[Dict[str, Any]] = []
        labels.extend([la.__dict__() for la in self.label])
        labels.extend([la.__dict__() for la in self.alias])
        dict_object: Dict[str, Any] = {
            SOURCE_REFERENCE_ID_TAG: (
                self.default_source_reference_id() if self.source_reference_id is not None else reference_id
            ),
            SOURCE_SYSTEM_TAG: self.source_system,
            IMAGE_TAG: self.image,
            LABELS_TAG: labels,
            DESCRIPTIONS_TAG: [desc.__dict__() for desc in self.description],
            TYPE_TAG: self.concept_type.iri,
            DATA_PROPERTIES_TAG: [],
            OBJECT_PROPERTIES_TAG: [],
            TENANT_RIGHTS_TAG: self.tenant_access_right.to_list(),
            TARGETS_TAG: [],
        }
        # if group ids are set in the object, use these
        if len(self.group_ids) > 0:
            dict_object[GROUP_IDS] = self.group_ids
        # if group ids are passed as parameter, override the ones in the object
        if group_ids is not None:
            dict_object[GROUP_IDS] = group_ids
        if self.use_for_nel:
            dict_object[TARGETS_TAG].append(INDEXING_NEL_TARGET)
        if self.use_vector_index:
            dict_object[TARGETS_TAG].append(INDEXING_VECTOR_SEARCH_TARGET)
        if self.use_vector_index_document:
            dict_object[TARGETS_TAG].append(INDEXING_VECTOR_SEARCH_DOCUMENT_TARGET)
        if self.use_full_text_index:
            dict_object[TARGETS_TAG].append(INDEXING_FULLTEXT_TARGET)
        if external_user_id:
            dict_object[EXTERNAL_USER_ID_TAG] = external_user_id
        for _, items in self.data_properties.items():
            dict_object[DATA_PROPERTIES_TAG].extend([i.__dict__() for i in items])
        for _, item in self.object_properties.items():
            dict_object[OBJECT_PROPERTIES_TAG].append(item.__dict__())
        return dict_object

    @staticmethod
    def from_import_dict(entity: Dict[str, Any]) -> "ThingObject":
        """Creates a ThingObject from a dict.

        Parameters
        ----------
        entity: Dict[str, Any]
            Dictionary that contains the data of the entity

        Returns
        -------
        instance: ThingObject
            The ThingObject that is created from the dict
        """
        labels: List[Label] = []
        alias: List[Label] = []
        descriptions: List[Description] = []
        main_labels: Dict[str, bool] = {}
        source_reference_id: Optional[str] = entity.get(SOURCE_REFERENCE_ID_TAG)
        for label in entity[LABELS_TAG]:
            if label[LOCALE_TAG] in SUPPORTED_LOCALES:
                if label[IS_MAIN_TAG]:
                    main_label: Label = Label.create_from_dict(label)
                    main_labels[label[LOCALE_TAG]] = True
                    labels.append(main_label)
                else:
                    alias_label: Label = Label.create_from_dict(label)
                    if alias_label.language_code not in main_labels:
                        main_labels[alias_label.language_code] = False
                    alias.append(alias_label)
        for lang_code, is_main in main_labels.items():
            if not is_main:
                la_idx: int = 0
                while la_idx < len(alias):
                    # Fix things where there is no main label
                    if alias[la_idx].language_code == lang_code:
                        al: Label = alias[la_idx]
                        labels.append(Label(al.content, al.language_code, main=True))
                        del alias[la_idx]
                    else:
                        la_idx += 1

        for desc in entity[DESCRIPTIONS_TAG]:
            if desc[LOCALE_TAG] in SUPPORTED_LOCALES:
                if desc[DESCRIPTION_TAG] is None:
                    logger.warning(f"Description is None for {desc}")
                else:
                    descriptions.append(Description.create_from_dict(desc))
        # Backwards-compatibility
        use_nel: bool = entity.get(USE_NEL_TAG, False)
        use_vector_index: bool = entity.get(USE_VECTOR_INDEX_TAG, False)
        use_vector_index_document: bool = entity.get(USE_VECTOR_DOCUMENT_INDEX_TAG, False)
        use_full_text_index: bool = entity.get(USE_FULLTEXT_TAG, False)
        # Vector index target
        if INDEXING_VECTOR_SEARCH_TARGET in entity.get(TARGETS_TAG, []):
            use_vector_index = True
        # Vector index document target
        if INDEXING_VECTOR_SEARCH_DOCUMENT_TARGET in entity.get(TARGETS_TAG, []):
            use_vector_index_document = True
        # Full text index target
        if INDEXING_FULLTEXT_TARGET in entity.get(TARGETS_TAG, []):
            use_full_text_index = True
        # Named entity linking target
        if INDEXING_NEL_TARGET in entity.get(TARGETS_TAG, []):
            use_nel = True
        thing: ThingObject = ThingObject(
            label=labels,
            icon=entity[IMAGE_TAG],
            description=descriptions,
            concept_type=OntologyClassReference.parse(entity[TYPE_TAG]),
            use_for_nel=use_nel,
            use_vector_index=use_vector_index,
            use_vector_index_document=use_vector_index_document,
            use_full_text_index=use_full_text_index,
        )
        if EXTERNAL_USER_ID_TAG in entity:
            thing.owner_external_user_id = entity[EXTERNAL_USER_ID_TAG]
        ref_id_found: bool = False
        if DATA_PROPERTIES_TAG in entity:
            if isinstance(entity[DATA_PROPERTIES_TAG], dict):
                for data_property_type_str, data_properties in entity[DATA_PROPERTIES_TAG].items():
                    data_property_type: OntologyPropertyReference = OntologyPropertyReference.parse(
                        data_property_type_str
                    )
                    if data_property_type == SYSTEM_SOURCE_REFERENCE_ID:
                        ref_id_found = True

                    for data_property in data_properties:
                        language_code: LocaleCode = LocaleCode(data_property[LOCALE_TAG])
                        value: str = data_property[VALUE_TAG]
                        if source_reference_id != value:
                            logger.warning(f"Source reference id mismatch: {source_reference_id} != {value}")
                            raise ValueError(f"Source reference id mismatch: {source_reference_id} != {value}")
                        thing.add_data_property(DataProperty(value, data_property_type, language_code))
            elif isinstance(entity[DATA_PROPERTIES_TAG], list):
                for data_property in entity[DATA_PROPERTIES_TAG]:
                    language_code: LocaleCode = LocaleCode(data_property[LOCALE_TAG])
                    value: str = data_property[VALUE_TAG]
                    data_property_type: OntologyPropertyReference = OntologyPropertyReference.parse(
                        data_property[DATA_PROPERTY_TAG]
                    )
                    if data_property_type == SYSTEM_SOURCE_REFERENCE_ID:
                        ref_id_found = True
                        if source_reference_id != value:
                            logger.warning(f"Source reference id mismatch: {source_reference_id} != {value}")
                            raise ValueError(f"Source reference id mismatch: {source_reference_id} != {value}")

                    thing.add_data_property(DataProperty(value, data_property_type, language_code))
        if not ref_id_found and source_reference_id:
            thing.add_data_property(DataProperty(source_reference_id, SYSTEM_SOURCE_REFERENCE_ID))
        elif not ref_id_found and not source_reference_id:
            logger.warning(f"No source reference id found for {thing.label[0]}")
        if OBJECT_PROPERTIES_TAG in entity:
            for object_property in entity[OBJECT_PROPERTIES_TAG]:
                _, obj = ObjectProperty.create_from_dict(object_property)
                thing.add_relation(obj)
        thing.alias = alias
        thing.group_ids = entity.get(GROUP_IDS, [])
        # Finally, retrieve rights
        if TENANT_RIGHTS_TAG in entity:
            thing.tenant_access_right = TenantAccessRight.parse(entity[TENANT_RIGHTS_TAG])
        return thing

    @staticmethod
    def from_dict(entity: Dict[str, Any]) -> "ThingObject":
        """Creates a ThingObject from a dict.

        Parameters
        ----------
        entity: Dict[str, Any]
            Dictionary that contains the data of the entity

        Returns
        -------
        instance: ThingObject
            The ThingObject that is created from the dict
        """
        labels: List[Label] = []
        alias: List[Label] = []
        descriptions: List[Description] = []

        for label in entity[LABELS_TAG]:
            if label[LOCALE_TAG] in SUPPORTED_LOCALES:
                if label[IS_MAIN_TAG]:
                    labels.append(Label.create_from_dict(label))
                else:
                    alias.append(Label.create_from_dict(label))

        for desc in entity[DESCRIPTIONS_TAG]:
            descriptions.append(Description.create_from_dict(desc))

        use_nel: bool = False
        use_vector_index: bool = False
        use_vector_index_document: bool = False
        if TARGETS_TAG in entity:
            use_nel = INDEXING_NEL_TARGET in entity[TARGETS_TAG]
            use_vector_index = INDEXING_VECTOR_SEARCH_TARGET in entity[TARGETS_TAG]
            use_vector_index_document = INDEXING_VECTOR_SEARCH_DOCUMENT_TARGET in entity[TARGETS_TAG]
            use_fulltext_index = INDEXING_FULLTEXT_TARGET in entity[TARGETS_TAG]
        else:
            if USE_NEL_TAG in entity:
                use_nel = entity[USE_NEL_TAG]
            elif SEND_TO_NEL in entity:
                use_nel = entity[SEND_TO_NEL]
            if USE_VECTOR_INDEX_TAG in entity:
                use_vector_index = entity[USE_VECTOR_INDEX_TAG]
            elif SEND_VECTOR_INDEX_TAG in entity:
                use_vector_index = entity[SEND_VECTOR_INDEX_TAG]
            use_fulltext_index = True
        visibility: Optional[str] = entity.get(VISIBILITY_TAG)
        thing: ThingObject = ThingObject(
            label=labels,
            icon=entity[IMAGE_TAG],
            description=descriptions,
            uri=entity[URI_TAG],
            concept_type=OntologyClassReference.parse(entity[TYPE_TAG]),
            owner=entity.get(OWNER_TAG, True),
            use_for_nel=use_nel,
            use_vector_index=use_vector_index,
            use_vector_index_document=use_vector_index_document,
            use_full_text_index=use_fulltext_index,
        )
        thing.visibility = visibility
        thing.owner_id = entity.get(OWNER_ID_TAG)
        thing.group_ids = entity.get(GROUP_IDS)
        if DATA_PROPERTIES_TAG in entity:
            if isinstance(entity[DATA_PROPERTIES_TAG], dict):
                for data_property_type_str, data_properties in entity[DATA_PROPERTIES_TAG].items():
                    data_property_type: OntologyPropertyReference = OntologyPropertyReference.parse(
                        data_property_type_str
                    )
                    for data_property in data_properties:
                        language_code: LocaleCode = LocaleCode(data_property[LOCALE_TAG])
                        value: str = data_property[VALUE_TAG]
                        thing.add_data_property(DataProperty(value, data_property_type, language_code))
            elif isinstance(entity[DATA_PROPERTIES_TAG], list):
                for data_property in entity[DATA_PROPERTIES_TAG]:
                    language_code: LocaleCode = LocaleCode(data_property[LOCALE_TAG])
                    value: str = data_property[VALUE_TAG]
                    data_property_type: OntologyPropertyReference = OntologyPropertyReference.parse(
                        data_property[DATA_PROPERTY_TAG]
                    )
                    thing.add_data_property(DataProperty(value, data_property_type, language_code))
        if OBJECT_PROPERTIES_TAG in entity:
            if isinstance(entity[OBJECT_PROPERTIES_TAG], list):
                for relation_item in entity[OBJECT_PROPERTIES_TAG]:
                    _, obj = ObjectProperty.create_from_dict(relation_item)
                    thing.add_relation(obj)
        thing.alias = alias
        # Finally, retrieve rights
        if TENANT_RIGHTS_TAG in entity and entity[TENANT_RIGHTS_TAG]:
            thing.tenant_access_right = TenantAccessRight.parse(entity[TENANT_RIGHTS_TAG])
        return thing

    def __getstate__(self) -> Dict[str, Any]:
        return self.__dict__()

    def __setstate__(self, state: Dict[str, Any]):
        self.__label: List[Label] = []
        self.__description: List[Description] = []
        self.__alias: List[Label] = []
        self.__data_properties: Dict[OntologyPropertyReference, List[DataProperty]] = {}
        self.__object_properties: Dict[OntologyPropertyReference, ObjectProperty] = {}
        self.__status_flag: EntityStatus = EntityStatus.UNKNOWN
        self.__ontology_types: Optional[Set[str]] = None
        self.__owner_id: Optional[str] = None
        self.__group_ids: List[str] = []
        self.__visibility: Optional[str] = None

        for label in state[LABELS_TAG]:
            if label[LOCALE_TAG] in SUPPORTED_LOCALES:
                if label[IS_MAIN_TAG]:
                    self.__label.append(Label.create_from_dict(label))
                else:
                    self.__alias.append(Label.create_from_dict(label))

        for desc in state[DESCRIPTIONS_TAG]:
            self.__description.append(Description.create_from_dict(desc))

        use_nel: bool = state.get(USE_NEL_TAG, True)
        visibility: Optional[str] = state.get(VISIBILITY_TAG)
        self.__icon = state[IMAGE_TAG]
        self.__uri = state[URI_TAG]
        self.__concept_type = OntologyClassReference.parse(state[TYPE_TAG])
        self.__owner = state.get(OWNER_TAG, True)
        self.__use_for_nel = use_nel
        self.__use_vector_index = state.get(USE_VECTOR_INDEX_TAG, False)
        self.__use_vector_index_document = state.get(USE_VECTOR_DOCUMENT_INDEX_TAG, False)
        self.__use_full_text_index = state.get(USE_FULLTEXT_TAG, True)
        self.__visibility = visibility
        self.__owner_id = state.get(OWNER_ID_TAG)
        self.__group_ids = state.get(GROUP_IDS)
        if DATA_PROPERTIES_TAG in state:
            if isinstance(state[DATA_PROPERTIES_TAG], dict):
                for data_property_type_str, data_properties in state[DATA_PROPERTIES_TAG].items():
                    data_property_type: OntologyPropertyReference = OntologyPropertyReference.parse(
                        data_property_type_str
                    )
                    for data_property in data_properties:
                        language_code: LocaleCode = LocaleCode(data_property[LOCALE_TAG])
                        value: str = data_property[VALUE_TAG]
                        self.add_data_property(DataProperty(value, data_property_type, language_code))
            elif isinstance(state[DATA_PROPERTIES_TAG], list):
                for data_property in state[DATA_PROPERTIES_TAG]:
                    language_code: LocaleCode = LocaleCode(data_property[LOCALE_TAG])
                    value: str = data_property[VALUE_TAG]
                    data_property_type: OntologyPropertyReference = OntologyPropertyReference.parse(
                        data_property[DATA_PROPERTY_TAG]
                    )
                    self.add_data_property(DataProperty(value, data_property_type, language_code))
        if OBJECT_PROPERTIES_TAG in state:
            for object_property in state[OBJECT_PROPERTIES_TAG].values():
                _, obj = ObjectProperty.create_from_dict(object_property)
                self.add_relation(obj)
        # Finally, retrieve rights
        if TENANT_RIGHTS_TAG in state:
            self.tenant_access_right = TenantAccessRight.parse(state[TENANT_RIGHTS_TAG])
        else:
            self.tenant_access_right = TenantAccessRight()

    def __hash__(self):
        return 0

    def __eq__(self, other: Any):
        # another object is equal to self, iff
        # it is an instance of MyClass
        if not isinstance(other, ThingObject):
            return False
        if self.uri != other.uri:
            return False
        other_thing: ThingObject = other
        # Check if the descriptions are different
        if len(self.description) != len(other_thing.description):
            return False
        for desc_file in self.description:
            kg_desc: Optional[Description] = other_thing.description_lang(desc_file.language_code)
            if kg_desc is None or desc_file.content != kg_desc.content:
                return False
        # Difference in vector index
        if self.use_vector_index != other_thing.use_vector_index:
            return False
        # Difference in NEL index
        if self.use_for_nel != other_thing.use_for_nel:
            return False
        if self.use_vector_index_document != other_thing.use_vector_index_document:
            return False

        # Different number of labels
        if len(self.label) != len(other_thing.label):
            return False
        # Check if the labels are different
        for label_file in self.label:
            label_kg_lang: Optional[Label] = other_thing.label_lang(label_file.language_code)
            if label_kg_lang is None or label_file.content != label_kg_lang.content:
                return False

        # Different number of aliases
        if len(self.alias) != len(other_thing.alias):
            return False

        # Check if the aliases are different
        for alias_file in self.alias:
            alias_kg_lang = other_thing.alias_lang(alias_file.language_code)
            if alias_file.content not in [alias.content for alias in alias_kg_lang]:
                return False

        # If the image is different
        if self.image != other_thing.image:
            return False

        # If the data properties are different
        if len(self.data_properties) != len(other_thing.data_properties):
            return False

        for prop, data_properties in self.data_properties.items():
            if prop not in other_thing.data_properties:
                return False
            if len(data_properties) != len(other_thing.data_properties.get(prop, [])):
                return False

            for dp in data_properties:
                if prop not in other_thing.data_properties:
                    return False
                if dp.value not in [d.value for d in other_thing.data_properties.get(prop)]:
                    return False
        return True

    def __repr__(self):
        return (
            f'<{self.concept_type.iri if self.__concept_type else "UNSET"}: uri:={self.uri}, labels:={self.label}, '
            f"tenant access right:={self.tenant_access_right}]>"
        )


# --------------------------------------------- Inflection setting -----------------------------------------------------
class InflectionSetting(abc.ABC):
    """
    Inflection settings
    --------------------

    Parameters
    ----------
    concept: str
        Concept class
    inflection: str
        Inflection setting
    case_sensitive: bool
        Entity labels of the class treated case-sensitive
    """

    def __init__(self, concept: str, inflection: str, case_sensitive: bool):
        self.__concept: OntologyClassReference = OntologyClassReference.parse(concept)
        self.__inflection: str = inflection
        self.__case_sensitive: bool = case_sensitive

    @property
    def concept(self) -> OntologyClassReference:
        """Concept class."""
        return self.__concept

    @property
    def inflection(self) -> str:
        """Inflection setting"""
        return self.__inflection

    @property
    def case_sensitive(self) -> bool:
        """Are entity labels of the class treated case-sensitive."""
        return self.__case_sensitive

    @staticmethod
    def from_dict(entity: Dict[str, Any]) -> "InflectionSetting":
        """
        Create inflection setting from dictionary.
        Parameters
        ----------
        entity: Dict[str, Any]
            Entity dictionary

        Returns
        -------
        instance: InflectionSetting
            Inflection setting instance
        """
        concept_class: str = ""
        inflection_setting: str = ""
        case_sensitive: bool = False
        if INFLECTION_CONCEPT_CLASS in entity:
            concept_class = entity[INFLECTION_CONCEPT_CLASS]
        if INFLECTION_SETTING in entity:
            inflection_setting = entity[INFLECTION_SETTING]
        if INFLECTION_CASE_SENSITIVE in entity:
            case_sensitive = entity[INFLECTION_CASE_SENSITIVE]
        return InflectionSetting(concept=concept_class, inflection=inflection_setting, case_sensitive=case_sensitive)


# -------------------------------------------------- Encoder -----------------------------------------------------------
class ThingEncoder(JSONEncoder):
    """
    Thing encoder
    -------------
    Encoder for ThingObject, Label and Description objects.
    """

    def default(self, o: Any):
        if isinstance(o, (Label, Description, ThingObject)):
            return o.__dict__()
        return str(o)


def ontology_import(rdf_content: str, tenant_id: str = "", context: str = "") -> Ontology:
    """Import Ontology from RDF ontology file.

    Parameters
    ----------
    rdf_content: str
        Content of the RDF content file.
    tenant_id: str (default:= '')
        Tenant ID.
    context: str (default:= '')
        Context file.

    Returns
    -------
    ontology: Ontology
        Instance of ontology.
    """
    rdf_graph: Graph = Graph().parse(data=rdf_content, format="xml")
    ontology: Ontology = Ontology()
    # Parse classes
    for cls_iri in [s for s, p, o in list(rdf_graph.triples((None, RDF.type, OWL.Class)))]:
        subclass_of: Optional[OntologyClassReference] = None
        comments: List[Comment] = []
        labels: List[OntologyLabel] = []
        for _, _, o in list(rdf_graph.triples((cls_iri, RDFS.comment, None))):
            if isinstance(o, Literal):
                comments.append(Comment(str(o), LanguageCode(o.language)))
        for _, _, o in list(rdf_graph.triples((cls_iri, PREFERRED_LABEL, None))):
            if isinstance(o, Literal):
                labels.append(OntologyLabel(str(o), LanguageCode(o.language)))
        for _, _, o in list(rdf_graph.triples((cls_iri, RDFS.subClassOf, None))):
            subclass_of = OntologyClassReference.parse(str(o))
        ontology.add_class(
            OntologyClass(
                tenant_id=tenant_id,
                context=context,
                reference=OntologyClassReference.parse(str(cls_iri)),
                subclass_of=subclass_of,
                labels=labels,
                comments=comments,
            )
        )

    # Parse data properties
    for data_property_iri in [s for s, p, o in list(rdf_graph.triples((None, RDF.type, OWL.DatatypeProperty)))]:
        subproperty_of: Optional[OntologyPropertyReference] = None
        range_prop: List[DataPropertyType] = []
        domain_prop: List[OntologyClassReference] = []
        comments: List[Comment] = []
        labels: List[OntologyLabel] = []
        inverse_prop: Optional[OntologyPropertyReference] = None
        for _, _, obj in list(rdf_graph.triples((data_property_iri, RDFS.range, None))):
            range_prop.append(INVERSE_DATA_PROPERTY_TYPE_MAPPING[str(obj)])
        for _, _, obj in list(rdf_graph.triples((data_property_iri, RDFS.domain, None))):
            domain_prop.append(OntologyClassReference.parse(str(obj)))
        for _, _, obj in list(rdf_graph.triples((data_property_iri, OWL.inverseOf, None))):
            inverse_prop = OntologyPropertyReference.parse(str(obj))
        for _, _, obj in list(rdf_graph.triples((data_property_iri, RDFS.subPropertyOf, None))):
            subproperty_of = OntologyPropertyReference.parse(str(obj))
        for _, _, o in list(rdf_graph.triples((data_property_iri, RDFS.comment, None))):
            if isinstance(o, Literal):
                comments.append(Comment(str(o), LanguageCode(o.language)))
        for _, _, o in list(rdf_graph.triples((data_property_iri, PREFERRED_LABEL, None))):
            if isinstance(o, Literal):
                labels.append(OntologyLabel(str(o), LanguageCode(o.language)))
        ontology.add_properties(
            OntologyProperty(
                kind=PropertyType.DATA_PROPERTY,
                tenant_id=tenant_id,
                context=context,
                name=OntologyPropertyReference.parse(str(data_property_iri)),
                property_range=range_prop,
                property_domain=domain_prop,
                sub_property_of=subproperty_of,
                inverse_property_of=inverse_prop,
                labels=labels,
                comments=comments,
            )
        )
    # Parse object properties
    for object_property_iri in [s for s, p, o in list(rdf_graph.triples((None, RDF.type, OWL.ObjectProperty)))]:
        subproperty_of: Optional[OntologyPropertyReference] = None
        obj_range_prop: List[OntologyClassReference] = []
        domain_prop: List[OntologyClassReference] = []
        inverse_prop: Optional[OntologyPropertyReference] = None
        comments: List[Comment] = []
        labels: List[OntologyLabel] = []
        for _, _, o_range in list(rdf_graph.triples((object_property_iri, RDFS.range, None))):
            obj_range_prop.append(OntologyClassReference.parse(str(o_range)))
        for _, _, o_domain in list(rdf_graph.triples((object_property_iri, RDFS.domain, None))):
            domain_prop.append(OntologyClassReference.parse(str(o_domain)))
        for _, _, o_inverse in list(rdf_graph.triples((object_property_iri, OWL.inverseOf, None))):
            inverse_prop = OntologyPropertyReference.parse(str(o_inverse))
        for _, _, o_sub in list(rdf_graph.triples((object_property_iri, RDFS.subPropertyOf, None))):
            subproperty_of = OntologyPropertyReference.parse(str(o_sub))
        for _, _, o in list(rdf_graph.triples((object_property_iri, RDFS.comment, None))):
            if isinstance(o, Literal):
                comments.append(Comment(str(o), LanguageCode(o.language)))
        for _, _, o in list(rdf_graph.triples((object_property_iri, PREFERRED_LABEL, None))):
            if isinstance(o, Literal):
                labels.append(OntologyLabel(str(o), LanguageCode(o.language)))
        ontology.add_properties(
            OntologyProperty(
                kind=PropertyType.OBJECT_PROPERTY,
                tenant_id=tenant_id,
                context=context,
                name=OntologyPropertyReference.parse(str(object_property_iri)),
                property_range=obj_range_prop,
                property_domain=domain_prop,
                sub_property_of=subproperty_of,
                inverse_property_of=inverse_prop,
            )
        )
    return ontology
