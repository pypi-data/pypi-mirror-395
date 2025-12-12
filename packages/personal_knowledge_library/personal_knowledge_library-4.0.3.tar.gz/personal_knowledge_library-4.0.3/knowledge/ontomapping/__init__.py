# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import enum
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

import loguru
from rdflib import Graph, RDFS, URIRef

from knowledge.base.ontology import OntologyClassReference, OntologyPropertyReference, DataPropertyType
from knowledge.public.cache import WikidataCache
from knowledge.public.wikidata import WikidataClass
from knowledge.public.client import WikiDataAPIClient

# Classes
TOPIC_CLASS: str = "wacom:core#Topic"
# Constants
DBPEDIA_TYPES: str = "dbpedia_types"
WIKIDATA_TYPES: str = "wikidata_types"
OBJECT_PROPERTIES: str = "object_properties"
DATA_PROPERTIES: str = "data_properties"
DOMAIN_PROPERTIES: str = "domain"
CLASSES: str = "classes"
CONTEXT_NAME: str = "core"
CWD: Path = Path(__file__).parent
ontology_graph: Graph = Graph()
logger = loguru.logger
# Cache
wikidata_cache: WikidataCache() = WikidataCache()


def flatten(hierarchy: WikidataClass) -> Set[str]:
    """
    Flattens the hierarchy.

    Parameters
    ----------
    hierarchy: WikidataClass
        Hierarchy

    Returns
    -------
    hierarchy: Set[str]
        Hierarchy
    """
    hierarchy_set: Set[str] = set()
    jobs: List[WikidataClass] = [hierarchy]

    while jobs:
        job = jobs.pop()

        # Skip if already visited
        if job.qid in hierarchy_set:
            continue

        hierarchy_set.add(job.qid)

        # Add only unvisited subclasses
        for c in job.subclasses:
            if c.qid not in hierarchy_set:
                jobs.append(c)

    return hierarchy_set


def subclasses_of(iri: str) -> List[str]:
    """
    Returns the subclasses of an ontology class.
    Parameters
    ----------
    iri: str
        Ontology class IRI.

    Returns
    -------
    subclasses: List[str]
        Subclasses of the ontology class.
    """
    sub_classes: List[str] = [str(s) for s, p, o in list(ontology_graph.triples((None, RDFS.subClassOf, URIRef(iri))))]
    for sub_class in sub_classes:
        sub_classes.extend(subclasses_of(sub_class))
    return sub_classes


def is_iso_date(date_string: str) -> bool:
    """
    Checks if a date string is an ISO date.
    Parameters
    ----------
    date_string: str
        Date string.

    Returns
    -------
    is_iso_date: bool
        True if the date string is an ISO date, otherwise False.
    """
    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError as _:
        return False


class WikidataClassEncoder(json.JSONEncoder):
    """
    Wikidata Class encoder
    ----------------------
    This class encodes a Wikidata class to JSON.
    """

    def default(self, o):
        if isinstance(o, WikidataClass):
            return o.__dict__()
        return json.JSONEncoder.default(self, o)


class ClassConfiguration:
    """
    Class configuration
    -------------------
    This class contains the configuration for a class.

    Parameters
    ----------
    ontology_class: str
        Ontology class
    """

    def __init__(self, ontology_class: str):
        self.__ontology_class: str = ontology_class
        self.__wikidata_classes: List[str] = []
        self.__dbpedia_classes: List[str] = []

    @property
    def ontology_class(self) -> str:
        """Ontology class."""
        return self.__ontology_class

    @property
    def wikidata_classes(self) -> List[str]:
        """Wikidata classes."""
        return self.__wikidata_classes

    @wikidata_classes.setter
    def wikidata_classes(self, value: List[str]):
        self.__wikidata_classes = value

    @property
    def dbpedia_classes(self) -> List[str]:
        """DBpedia classes."""
        return self.__dbpedia_classes

    @dbpedia_classes.setter
    def dbpedia_classes(self, value: List[str]):
        self.__dbpedia_classes = value

    @property
    def concept_type(self) -> OntologyClassReference:
        """Concept type."""
        return OntologyClassReference.parse(self.__ontology_class)

    def __str__(self):
        return (
            f"ClassConfiguration(ontology_class={self.__ontology_class}, "
            f"wikidata_classes={self.__wikidata_classes}, dbpedia_classes={self.__dbpedia_classes})"
        )


