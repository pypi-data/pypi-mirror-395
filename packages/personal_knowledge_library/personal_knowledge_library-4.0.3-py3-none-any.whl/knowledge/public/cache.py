# -*- coding: utf-8 -*-
# Copyright © 2023-present Wacom. All rights reserved.
import threading
from collections import OrderedDict
from functools import wraps
from pathlib import Path
from typing import Dict, Any

import loguru
import orjson

from knowledge.public.wikidata import WikidataThing, WikidataProperty, WikidataClass

# Configure logging
logger = loguru.logger


def singleton(cls):
    """
    Singleton decorator to ensure that a class has only one instance and provide a global point of access to it.
    """
    instances: Dict[str, Any] = {}
    lock: threading.Lock = threading.Lock()

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:  # Double-checked locking
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class WikidataCache:
    """
    WikidataCache
    --------------
    A singleton class that manages a cache of Wikidata objects using an LRU (Least Recently Used) strategy.

    Parameters
    ----------
    max_size: int
        The maximum size of the cache. When the cache exceeds this size, the least recently used item will be removed.

    Attributes
    ----------
    cache: OrderedDict
        The cache that stores Wikidata objects.
    """

    _instance = None  # Singleton instance

    def __init__(self, max_size: int = 100000):
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()  # Maintain insertion order for LRU eviction
        self.property_cache: OrderedDict = OrderedDict()  # Cache for properties
        self.subclass_cache: OrderedDict = OrderedDict()  # Cache for subclasses
        self.superclass_cache: OrderedDict = OrderedDict()  # Cache for superclasses

    def cache_property(self, prop: WikidataProperty):
        """Adds a property to the property cache with LRU eviction.

        Parameters
        ----------
        prop: Dict[str, Any]
            The property to cache.
        """
        if prop.pid in self.property_cache:
            self.property_cache.move_to_end(prop.pid)
        elif len(self.property_cache) >= self.max_size:
            self.property_cache.popitem(last=False)  # Remove the least recently used item
        self.property_cache[prop.pid] = prop

    def get_property(self, pid: str) -> WikidataProperty:
        """Retrieves a property from the property cache.

        Parameters
        ----------
        pid: str
            The PID of the property to retrieve.

        Returns
        -------
        Dict[str, Any]
            The property associated with the given PID.
        """
        if pid in self.property_cache:
            self.property_cache.move_to_end(pid)
            return self.property_cache[pid]
        raise KeyError(f"Property {pid} not found in cache.")

    def cache_wikidata_object(self, wikidata_object: WikidataThing):
        """Adds a Wikidata object to the cache with LRU eviction.

        Parameters
        ----------
        wikidata_object: WikidataThing
            The Wikidata object to cache.
        """
        if wikidata_object.qid in self.cache:
            self.cache.move_to_end(wikidata_object.qid)  # Mark as most recently used
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)  # Remove the least recently used item

        self.cache[wikidata_object.qid] = wikidata_object

    def get_wikidata_object(self, qid: str) -> WikidataThing:
        """Retrieves a Wikidata object from the cache.

        Parameters
        ----------
        qid: str
            The QID of the Wikidata object to retrieve.

        Returns
        -------
        WikidataThing
            The Wikidata object associated with the given QID.
        """
        if qid in self.cache:
            self.cache.move_to_end(qid)  # Mark as most recently used
            return self.cache[qid]
        raise KeyError(f"Wikidata object {qid} not found in cache.")

    def cache_subclass(self, subclass: WikidataClass):
        """Adds a subclass to the subclass cache with LRU eviction.

        Parameters
        ----------
        subclass: WikidataClass
            The subclass to cache.
        """
        if subclass.qid in self.subclass_cache:
            self.subclass_cache.move_to_end(subclass.qid)
        elif len(self.subclass_cache) >= self.max_size:
            self.subclass_cache.popitem(last=False)

        self.subclass_cache[subclass.qid] = subclass

    def get_subclass(self, qid: str) -> WikidataClass:
        """Retrieves a subclass from the subclass cache.

        Parameters
        ----------
        qid: str
            The QID of the subclass to retrieve.

        Returns
        -------
        WikidataClass
            The subclass associated with the given QID.
        """
        if qid in self.subclass_cache:
            self.subclass_cache.move_to_end(qid)
            return self.subclass_cache[qid]
        raise KeyError(f"Subclass {qid} not found in cache.")

    def cache_superclass(self, superclass: WikidataClass):
        """Adds a superclass to the superclass cache with LRU eviction.

        Parameters
        ----------
        superclass: WikidataClass
            The superclass to cache.
        """
        if superclass.qid in self.superclass_cache:
            self.superclass_cache.move_to_end(superclass.qid)
        elif len(self.superclass_cache) >= self.max_size:
            self.superclass_cache.popitem(last=False)

        self.superclass_cache[superclass.qid] = superclass

    def get_superclass(self, qid: str) -> WikidataClass:
        """Retrieves a superclass from the superclass cache.

        Parameters
        ----------
        qid: str
            The QID of the superclass to retrieve.

        Returns
        -------
        WikidataClass
            The superclass associated with the given QID.
        """
        if qid in self.superclass_cache:
            self.superclass_cache.move_to_end(qid)
            return self.superclass_cache[qid]
        raise KeyError(f"Superclass {qid} not found in cache.")

    @staticmethod
    def __path__objects__(path: Path) -> Path:
        """Caches the objects from a path.

        Parameters
        ----------
        path: Path
            The path to the file containing the objects.

        Returns
        -------
        Path
            The path to the file containing the objects.
        """
        return path / "wikidata_cache.ndjson"

    @staticmethod
    def __path__properties__(path: Path) -> Path:
        """Caches the properties from a path.

        Parameters
        ----------
        path: Path
            The path to the file containing the properties.
        """
        return path / "property_cache.ndjson"

    @staticmethod
    def __path__subclasses__(path: Path) -> Path:
        """Caches the subclasses from a path.

        Parameters
        ----------
        path: Path
            The path to the file containing the subclasses.

        Returns
        -------
        Path
            The path to the file containing the subclasses.
        """
        return path / "subclass_cache.ndjson"

    @staticmethod
    def __path__superclasses__(path: Path) -> Path:
        """Caches the superclasses from a path.

        Parameters
        ----------
        path: Path
            The path to the file containing the superclasses.

        Returns
        -------
        Path
            The path to the file containing the superclasses.
        """
        return path / "superclass_cache.ndjson"

    def save_cache(self, cache_path: Path):
        """Saves the cache to a file.

        Parameters
        ----------
        cache_path: Path
            The path to the file where the cache will be saved.
        """

        if not cache_path.exists():
            cache_path.mkdir(parents=True, exist_ok=True)
        elif cache_path.is_file():
            logger.warning(f"Cache path {cache_path} is a file. Please provide a directory.")
            return
        # Save the cache to a file
        with WikidataCache.__path__objects__(cache_path).open("w") as file:
            for thing in self.cache.values():
                thing: WikidataThing
                file.write(orjson.dumps(thing.__dict__()).decode("utf-8") + "\n")
        # Save the property cache to a file
        with WikidataCache.__path__properties__(cache_path).open("w") as file:
            for prop in self.property_cache.values():
                prop: WikidataProperty
                file.write(orjson.dumps(prop.__dict__()).decode("utf-8") + "\n")
        # Save the superclass cache to a file
        with WikidataCache.__path__subclasses__(cache_path).open("w") as file:
            for subclass in self.subclass_cache.values():
                subclass: WikidataClass
                file.write(orjson.dumps(subclass.__dict__()).decode("utf-8") + "\n")
        # Save the subclass cache to a file
        with WikidataCache.__path__superclasses__(cache_path).open("w") as file:
            for superclass in self.superclass_cache.values():
                superclass: WikidataClass
                file.write(orjson.dumps(superclass.__dict__()).decode("utf-8") + "\n")

    def load_cache(self, cache_path: Path) -> None:
        """Loads the cache from a path.

        Parameters
        ----------
        cache_path: Path
            The path to the file from which the cache will be loaded.
        """
        if not cache_path.exists():
            logger.warning(f"Cache file {cache_path} not found. Skipping load.")
            return
        if cache_path.is_file():
            logger.warning(f"Cache path {cache_path} is a file. Please provide a directory.")
            return

        wikidata_object_path: Path = WikidataCache.__path__objects__(cache_path)
        if wikidata_object_path.exists():
            with wikidata_object_path.open("r") as file:
                for line in file:
                    try:
                        thing_data = orjson.loads(line)
                        thing = WikidataThing.create_from_dict(thing_data)
                        self.cache_wikidata_object(thing)
                    except Exception as e:
                        logger.error(f"Error loading cache: {e}. Line: {line}")
        path_property: Path = WikidataCache.__path__properties__(cache_path)
        if path_property.exists():
            with path_property.open("r") as file:
                for line in file:
                    try:
                        prop_data = orjson.loads(line)
                        prop = WikidataProperty.create_from_dict(prop_data)
                        self.cache_property(prop)
                    except Exception as e:
                        logger.error(f"Error loading property cache: {e}. Line: {line}")
        subclass_path: Path = WikidataCache.__path__subclasses__(cache_path)
        if subclass_path.exists():
            with WikidataCache.__path__subclasses__(cache_path).open("r") as file:
                for line in file:
                    try:
                        subclass_data = orjson.loads(line)
                        subclass = WikidataClass.create_from_dict(subclass_data)
                        self.subclass_cache[subclass.qid] = subclass
                    except Exception as e:
                        logger.error(f"Error loading subclass cache: {e}. Line: {line}")
        superclass_path: Path = WikidataCache.__path__superclasses__(cache_path)
        if superclass_path.exists():
            with superclass_path.open("r") as file:
                for line in file:
                    try:
                        superclass_data = orjson.loads(line)
                        superclass = WikidataClass.create_from_dict(superclass_data)
                        self.superclass_cache[superclass.qid] = superclass
                    except Exception as e:
                        logger.error(f"Error loading superclass cache: {e}. Line: {line}")

    def qid_in_cache(self, qid: str) -> bool:
        """Checks if a QID is in the cache.

        Parameters
        ----------
        qid: str
            The QID to check.

        Returns
        -------
        bool
            True if the QID is in the cache, False otherwise.
        """
        return qid in self.cache

    def property_in_cache(self, pid: str) -> bool:
        """Checks if a property is in the cache.

        Parameters
        ----------
        pid: str
            The PID to check.

        Returns
        -------
        bool
            True if the PID is in the cache, False otherwise.
        """
        return pid in self.property_cache

    def subclass_in_cache(self, qid: str) -> bool:
        """Checks if a subclass is in the cache.

        Parameters
        ----------
        qid: str
            The QID to check.

        Returns
        -------
        bool
            True if the QID is in the subclass cache, False otherwise.
        """
        return qid in self.subclass_cache

    def superclass_in_cache(self, qid: str) -> bool:
        """Checks if a superclass is in the cache.

        Parameters
        ----------
        qid: str
            The QID to check.

        Returns
        -------
        bool
            True if the QID is in the superclass cache, False otherwise.
        """
        return qid in self.superclass_cache

    def number_of_cached_subclasses(self) -> int:
        """Returns the number of cached subclasses.

        Returns
        -------
        int
            The number of subclasses in the cache.
        """
        return len(self.subclass_cache)

    def number_of_cached_superclasses(self) -> int:
        """Returns the number of cached superclasses.

        Returns
        -------
        int
            The number of superclasses in the cache.
        """
        return len(self.superclass_cache)

    def number_of_cached_objects(self) -> int:
        """Returns the number of cached objects.

        Returns
        -------
        int
            The number of objects in the cache.
        """
        return len(self.cache)

    def number_of_cached_properties(self) -> int:
        """Returns the number of cached properties.

        Returns
        -------
        int
            The number of properties in the cache.
        """
        return len(self.property_cache)
