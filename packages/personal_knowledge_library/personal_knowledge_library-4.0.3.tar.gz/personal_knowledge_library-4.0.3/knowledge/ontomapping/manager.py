# -*- coding: utf-8 -*-
# Copyright © 2023-present Wacom. All rights reserved.
import time
from datetime import datetime, timezone
from typing import Optional, Any, List, Dict, Tuple, Set

import loguru

from knowledge.base.entity import Label, LanguageCode, Description
from knowledge.base.language import LOCALE_LANGUAGE_MAPPING, LocaleCode, LANGUAGE_LOCALE_MAPPING, EN_US
from knowledge.base.ontology import (
    ThingObject,
    DataProperty,
    SYSTEM_SOURCE_SYSTEM,
    SYSTEM_SOURCE_REFERENCE_ID,
    OntologyClassReference,
    OntologyPropertyReference,
    ObjectProperty,
)
from knowledge.ontomapping import (
    ClassConfiguration,
    TOPIC_CLASS,
    PropertyConfiguration,
    PropertyType,
    get_mapping_configuration,
)
from knowledge.public.cache import WikidataCache
from knowledge.public.client import WikiDataAPIClient
from knowledge.public.wikidata import WikidataThing, WikidataClass, WikidataProperty
from knowledge.utils.wikipedia import get_wikipedia_summary

logger = loguru.logger
# Initialize the cache
cache: WikidataCache = WikidataCache()


def flatten(hierarchy: WikidataClass, use_names: bool = False) -> List[str]:
    """
    Flattens the hierarchy.

    Parameters
    ----------
    hierarchy: WikidataClass
        Hierarchy
    use_names: bool
        Use names instead of QIDs.

    Returns
    -------
    hierarchy: List[str]
        Hierarchy

    """
    hierarchy_list: List[str] = [hierarchy.qid]
    jobs: List[WikidataClass] = [hierarchy]
    while len(jobs) > 0:
        job: WikidataClass = jobs.pop()
        if use_names:
            hierarchy_list.append(f"{job.qid} ({job.label})")
        else:
            hierarchy_list.append(job.qid)
        for c in job.superclasses:
            if use_names:
                if f"{job.qid} ({job.label})" not in hierarchy_list:
                    jobs.append(c)
            elif c.qid not in hierarchy_list:
                jobs.append(c)
    return hierarchy_list


def wikidata_taxonomy(qid: str) -> Optional[WikidataClass]:
    """
    Returns the taxonomy of a Wikidata thing.
    Parameters
    ----------
    qid: str
        Wikidata QID.

    Returns
    -------
    hierarchy: WikidataClass
        Hierarchy.
    """
    hierarchy: Dict[str, WikidataClass] = WikiDataAPIClient.superclasses(qid)
    if qid not in hierarchy:
        logger.warning(f"Taxonomy for {qid} not found.")
        return None
    return hierarchy.get(qid)


def convert_dict(structure: Dict[str, Any], locale: str) -> Optional[str]:
    """
    Converts a dictionary to a string.
    Parameters
    ----------
    structure:  Dict[str, Any]
        Dictionary to convert.
    locale: str
        Locale.

    Returns
    -------
    string: str
        String representation of the dictionary.
    """
    if "type" in structure and "value" in structure:
        structure_type: str = structure["type"]
        value: Any = structure["value"]
        if structure_type == "time" and isinstance(value, dict) and "iso" in value and value["iso"]:
            return value["iso"]
        if structure_type == "time" and isinstance(value, dict):
            return value["time"]
        if structure_type == "quantity" and isinstance(value, dict):
            return value["amount"]
        if structure_type == "wikibase-item" and isinstance(value, dict):
            qid: str = value["id"]
            if cache.qid_in_cache(qid):
                wikidata_data: WikidataThing = cache.get_wikidata_object(qid)
            else:
                wikidata_data: WikidataThing = WikiDataAPIClient.retrieve_entity(qid)
            if locale in wikidata_data.label:
                return wikidata_data.label[locale].content
        if structure_type == "external-id":
            return value
        if structure_type == "string":
            return value
        if structure_type == "monolingualtext" and isinstance(value, dict):
            if LOCALE_LANGUAGE_MAPPING.get(LocaleCode(locale)) == LanguageCode(value["language"]):
                return value["text"]
            return None
        if structure_type == "globe-coordinate" and isinstance(value, dict):
            return f'{value["latitude"]},{value["longitude"]}'
        if structure_type == "url" and isinstance(value, str):
            return value
    raise NotImplementedError()


