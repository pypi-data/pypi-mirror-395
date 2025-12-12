# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import abc
import enum
from typing import Any, List, Dict, Union

from knowledge.base.language import LocaleCode, LanguageCode, EN_US


#  ---------------------------------------- Exceptions -----------------------------------------------------------------
class ServiceException(Exception):
    """Service exception."""


class KnowledgeException(Exception):
    """Knowledge exception."""


#  ---------------------------------------- Constants ------------------------------------------------------------------
RDF_SYNTAX_NS_TYPE: str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
RDF_SCHEMA_COMMENT: str = "http://www.w3.org/2000/01/rdf-schema#comment"
RDF_SCHEMA_LABEL: str = "http://www.w3.org/2000/01/rdf-schema#label"
ALIAS_TAG: str = "alias"
DATA_PROPERTY_TAG: str = "literal"
VALUE_TAG: str = "value"
LANGUAGE_TAG: str = "lang"
LOCALE_TAG: str = "locale"
DATA_PROPERTIES_TAG: str = "literals"
SEND_TO_NEL_TAG: str = "sendToNEL"
SEND_VECTOR_INDEX_TAG: str = "sendToVectorIndex"
SOURCE_REFERENCE_ID_TAG: str = "source_reference_id"
EXTERNAL_USER_ID_TAG: str = "external_user_id"
SOURCE_SYSTEM_TAG: str = "source_system"
OBJECT_PROPERTIES_TAG: str = "relations"
OWNER_TAG: str = "owner"
OWNER_ID_TAG: str = "ownerId"
GROUP_IDS: str = "groupIds"
LOCALIZED_CONTENT_TAG: str = "LocalizedContent"
STATUS_FLAG_TAG: str = "status"
CONTENT_TAG: str = "value"
URI_TAG: str = "uri"
URIS_TAG: str = "uris"
FORCE_TAG: str = "force"
ERRORS_TAG: str = "errors"
TEXT_TAG: str = "text"
TYPE_TAG: str = "type"
IMAGE_TAG: str = "image"
DESCRIPTION_TAG: str = "description"
COMMENT_TAG: str = "text"
COMMENTS_TAG: str = "comments"
DESCRIPTIONS_TAG: str = "descriptions"
REPOSITORY_TAG: str = "repository"
DISPLAY_TAG: str = "display"
USE_NEL_TAG: str = "use_for_nel"
USE_VECTOR_INDEX_TAG: str = "use_for_vector_index"
USE_VECTOR_DOCUMENT_INDEX_TAG: str = "use_for_vector_document_index"
USE_FULLTEXT_TAG: str = "user_full_text"
TARGETS_TAG: str = "targets"
VISIBILITY_TAG: str = "visibility"
RELATIONS_TAG: str = "relations"
INCLUDE_RELATIONS_TAG: str = "includeRelations"
LABELS_TAG: str = "labels"
IS_MAIN_TAG: str = "isMain"
DATA_TYPE_TAG: str = "dataType"
RELATION_TAG: str = "relation"
OUTGOING_TAG: str = "out"
INCOMING_TAG: str = "in"
TENANT_RIGHTS_TAG: str = "tenantRights"
INFLECTION_CONCEPT_CLASS: str = "concept"
INFLECTION_SETTING: str = "inflection"
INFLECTION_CASE_SENSITIVE: str = "caseSensitive"
# ------------------------------------------ Indexing targets ----------------------------------------------------------
INDEXING_NEL_TARGET: str = "NEL"
INDEXING_VECTOR_SEARCH_TARGET: str = "VectorSearchWord"
INDEXING_VECTOR_SEARCH_DOCUMENT_TARGET: str = "VectorSearchDocument"
INDEXING_FULLTEXT_TARGET: str = "ElasticSearch"


class EntityStatus(enum.Enum):
    """
    Entity Status
    -------------
    Status of the entity synchronization (client and knowledge graph).
    """

    UNKNOWN = 0
    """Unknown status."""
    CREATED = 1
    """Entity has been created and not yet update."""
    UPDATED = 2
    """Entity has been updated by the client and must be synced."""
    SYNCED = 3
    """State of entity is in sync with knowledge graph."""