class PropertyType(enum.Enum):
    """
    Property type
    """

    DATA_PROPERTY = 0
    OBJECT_PROPERTY = 1


class PropertyConfiguration:
    """
    Property configuration.
    -----------------------
    This class contains the configuration for a property.

    Parameters
    ----------
    iri: str
        The IRI of the property.
    property_type: PropertyType
        The property type.
    pids: Optional[List[str]]
        The list of property PIDs.
    """

    def __init__(self, iri: str, property_type: PropertyType, pids: Optional[List[str]] = None):
        self.__iri: str = iri
        self.__pids: List[str] = pids if pids else []
        self.__property: PropertyType = property_type
        self.__inverse: Optional[str] = None
        self.__ranges: List[str] = []
        self.__domains: List[str] = []

    @property
    def iri(self) -> str:
        """IRI of the property."""
        return self.__iri

    @iri.setter
    def iri(self, value: str):
        self.__iri = value

    @property
    def inverse(self) -> Optional[str]:
        """Inverse property."""
        return self.__inverse

    @inverse.setter
    def inverse(self, value: str):
        self.__inverse = value

    @property
    def type(self) -> PropertyType:
        """Property type."""
        return self.__property

    @property
    def pids(self) -> List[str]:
        """List of property PIDs."""
        return self.__pids

    @property
    def ranges(self) -> List[str]:
        """List of ranges."""
        return self.__ranges

    @property
    def domains(self) -> List[str]:
        """List of domains."""
        return self.__domains

    def __str__(self):
        return f"PropertyConfiguration(ontology_property={self.iri})"


