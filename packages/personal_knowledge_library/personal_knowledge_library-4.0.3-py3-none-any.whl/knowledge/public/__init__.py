# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
"""Mapping of Wikidata property ids to its string."""
import json
from pathlib import Path
from typing import Dict, List

# OntologyPropertyReference constants
INSTANCE_OF_PROPERTY: str = "P31"
IMAGE_PROPERTY: str = "P18"

# Mapping for property names
DEFAULT_TIMEOUT: int = 60
DEFAULT_TOKEN_REFRESH_TIME: int = 360
STATUS_FORCE_LIST: List[int] = [429, 500, 502, 503, 504]
DEFAULT_BACKOFF_FACTOR: float = 0.1
DEFAULT_MAX_RETRIES: int = 3

CWD: Path = Path(__file__).parent


from knowledge.public import wikidata
from knowledge.public import helper
from knowledge.public import relations
from knowledge.public import cache


__all__ = ["wikidata", "helper", "relations", "cache", "client", "INSTANCE_OF_PROPERTY", "IMAGE_PROPERTY"]