def wikidata_to_thing(
    wikidata_thing: WikidataThing,
    all_relations: Dict[str, Any],
    supported_locales: List[str],
    all_wikidata_objects: Dict[str, WikidataThing],
    pull_wikipedia: bool = False,
    guess_concept_type: bool = True,
) -> Tuple[ThingObject, List[Dict[str, Any]]]:
    """
    Converts a Wikidata thing to a ThingObject.

    Parameters
    ----------
    wikidata_thing: WikidataThing
        Wikidata thing

    all_relations: Dict[str, Any]
        All relations.

    supported_locales: List[str]
        Supported locales.

    all_wikidata_objects: Dict[str, WikidataThing]
        All Wikidata objects.

    pull_wikipedia: bool
        Pull Wikipedia summary.

    guess_concept_type: bool
        Guess the concept type (queries all super types from Wikidata).

    Returns
    -------
    thing: ThingObject
        Thing object
    import_warnings: List[Dict[str, Any]]
        Errors

    """
    import_warnings: List[Dict[str, Any]] = []
    qid: str = wikidata_thing.qid
    labels_entity: List[Label] = []
    aliases_entity: List[Label] = []
    supported_languages: List[str] = [
        LOCALE_LANGUAGE_MAPPING[locale] for locale in supported_locales if locale in LOCALE_LANGUAGE_MAPPING
    ]
    # Make sure that the main label are added to labels and aliases to aliases.
    main_languages: Set[str] = set()
    t1: float = time.perf_counter()
    for la in wikidata_thing.label.values():
        if str(la.language_code) in supported_locales:
            if str(la.language_code) not in main_languages:
                main_languages.add(str(la.language_code))
                labels_entity.append(Label(content=la.content, language_code=la.language_code, main=True))
            else:
                aliases_entity.append(Label(content=la.content, language_code=la.language_code, main=False))
    for lang, aliases in wikidata_thing.aliases.items():
        if str(lang) in supported_locales:
            if str(lang) not in main_languages:
                main_languages.add(str(lang))
                labels_entity.append(Label(content=aliases[0].content, language_code=LocaleCode(lang), main=True))
                for alias in aliases[1:]:
                    aliases_entity.append(Label(content=alias.content, language_code=LocaleCode(lang), main=False))
            else:
                for alias in aliases:
                    aliases_entity.append(Label(content=alias.content, language_code=LocaleCode(lang), main=False))
    t2: float = time.perf_counter()
    descriptions: List[Description] = []
    if "wiki" in wikidata_thing.sitelinks and pull_wikipedia:
        for lang, title in wikidata_thing.sitelinks["wiki"].titles.items():
            if str(lang) in supported_languages:
                locale: LocaleCode = LANGUAGE_LOCALE_MAPPING.get(LanguageCode(lang), EN_US)
                if locale in supported_locales:
                    try:
                        descriptions.append(
                            Description(
                                description=get_wikipedia_summary(title, lang), language_code=LocaleCode(locale)
                            )
                        )
                    except Exception as e:
                        logger.error(f"Failed to get Wikipedia summary for {title} ({lang}): {e}")
    if len(descriptions) == 0:
        descriptions = list(wikidata_thing.description.values())
    t3: float = time.perf_counter()
    # Create the thing
    thing: ThingObject = ThingObject(label=labels_entity, description=descriptions, icon=wikidata_thing.image(dpi=500))
    thing.alias = aliases_entity
    thing.add_source_system(DataProperty(content="wikidata", property_ref=SYSTEM_SOURCE_SYSTEM, language_code=EN_US))
    thing.add_source_reference_id(
        DataProperty(content=qid, property_ref=SYSTEM_SOURCE_REFERENCE_ID, language_code=EN_US)
    )
    thing.add_data_property(
        DataProperty(
            content=datetime.now(timezone.utc).isoformat(),
            property_ref=OntologyPropertyReference.parse("wacom:core#lastUpdate"),
        )
    )
    t4: float = time.perf_counter()
    class_types: List[str] = wikidata_thing.ontology_types
    if guess_concept_type:
        for cls in wikidata_thing.instance_of:
            class_types.append(cls.qid)
    class_configuration: Optional[ClassConfiguration] = get_mapping_configuration().guess_classed(class_types)
    if class_configuration:
        thing.concept_type = class_configuration.concept_type
    else:
        thing.concept_type = OntologyClassReference.parse(TOPIC_CLASS)
    t5: float = time.perf_counter()
    relation_props: Dict[OntologyPropertyReference, List[str]] = {}
    for pid, cl in wikidata_thing.claims.items():
        prop: Optional[PropertyConfiguration] = get_mapping_configuration().guess_property(pid, thing.concept_type)
        if prop and prop.type == PropertyType.DATA_PROPERTY:
            property_type: OntologyPropertyReference = OntologyPropertyReference.parse(prop.iri)
            for locale in supported_locales:
                for c in cl.literals:
                    try:
                        if isinstance(c, dict):
                            content: Optional[str] = convert_dict(c, locale)
                            if get_mapping_configuration().check_data_property_range(property_type, content):
                                thing.add_data_property(
                                    DataProperty(
                                        content=content, property_ref=property_type, language_code=LocaleCode(locale)
                                    )
                                )
                        elif isinstance(c, (str, float, int)):
                            thing.add_data_property(
                                DataProperty(content=c, property_ref=property_type, language_code=LocaleCode(locale))
                            )
                    except NotImplementedError as e:
                        import_warnings.append({"qid": qid, "pid": pid, "error": str(e)})
    t6: float = time.perf_counter()
    for relation in all_relations.get(qid, []):
        prop: Optional[PropertyConfiguration] = get_mapping_configuration().guess_property(
            relation["predicate"]["pid"], thing.concept_type
        )
        target_thing: Optional[WikidataThing] = all_wikidata_objects.get(relation["target"]["qid"])
        if target_thing:
            if prop and prop.type == PropertyType.OBJECT_PROPERTY:
                class_types: List[str] = [c.qid for c in target_thing.instance_of]
                class_types.extend(target_thing.ontology_types)
                target_config: Optional[ClassConfiguration] = get_mapping_configuration().guess_classed(class_types)
                if target_config:
                    if get_mapping_configuration().check_object_property_range(
                        prop, thing.concept_type, target_config.concept_type
                    ):
                        property_type: OntologyPropertyReference = OntologyPropertyReference.parse(prop.iri)
                        if property_type not in relation_props:
                            relation_props[property_type] = []
                        relation_props[property_type].append(relation["target"]["qid"])
                    else:
                        prop_missing: WikidataProperty = WikidataProperty(pid=relation["predicate"]["pid"])
                        import_warnings.append(
                            {
                                "source_qid": qid,
                                "source_concept": thing.concept_type,
                                "source_classes": class_types,
                                "property": prop_missing.pid,
                                "target_qid": target_thing.qid,
                                "target_classes": target_thing.ontology_types,
                            }
                        )
            else:
                prop_missing: WikidataProperty = WikidataProperty(pid=relation["predicate"]["pid"])
                import_warnings.append(
                    {
                        "source_qid": qid,
                        "source_concept": thing.concept_type,
                        "source_classes": class_types,
                        "property": prop_missing.pid,
                        "target_qid": target_thing.qid,
                        "target_classes": target_thing.ontology_types,
                    }
                )
    for p, lst in relation_props.items():
        thing.add_relation(ObjectProperty(p, outgoing=lst))
    t7: float = time.perf_counter()
    logger.debug(
        f"Wikidata to Thing: {(t2 - t1) * 1000.:.2f} ms for labels, {(t3 - t2) * 1000.:.2f} ms for descriptions, "
        f"{(t4 - t3) * 1000.:.2f} ms for sources, {(t5 - t4) * 1000.:.2f} ms for class types, "
        f"{(t6 - t5) * 1000.:.2f} ms for data properties, {(t7 - t6) * 1000.:.2f} ms for object properties"
    )
    return thing, import_warnings