class MappingConfiguration:
    """
    Mapping configuration
    ---------------------
    This class contains the configuration for the mapping.

    """

    def __init__(self):
        self.__classes: List[ClassConfiguration] = []
        self.__properties: List[PropertyConfiguration] = []
        self.__index: Dict[str, int] = {}
        self.__index_properties: Dict[str, List[int]] = {}
        self.__index_iri: Dict[str, int] = {}
        self.__direct_index: Dict[str, int] = {}

    @property
    def classes(self) -> List[ClassConfiguration]:
        """List of classes."""
        return self.__classes

    @property
    def properties(self) -> List[PropertyConfiguration]:
        """List of properties."""
        return self.__properties

    def guess_classed(self, classes: List[str]) -> Optional[ClassConfiguration]:
        """
        Guesses the class from the label.
        Parameters
        ----------
        classes: List[str]
            The list of classes

        Returns
        -------
        class: Optional[ClassConfiguration]
            If a mapping exists, the class configuration, otherwise None.
        """
        for cls_name in classes:
            if cls_name in self.__direct_index:
                return self.__classes[self.__direct_index[cls_name]]
            if cls_name in self.__index:
                return self.__classes[self.__index[cls_name]]
        return None

    def guess_property(
        self, property_pid: str, concept_type: OntologyClassReference
    ) -> Optional[PropertyConfiguration]:
        """
        Guesses the property from the label.
        Parameters
        ----------
        property_pid: str
            PID of the property
        concept_type: OntologyClassReference
            The concept type.
        Returns
        -------
        property_config: Optional[PropertyConfiguration]
            If a mapping exists, the property configuration, otherwise None.
        """
        if property_pid in self.__index_properties:
            for pid_idx in self.__index_properties[property_pid]:
                prop_conf: PropertyConfiguration = self.__properties[pid_idx]
                if concept_type.iri in prop_conf.domains:
                    return prop_conf
        return None

    def property_for(
        self, class_ref: OntologyClassReference, property_type: Optional[PropertyType]
    ) -> List[PropertyConfiguration]:
        """
        Returns the properties for a class.
        Parameters
        ----------
        class_ref: OntologyClassReference
            The class reference.
        property_type: Optional[PropertyType]
            The property type, if None, all properties are returned.
        Returns
        -------
        properties: List[PropertyConfiguration]
            The list of properties.
        """
        domain_classes: List[str] = [class_ref.iri]
        domain_classes += subclasses_of(class_ref.iri)
        domain_subclasses: Dict[str, List[str]] = {}
        properties: List[PropertyConfiguration] = []
        for prop_conf in self.properties:
            for d in prop_conf.domains:
                if d not in domain_subclasses:
                    domain_subclasses[d] = [d] + subclasses_of(d)
                if class_ref.iri in domain_subclasses[d]:
                    if property_type is None or prop_conf.type == property_type:
                        properties.append(prop_conf)
        return properties

    def add_class(self, class_configuration: ClassConfiguration):
        """
        Adds a class configuration.

        Parameters
        ----------
        class_configuration: ClassConfiguration
            The class configuration
        """
        self.__classes.append(class_configuration)
        class_idx: int = len(self.__classes) - 1
        number_of_classes: int = len(class_configuration.wikidata_classes)
        if number_of_classes > 0:
            logger.debug(f"Adding {number_of_classes} classes for {class_configuration.concept_type.iri}")
        for _, c in enumerate(class_configuration.wikidata_classes):
            if wikidata_cache.subclass_in_cache(c):
                for subclass in wikidata_cache.get_subclass(c).subclasses:
                    if subclass in self.__index:
                        logger.warning(f"Class {subclass} already exists in the index.")
                        class_config: ClassConfiguration = self.__classes[self.__index[subclass]]
                        logger.warning(
                            f"Class {class_config.concept_type} "
                            f"is conflicting with {class_configuration.concept_type}."
                        )
                    self.__index[subclass] = class_idx
                self.__direct_index[c] = class_idx
            else:
                w_classes: Dict[str, WikidataClass] = WikiDataAPIClient.subclasses(c)
                for subclass in w_classes.values():
                    wikidata_cache.cache_subclass(subclass)
                    for cls in flatten(subclass):
                        self.__index[cls] = class_idx
        for c in class_configuration.dbpedia_classes:
            self.__index[c] = len(self.__classes) - 1

    def add_property(self, property_configuration: PropertyConfiguration):
        """
        Adds a property configuration.

        Parameters
        ----------
        property_configuration: PropertyConfiguration
            The property configuration
        """
        self.__properties.append(property_configuration)
        for pid in property_configuration.pids:
            idx: int = len(self.__properties) - 1
            if pid not in self.__index_properties:
                self.__index_properties[pid] = []
            self.__index_properties[pid].append(idx)
            self.__index_iri[property_configuration.iri] = idx

    def property_for_iri(self, property_iri: str) -> PropertyConfiguration:
        """
        Returns the property configuration for an IRI.

        Parameters
        ----------
        property_iri: str
            The property IRI

        Returns
        -------
        property: PropertyConfiguration
            The property configuration

        Raises
        ------
        ValueError
            If the property is not found.
        """
        if property_iri not in self.__index_iri:
            raise ValueError(f"Property {property_iri} not found.")
        return self.__properties[self.__index_iri[property_iri]]

    def check_data_property_range(self, property_type: OntologyPropertyReference, content: Optional[Any]) -> bool:
        """
        Checks if the content is in the range of the property.

        Parameters
        ----------
        property_type: OntologyPropertyReference
            The property type
        content: Optional[Any]
            The content

        Returns
        -------
        evaluation: bool
            True if the content is in the range, False otherwise.
        """
        if content is None:
            return False
        prop_config: Optional[PropertyConfiguration] = self.property_for_iri(property_type.iri)
        if prop_config:
            for r in prop_config.ranges:
                if r == DataPropertyType.STRING.value:
                    return content is not None and isinstance(content, str)
                if r == DataPropertyType.INTEGER.value:
                    return content is not None and isinstance(content, int)
                if r == DataPropertyType.FLOAT.value:
                    return content is not None and isinstance(content, float)
                if r == DataPropertyType.BOOLEAN.value:
                    return content is not None and isinstance(content, bool)
                if r in {DataPropertyType.DATE.value, DataPropertyType.DATE_TIME.value}:
                    return content is not None and isinstance(content, str) and is_iso_date(content)
                return True
        return False

    def check_object_property_range(
        self,
        property_type: OntologyPropertyReference,
        source_type: OntologyClassReference,
        target_type: OntologyClassReference,
    ) -> bool:
        """
        Checks if the target is in the range of the property.
        Parameters
        ----------
        property_type: OntologyPropertyReference
            The property
        source_type: OntologyClassReference
            The concept type
        target_type: OntologyClassReference
            The target type

        Returns
        -------
        valid: bool
            True if the target is in the range, False otherwise.
        """
        prop_config: Optional[PropertyConfiguration] = self.property_for_iri(property_type.iri)
        if prop_config:
            if prop_config.type == PropertyType.OBJECT_PROPERTY:
                if source_type.iri in prop_config.domains and target_type.iri in prop_config.ranges:
                    return True
                return False
        return False

    def __str__(self):
        return f"Mapping Configuration(#classes={len(self.__classes)}" f", #properties={len(self.__properties)})"


