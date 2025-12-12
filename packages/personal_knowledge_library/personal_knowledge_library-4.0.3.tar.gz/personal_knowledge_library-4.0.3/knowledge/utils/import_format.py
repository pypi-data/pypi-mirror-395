# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
import gzip
import json
import logging
import re
import uuid
from json import JSONDecodeError
from pathlib import Path
from typing import List, Dict, Any

import loguru

from knowledge.base.ontology import ThingObject, OntologyPropertyReference

logger = loguru.logger


def is_http_url(url: str) -> bool:
    """Check if a string is an HTTP(S) URL.
    Parameters
    ----------
    url: str
        The URL to check.

    Returns
    -------
    bool
        True if the URL is HTTP(S), False otherwise.
    """
    return bool(re.match(r"^(https?://)", url, re.IGNORECASE))


def is_local_url(url: str) -> bool:
    """Check if a string is a local file path or relative URL.
    Parameters
    ----------
    url: str
        The URL to check.

    Returns
    -------
    bool
        True if the URL is a local file path or relative URL, False otherwise.
    """
    return bool(re.match(r"^(file://|/|\.{1,2}/)", url, re.IGNORECASE))


def __import_format_to_thing__(line: str) -> ThingObject:
    """
    Convert a line of JSON to a ThingObject.
    Parameters
    ----------
    line: str
        The line of JSON to convert.

    Returns
    -------
    entity: ThingObject
        The ThingObject created from the JSON line.

    Raises
    ------
    JSONDecodeError
        If the line is not valid JSON.
    """
    thing_dict: Dict[str, Any] = json.loads(line)
    entity: ThingObject = ThingObject.from_import_dict(thing_dict)
    if entity.image:
        if not is_local_url(entity.image) and not is_http_url(entity.image):
            path: Path = Path(entity.image)
            if not path.exists():
                entity.image = path.absolute().as_uri()
            else:
                logger.warning(f"Image path {path} does not exist. Setting to None.")
                entity.image = None
    remove_props: List[OntologyPropertyReference] = []
    # Remove empty properties
    for obj_prop, value in entity.object_properties.items():
        if len(value.incoming_relations) == 0 and len(value.outgoing_relations) == 0:
            remove_props.append(obj_prop)
    for prop in remove_props:
        del entity.object_properties[prop]
    return entity


def load_import_format(file_path: Path) -> List[ThingObject]:
    """
    Load the import format file.
    Parameters
    ----------
    file_path:  Path
        The path to the file.

    Returns
    -------
    entity_list: List[ThingObject]
        The list of entities.

    Raises
    ------
    FileNotFoundError
        If the file does not exist or is not a file.
    """
    if not file_path.exists():
        logger.error(f"File {file_path} does not exist.")
        raise FileNotFoundError(f"File {file_path} does not exist.")
    if not file_path.is_file():
        logger.error(f"Path {file_path} is not a file.")
        raise FileNotFoundError(f"Path {file_path} is not a file.")
    cached_entities: List[ThingObject] = []
    if file_path.suffix == ".gz":
        with gzip.open(file_path, "rt", encoding="utf-8") as f_gz:
            for line_number, line in enumerate(f_gz):
                stripped_line: str = line.strip()
                if not stripped_line:
                    continue  # Skip empty lines
                if line_number == 0:
                    # Skip the first line (header)
                    continue
                try:
                    cached_entities.append(__import_format_to_thing__(line))
                except JSONDecodeError as e:
                    logging.error(f"[line:={line_number}] Error decoding JSON: {e}.")
                except Exception as e:
                    logging.error(f"[line:={line_number}] Error loading entity: {e}.")

    else:
        with file_path.open(encoding="utf8") as f:
            # Skip the first line
            for line_number, line in enumerate(f.readlines()):
                try:
                    cached_entities.append(__import_format_to_thing__(line))
                except JSONDecodeError as e:
                    logging.error(f"[line:={line_number}] Error decoding JSON: {e}.")
                except Exception as e:
                    logging.error(f"[line:={line_number}] - Error parsing import format {e}.")
    return cached_entities


def save_import_format(
    file_path: Path, entities: List[ThingObject], save_groups: bool = True, generate_missing_ref_ids: bool = True
) -> None:
    """
    Save the import format file.
    Parameters
    ----------
    file_path: Path
        The path to the file.
    entities: List[ThingObject]
        The list of entities.
    save_groups: bool
        Whether to save groups or not.
    generate_missing_ref_ids: bool
        Whether to generate missing reference IDs or not.
    """
    # Create the directory if it does not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.suffix == ".gz":
        with gzip.open(file_path, "wt", encoding="utf-8") as fp_thing:
            for entity in entities:
                if generate_missing_ref_ids and entity.default_source_reference_id() is None:
                    entity.reference_id = str(uuid.uuid4())
                if save_groups:
                    fp_thing.write(f"{json.dumps(entity.__import_format_dict__(), ensure_ascii=False)}\n")
                else:
                    fp_thing.write(f"{json.dumps(entity.__import_format_dict__(group_ids=[]), ensure_ascii=False)}\n")
    elif file_path.suffix == ".ndjson":
        with file_path.open("w", encoding="utf-8") as fp_thing:
            for entity in entities:
                if generate_missing_ref_ids and entity.default_source_reference_id() is None:
                    entity.reference_id = str(uuid.uuid4())
                if save_groups:
                    fp_thing.write(f"{json.dumps(entity.__import_format_dict__(), ensure_ascii=False)}\n")
                else:
                    fp_thing.write(f"{json.dumps(entity.__import_format_dict__(group_ids=[]), ensure_ascii=False)}\n")


def append_import_format(file_path: Path, entity: ThingObject) -> None:
    """
    Append to the import format file.
    Parameters
    ----------
    file_path: Path
        The path to the file.
    entity: ThingObject
        The entity to append.
    """
    with file_path.open("a", encoding="utf-8") as fp_thing:
        fp_thing.write(f"{json.dumps(entity.__import_format_dict__(), ensure_ascii=False)}\n")