class LocalizedContent(abc.ABC):
    """
    Localized content
    -----------------
    Content that is multilingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LanguageCode (default:= 'en_US')
        ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
    """

    def __init__(self, content: str, language_code: Union[LocaleCode, LanguageCode]):
        self.__content: str = content
        self.__language_code: Union[LocaleCode, LanguageCode] = language_code

    @property
    def content(self) -> str:
        """String representation of the content."""
        return self.__content

    @content.setter
    def content(self, value: str):
        self.__content = value

    @property
    def language_code(self) -> Union[LocaleCode, LanguageCode]:
        """Locale"""
        return self.__language_code

    def __repr__(self):
        return f"{self.content}@{self.language_code}"


class Label(LocalizedContent):
    """
    Label
    -----
    Label that is multilingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LocaleCode (default:= 'en_US')
        ISO-3166 Country Codes and ISO-639 Language Codes in the format <language_code>_<country>, e.g., en_US.
    main: bool (default:=False)
        Main content
    """

    def __init__(self, content: str, language_code: LocaleCode = EN_US, main: bool = False):
        self.__main: bool = main
        super().__init__(content, language_code)

    @property
    def main(self) -> bool:
        """Flag if the content is the  main content or an alias."""
        return self.__main

    @staticmethod
    def create_from_dict(
        dict_label: Dict[str, Any], tag_name: str = CONTENT_TAG, locale_name: str = LOCALE_TAG
    ) -> "Label":
        """
        Create a label from a dictionary.
        Parameters
        ----------
        dict_label: Dict[str, Any]
            Dictionary containing the label information.
        tag_name: str
            Tag name of the content.
        locale_name: str
            Tag name of the language code.

        Returns
        -------
        instance: Label
            The Label instance.
        """
        if tag_name not in dict_label:
            raise ValueError("Dict is does not contain a localized label.")
        if locale_name not in dict_label:
            raise ValueError("Dict is does not contain a language code")
        if IS_MAIN_TAG in dict_label:
            return Label(dict_label[tag_name], LocaleCode(dict_label[locale_name]), dict_label[IS_MAIN_TAG])
        return Label(dict_label[tag_name], LocaleCode(dict_label[locale_name]))

    @staticmethod
    def create_from_list(param: List[dict]) -> List[LOCALIZED_CONTENT_TAG]:
        """
        Create a list of labels from a list of dictionaries.

        Parameters
        ----------
        param: List[dict]
            List of dictionaries containing the label information.

        Returns
        -------
        instance: List[Label]
            List of label instances.
        """
        return [Label.create_from_dict(p) for p in param]

    def __dict__(self):
        return {CONTENT_TAG: self.content, LOCALE_TAG: self.language_code, IS_MAIN_TAG: self.main}


class Description(LocalizedContent):
    """
    Description
    -----------
    Description that is multilingual.

    Parameters
    ----------
    description: str
        Description value
    language_code: LanguageCode (default:= 'en_US')
        Language code of content
    """

    def __init__(self, description: str, language_code: LocaleCode = EN_US):
        super().__init__(description, language_code)

    @staticmethod
    def create_from_dict(
        dict_description: Dict[str, Any], tag_name: str = DESCRIPTION_TAG, locale_name: str = LOCALE_TAG
    ) -> "Description":
        """
        Create a description from a dictionary.

        Parameters
        ----------
        dict_description: Dict[str, Any]
            Dictionary containing the description information.
        tag_name: str
            Tag name of the content.
        locale_name:
            Tag name of the language code.

        Returns
        -------
        instance: Description
            The description instance.
        """
        if tag_name not in dict_description or locale_name not in dict_description:
            raise ValueError("Dict is does not contain a localized label.")
        return Description(dict_description[tag_name], LocaleCode(dict_description[locale_name]))

    @staticmethod
    def create_from_list(param: List[Dict[str, Any]]) -> List["Description"]:
        """Create a list of descriptions from a list of dictionaries.

        Parameters
        ----------
        param: List[Dict[str, Any]]
            List of dictionaries containing the description information.

        Returns
        -------
        instance: List[Description]
            List of description instances.
        """
        return [Description.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            DESCRIPTION_TAG: self.content,
            LOCALE_TAG: self.language_code,
        }
