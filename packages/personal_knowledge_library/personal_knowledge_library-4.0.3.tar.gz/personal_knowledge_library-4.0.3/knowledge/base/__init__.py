# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
"""
Base structures.
----------------
This module provides the base structures for the knowledge graph.
Such as the ontology, entities and access.

The classes in this module are used by the knowledge graph service.
For instance, the ontology structure is used to create the structure knowledge graph.
The entities are used to store the knowledge graph.

The access is used to access the knowledge graph, there are different types of access:
    - Private access: the user can access only the entities that he/she created.
    - Public access: the user can access all the entities.
    - Group access: the user can access the entities that are in the same group.
"""
__all__ = ["access", "entity", "language", "ontology", "response", "search", "tenant"]

from knowledge.base import access
from knowledge.base import entity
from knowledge.base import language
from knowledge.base import ontology
from knowledge.base import response
from knowledge.base import search
from knowledge.base import tenant