mapping_configuration: Optional[MappingConfiguration] = None


def build_configuration(mapping: Dict[str, Any]) -> MappingConfiguration:
    """
    Builds the configuration from the mapping file.
    Parameters
    ----------
    mapping: Dict[str, Any]
        The mapping file

    Returns
    -------
    conf: MappingConfiguration
        The mapping configuration
    """
    conf: MappingConfiguration = MappingConfiguration()
    configuration_classes: int = len(mapping["classes"])
    logger.debug(f"Adding {configuration_classes} classes to the mapping configuration")
    for c, c_conf in mapping["classes"].items():
        class_config: ClassConfiguration = ClassConfiguration(c)
        class_config.dbpedia_classes = c_conf[DBPEDIA_TYPES]
        class_config.wikidata_classes = c_conf[WIKIDATA_TYPES]
        conf.add_class(class_config)
    dataproperty_count: int = len(mapping["data_properties"])
    logger.debug(f"Adding {dataproperty_count} data properties to the mapping configuration")
    for p, p_conf in mapping["data_properties"].items():
        property_config: PropertyConfiguration = PropertyConfiguration(
            p, PropertyType.DATA_PROPERTY, p_conf["wikidata_types"]
        )
        if "ranges" in p_conf:
            for ra in p_conf["ranges"]:
                property_config.ranges.append(ra)
                property_config.ranges.extend(subclasses_of(ra))
        if "domains" in p_conf:
            for do in p_conf["domains"]:
                property_config.domains.append(do)
                property_config.domains.extend(subclasses_of(do))
        conf.add_property(property_config)
    object_property_count: int = len(mapping["object_properties"])
    logger.debug(f"Adding {object_property_count} object properties to the mapping configuration")
    for p, p_conf in mapping["object_properties"].items():
        property_config: PropertyConfiguration = PropertyConfiguration(
            p, PropertyType.OBJECT_PROPERTY, p_conf["wikidata_types"]
        )
        if "ranges" in p_conf:
            for ra in p_conf["ranges"]:
                property_config.ranges.append(ra)
                property_config.ranges.extend(subclasses_of(ra))
        if "domains" in p_conf:
            for do in p_conf["domains"]:
                property_config.domains.append(do)
                property_config.domains.extend(subclasses_of(do))
        if "inverse" in p_conf:
            property_config.inverse = p_conf["inverse"]
        conf.add_property(property_config)
    return conf


def register_ontology(rdf_str: str):
    """
    Registers the ontology.
    Parameters
    ----------
    rdf_str: str
        The ontology in RDF/XML format.
    """
    ontology_graph.parse(data=rdf_str, format="xml")


def load_configuration(configuration: Path):
    """
    Loads the configuration.

    Raises
    ------
    ValueError
        If the configuration file is not found.
    """
    global mapping_configuration
    if configuration.exists():
        with configuration.open("r", encoding="utf-8") as fp_configuration:
            configuration = json.loads(fp_configuration.read())
        mapping_configuration = build_configuration(configuration)
    else:
        raise ValueError(f"Configuration file {configuration} not found.")


def get_mapping_configuration() -> MappingConfiguration:
    """
    Returns the mapping configuration.

    Returns
    -------
    mapping_configuration: MappingConfiguration
        The mapping configuration
    """
    if mapping_configuration is None:
        raise ValueError("Please load configuration")
    return mapping_configuration
