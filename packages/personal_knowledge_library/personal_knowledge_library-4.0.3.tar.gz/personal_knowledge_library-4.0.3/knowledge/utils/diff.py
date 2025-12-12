# -*- coding: utf-8 -*-
# Copyright © 2025-present Wacom. All rights reserved.
from typing import Optional, Any, List, Dict, Tuple

from knowledge.base.entity import Label, Description
from knowledge.base.ontology import ThingObject
from knowledge.services.asyncio.graph import AsyncWacomKnowledgeService
from knowledge.services.graph import WacomKnowledgeService


def diff_entities(
    client: WacomKnowledgeService,
    file_thing: ThingObject,
    kg_thing: ThingObject,
    kg_things: Optional[Dict[str, ThingObject]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Check the differences between the two entities.

    Parameters
    ----------
    client: WacomKnowledgeService
        The client to use.
    file_thing: ThingObject
        The thing to check.
    kg_thing: ThingObject
        The knowledge graph entity to check.
    kg_things: Optional[Dict[str, ThingObject]]
        The entities in the knowledge graph.

    Returns
    -------
    differences: List[Dict[str, Any]]
        The differences.
    difference_data_properties: List[Dict[str, Any]]
        The differences in the data properties.
    difference_object_properties: List[Dict[str, Any]]
        The differences in the object properties.
    """
    # Different number of descriptions
    differences: List[Dict[str, Any]] = []
    # Check if the descriptions are different
    if len(file_thing.description) != len(kg_thing.description):
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "description",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(file_thing.description),
                "file": len(kg_thing.description),
            }
        )
    for desc_file in file_thing.description:
        kg_desc: Optional[Description] = kg_thing.description_lang(desc_file.language_code)
        if kg_desc is None or desc_file.content != kg_desc.content:
            differences.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Description content" if kg_desc else "Missing description",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": kg_desc.content if kg_desc else "",
                    "file": desc_file.content,
                }
            )
    # Difference in vector index
    if file_thing.use_vector_index != kg_thing.use_vector_index:
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "Vector index",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": kg_thing.use_vector_index,
                "file": file_thing.use_vector_index,
            }
        )
    # Difference in NEL index
    if file_thing.use_for_nel != kg_thing.use_for_nel:
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "NEL index",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": kg_thing.use_for_nel,
                "file": file_thing.use_for_nel,
            }
        )

    # Different number of labels
    if len(file_thing.label) != len(kg_thing.label):
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "Number of labels",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(kg_thing.label),
                "file": len(file_thing.label),
            }
        )
    # Check if the labels are different
    for label_file in file_thing.label:
        label_kg_lang: Optional[Label] = kg_thing.label_lang(label_file.language_code)
        if label_kg_lang is None or label_file.content != label_kg_lang.content:
            differences.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Label content" if label_kg_lang else "Missing label",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": label_kg_lang.content if label_kg_lang else "",
                    "file": kg_thing.label[0].content,
                }
            )
    # Different number of aliases
    if len(file_thing.alias) != len(kg_thing.alias):
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "Number of aliases",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(file_thing.alias),
                "file": len(kg_thing.alias),
            }
        )
    # Check if the aliases are different
    for alias_file in file_thing.alias:
        alias_kg_lang = kg_thing.alias_lang(alias_file.language_code)
        if alias_file.content not in [alias.content for alias in alias_kg_lang]:
            differences.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Alias content",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": ", ".join([alias.content for alias in alias_kg_lang]),
                    "file": alias_file.content,
                }
            )
    difference_data_properties: List[Dict[str, Any]] = []
    # If the data properties are different
    if len(file_thing.data_properties) != len(kg_thing.data_properties):
        difference_data_properties.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "data properties",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(file_thing.data_properties),
                "file": len(kg_thing.data_properties),
            }
        )

    for prop, data_properties in file_thing.data_properties.items():
        if prop not in kg_thing.data_properties:
            difference_data_properties.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "missing data properties",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": None,
                    "file": prop,
                }
            )
            continue
        if len(data_properties) != len(kg_thing.data_properties.get(prop, [])):
            difference_data_properties.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Number of data properties values",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": len(data_properties),
                    "file": len(kg_thing.data_properties.get(prop, [])),
                }
            )
        for dp in data_properties:
            if prop not in kg_thing.data_properties:
                difference_data_properties.append(
                    {
                        "concept_type": file_thing.concept_type.name,
                        "type": "Missing data properties",
                        "resource_id": kg_thing.default_source_reference_id(),
                        "uri": kg_thing.uri,
                        "kg": "",
                        "file": dp.value,
                    }
                )
            elif dp.value not in [d.value for d in kg_thing.data_properties.get(prop)]:
                difference_data_properties.append(
                    {
                        "concept_type": file_thing.concept_type.name,
                        "type": "Different data property values",
                        "resource_id": kg_thing.default_source_reference_id(),
                        "uri": kg_thing.uri,
                        "kg": ", ".join([d.value for d in kg_thing.data_properties.get(prop)]),
                        "file": dp.value,
                    }
                )
    difference_object_properties: List[Dict[str, Any]] = []
    if kg_things:
        kg_thing.object_properties = client.relations(kg_thing.uri)
        for rel_type, _ in file_thing.object_properties.items():
            # Check if the object property is missing
            if rel_type not in kg_thing.object_properties:
                difference_object_properties.append(
                    {
                        "concept_type": file_thing.concept_type.name,
                        "type": "Object property missing",
                        "resource_id": kg_thing.default_source_reference_id(),
                        "uri": kg_thing.uri,
                        "kg": "",
                        "file": rel_type.iri,
                    }
                )
            else:
                # Check if the target entity is different (incoming relations)
                for file_target in file_thing.object_properties[rel_type].incoming_relations:
                    ref_obj: Optional[ThingObject] = kg_things.get(file_target)
                    uris_kg: List[str] = [
                        t.uri if isinstance(t, ThingObject) else t
                        for t in kg_thing.object_properties[rel_type].incoming_relations
                    ]
                    if ref_obj is None:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target missing",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": file_target,
                            }
                        )
                    elif ref_obj.uri not in uris_kg:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target not linked",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": f"{ref_obj.uri} (reference id: {ref_obj.default_source_reference_id()})",
                            }
                        )
                # Check if the target entity is different (outgoing relations)
                for file_target in file_thing.object_properties[rel_type].outgoing_relations:
                    ref_obj: Optional[ThingObject] = kg_things.get(file_target)
                    uris_kg: List[str] = [
                        t.uri if isinstance(t, ThingObject) else t
                        for t in kg_thing.object_properties[rel_type].outgoing_relations
                    ]
                    if ref_obj is None:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target missing",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": file_target,
                            }
                        )
                    elif ref_obj.uri not in uris_kg:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target not linked",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": f"{ref_obj.uri} (reference id: {ref_obj.default_source_reference_id()})",
                            }
                        )
    return differences, difference_data_properties, difference_object_properties


async def diff_entities_async(
    client: AsyncWacomKnowledgeService,
    file_thing: ThingObject,
    kg_thing: ThingObject,
    kg_things: Optional[Dict[str, ThingObject]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Check the differences between the two entities.

    Parameters
    ----------
    client: WacomKnowledgeService
        The client to use.
    file_thing: ThingObject
        The thing to check.
    kg_thing: ThingObject
        The knowledge graph entity to check.
    kg_things: Optional[Dict[str, ThingObject]]
        The entities in the knowledge graph.

    Returns
    -------
    differences: List[Dict[str, Any]]
        The differences.
    difference_data_properties: List[Dict[str, Any]]
        The differences in the data properties.
    difference_object_properties: List[Dict[str, Any]]
        The differences in the object properties.
    """
    # Different number of descriptions
    differences: List[Dict[str, Any]] = []
    # Check if the descriptions are different
    if len(file_thing.description) != len(kg_thing.description):
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "description",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(file_thing.description),
                "file": len(kg_thing.description),
            }
        )
    for desc_file in file_thing.description:
        kg_desc: Optional[Description] = kg_thing.description_lang(desc_file.language_code)
        if kg_desc is None or desc_file.content != kg_desc.content:
            differences.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Description content" if kg_desc else "Missing description",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": kg_desc.content if kg_desc else "",
                    "file": desc_file.content,
                }
            )
    # Difference in vector index
    if file_thing.use_vector_index != kg_thing.use_vector_index:
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "Vector index",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": kg_thing.use_vector_index,
                "file": file_thing.use_vector_index,
            }
        )
    # Difference in NEL index
    if file_thing.use_for_nel != kg_thing.use_for_nel:
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "NEL index",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": kg_thing.use_for_nel,
                "file": file_thing.use_for_nel,
            }
        )

    # Different number of labels
    if len(file_thing.label) != len(kg_thing.label):
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "Number of labels",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(kg_thing.label),
                "file": len(file_thing.label),
            }
        )
    # Check if the labels are different
    for label_file in file_thing.label:
        label_kg_lang: Optional[Label] = kg_thing.label_lang(label_file.language_code)
        if label_kg_lang is None or label_file.content != label_kg_lang.content:
            differences.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Label content" if label_kg_lang else "Missing label",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": label_kg_lang.content if label_kg_lang else "",
                    "file": kg_thing.label[0].content,
                }
            )
    # Different number of aliases
    if len(file_thing.alias) != len(kg_thing.alias):
        differences.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "Number of aliases",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(file_thing.alias),
                "file": len(kg_thing.alias),
            }
        )
    # Check if the aliases are different
    for alias_file in file_thing.alias:
        alias_kg_lang = kg_thing.alias_lang(alias_file.language_code)
        if alias_file.content not in [alias.content for alias in alias_kg_lang]:
            differences.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Alias content",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": ", ".join([alias.content for alias in alias_kg_lang]),
                    "file": alias_file.content,
                }
            )
    difference_data_properties: List[Dict[str, Any]] = []
    # If the data properties are different
    if len(file_thing.data_properties) != len(kg_thing.data_properties):
        difference_data_properties.append(
            {
                "concept_type": file_thing.concept_type.name,
                "type": "data properties",
                "resource_id": kg_thing.default_source_reference_id(),
                "uri": kg_thing.uri,
                "kg": len(file_thing.data_properties),
                "file": len(kg_thing.data_properties),
            }
        )

    for prop, data_properties in file_thing.data_properties.items():
        if prop not in kg_thing.data_properties:
            difference_data_properties.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "missing data properties",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": None,
                    "file": prop,
                }
            )
            continue
        if len(data_properties) != len(kg_thing.data_properties.get(prop, [])):
            difference_data_properties.append(
                {
                    "concept_type": file_thing.concept_type.name,
                    "type": "Number of data properties values",
                    "resource_id": kg_thing.default_source_reference_id(),
                    "uri": kg_thing.uri,
                    "kg": len(data_properties),
                    "file": len(kg_thing.data_properties.get(prop, [])),
                }
            )
        for dp in data_properties:
            if prop not in kg_thing.data_properties:
                difference_data_properties.append(
                    {
                        "concept_type": file_thing.concept_type.name,
                        "type": "Missing data properties",
                        "resource_id": kg_thing.default_source_reference_id(),
                        "uri": kg_thing.uri,
                        "kg": "",
                        "file": dp.value,
                    }
                )
            elif dp.value not in [d.value for d in kg_thing.data_properties.get(prop)]:
                difference_data_properties.append(
                    {
                        "concept_type": file_thing.concept_type.name,
                        "type": "Different data property values",
                        "resource_id": kg_thing.default_source_reference_id(),
                        "uri": kg_thing.uri,
                        "kg": ", ".join([d.value for d in kg_thing.data_properties.get(prop)]),
                        "file": dp.value,
                    }
                )
    difference_object_properties: List[Dict[str, Any]] = []
    if kg_things:
        kg_thing.object_properties = await client.relations(kg_thing.uri)
        for rel_type, _ in file_thing.object_properties.items():
            # Check if the object property is missing
            if rel_type not in kg_thing.object_properties:
                difference_object_properties.append(
                    {
                        "concept_type": file_thing.concept_type.name,
                        "type": "Object property missing",
                        "resource_id": kg_thing.default_source_reference_id(),
                        "uri": kg_thing.uri,
                        "kg": "",
                        "file": rel_type.iri,
                    }
                )
            else:
                # Check if the target entity is different (incoming relations)
                for file_target in file_thing.object_properties[rel_type].incoming_relations:
                    ref_obj: Optional[ThingObject] = kg_things.get(file_target)
                    uris_kg: List[str] = [
                        t.uri if isinstance(t, ThingObject) else t
                        for t in kg_thing.object_properties[rel_type].incoming_relations
                    ]
                    if ref_obj is None:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target missing",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": file_target,
                            }
                        )
                    elif ref_obj.uri not in uris_kg:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target not linked",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": f"{ref_obj.uri} (reference id: {ref_obj.default_source_reference_id()})",
                            }
                        )
                # Check if the target entity is different (outgoing relations)
                for file_target in file_thing.object_properties[rel_type].outgoing_relations:
                    ref_obj: Optional[ThingObject] = kg_things.get(file_target)
                    uris_kg: List[str] = [
                        t.uri if isinstance(t, ThingObject) else t
                        for t in kg_thing.object_properties[rel_type].outgoing_relations
                    ]
                    if ref_obj is None:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target missing",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": file_target,
                            }
                        )
                    elif ref_obj.uri not in uris_kg:
                        difference_object_properties.append(
                            {
                                "concept_type": file_thing.concept_type.name,
                                "type": "Object properties target not linked",
                                "resource_id": kg_thing.default_source_reference_id(),
                                "uri": kg_thing.uri,
                                "kg": "",
                                "file": f"{ref_obj.uri} (reference id: {ref_obj.default_source_reference_id()})",
                            }
                        )
    return differences, difference_data_properties, difference_object_properties


def is_different(client: WacomKnowledgeService, thing_file: ThingObject, thing_kg: ThingObject) -> bool:
    """
    Check if the two entities are different.

    Parameters
    ----------
    client: WacomKnowledgeService
        The client to use.
    thing_file: ThingObject
        The thing from the file.
    thing_kg: ThingObject
        The thing from the knowledge graph.

    Returns
    -------
    is_different: bool
        True if the entities are different, False otherwise.
    """
    differences, data_properties_diff, _ = diff_entities(client, thing_file, thing_kg)
    return len(differences) > 0 or len(data_properties_diff) > 0


async def is_different_async(
    client: AsyncWacomKnowledgeService, thing_file: ThingObject, thing_kg: ThingObject
) -> bool:
    """
    Check if the two entities are different.

    Parameters
    ----------
    client: WacomKnowledgeService
        The client to use.
    thing_file: ThingObject
        The thing from the file.
    thing_kg: ThingObject
        The thing from the knowledge graph.

    Returns
    -------
    is_different: bool
        True if the entities are different, False otherwise.
    """
    differences, data_properties_diff, _ = await diff_entities_async(client, thing_file, thing_kg)
    return len(differences) > 0 or len(data_properties_diff) > 0
