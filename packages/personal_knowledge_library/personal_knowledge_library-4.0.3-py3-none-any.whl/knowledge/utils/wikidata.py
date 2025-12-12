# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
from typing import Any, Dict, List

from knowledge import logger
from knowledge.base.entity import LanguageCode, IMAGE_TAG, STATUS_FLAG_TAG, Description, Label
from knowledge.base.language import LANGUAGE_LOCALE_MAPPING, LocaleCode
from knowledge.base.ontology import ThingObject, OntologyClassReference


# ----------------------------------------------- Helper functions -----------------------------------------------------
def update_language_code(lang: LanguageCode) -> LocaleCode:
    """Update the language_code code to a default language_code / country code
    Parameters
    ----------
    lang: LanguageCode
        Language code.

    Returns
    -------
    language_code: LocaleCode
        Language code.

    Raises
    ------
    ValueError
        If the language_code code is not supported.
    """
    if lang not in LANGUAGE_LOCALE_MAPPING:
        raise ValueError(f"Language code {lang} not supported.")
    return LANGUAGE_LOCALE_MAPPING[lang]


def localized_list_description(entity_dict: Dict[str, str]) -> List[Description]:
    """
    Creates a list of descriptions for the given entity dictionary.
    Parameters
    ----------
    entity_dict: Dict[str, str]
        Entities dictionary.

    Returns
    -------
    descriptions: List[Description]
        List of descriptions.
    """
    return [Description(cont, update_language_code(LanguageCode(lang))) for lang, cont in entity_dict.items()]


def localized_list_label(entity_dict: Dict[str, str]) -> List[Label]:
    """
    Creates a list of labels for the given entity dictionary.

    Parameters
    ----------
    entity_dict: Dict[str, str]
        Entities dictionary.

    Returns
    -------
    labels: List[Label]
        List of labels.
    """
    return [
        Label(cont, update_language_code(LanguageCode(lang)), main=True)
        for lang, cont in entity_dict.items()
        if cont != ""
    ]


def localized_flatten_alias_list(entity_dict: Dict[str, List[str]]) -> List[Label]:
    """
    Flattens the alias list.
    Parameters
    ----------
    entity_dict: Dict[str, List[str]]
        Entities dictionary.

    Returns
    -------
    flatten: List[Label]
        Flattened list of labels.
    """
    flatten: List[Label] = []
    for language, items in entity_dict.items():
        for i in items:
            if i != "":
                flatten.append(Label(i, update_language_code(LanguageCode(language)), main=False))
    return flatten


def from_dict(entity: Dict[str, Any], concept_type: OntologyClassReference) -> ThingObject:
    """
    Create a thing object from a dictionary.
    Parameters
    ----------
    entity: Dict[str, Any]
        Entities dictionary.
    concept_type: OntologyClassReference
        Concept type.

    Returns
    -------
    thing: ThingObject
        Thing object.
    """
    labels: List[Label] = localized_list_label(entity["label"])
    description: List[Description] = localized_list_description(entity["description"])
    alias: List[Label] = localized_flatten_alias_list(entity["alias"])
    if IMAGE_TAG in entity:
        icon: str = entity[IMAGE_TAG]
    else:
        logger.warning(f"Entity has no image: {entity}")
        icon: str = ""
    # Create the entity
    thing: ThingObject = ThingObject(label=labels, concept_type=concept_type, description=description, icon=icon)
    thing.alias = alias
    if STATUS_FLAG_TAG in entity:
        thing.status_flag = entity[STATUS_FLAG_TAG]
    return thing


# --------------------------------------------------- Utilities --------------------------------------------------------


def strip(url: str) -> str:
    """Strip qid from url.
    Parameters
    ----------
    url: str
        URL
    Returns
    -------
    result: str
        Stripped URL
    """
    parts = url.split("/")
    return parts[-1]


def build_query(params: Dict[str, Any]) -> List[str]:
    """
    Build of query.

    Parameters
    ----------
    params:
        Parameters for query

    Returns
    -------
    queries: List[str]
        SPARQL query string
    """
    filters: List[Dict[str, Any]] = params.get("filters")
    dynamics: Dict[str, Any] = params.get("dynamic-filters")
    limit: int = params.get("limit", 1000)
    lang_code: str = params.get("language_code", "en")
    filter_string: str = ""
    queries: List[str] = []
    for f in filters:
        filter_string += f"?item wdt:{f['property']}  wd:{f['target']}.\n"
    if dynamics:
        property_str: str = dynamics["property"]
        for v in dynamics["targets"]:
            dyn: str = filter_string + f"?item wdt:{property_str}  wd:{v}.\n"
            query: str = f"""SELECT DISTINCT ?item ?itemLabel WHERE {{
              {dyn}SERVICE wikibase:label {{ bd:serviceParam wikibase:language \"[AUTO_LANGUAGE],{lang_code}\". }}
            }}
            LIMIT {limit}
            """
            queries.append(query)
    else:
        query: str = f"""SELECT DISTINCT ?item ?itemLabel WHERE {{
          {filter_string}SERVICE wikibase:label {{ bd:serviceParam wikibase:language \"[AUTO_LANGUAGE],{lang_code}\". }}
        }}
        LIMIT {limit}
        """
        queries.append(query)
    return queries


def extract_qid(url: str) -> str:
    """
    Extract qid from url.
    Parameters
    ----------
    url: str
        URL

    Returns
    -------
    qid: str
        QID
    """
    parts: List[str] = url.split("/")
    return parts[-1]
