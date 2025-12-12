# -*- coding: utf-8 -*-
# Copyright © 2023-24 Wacom. All rights reserved.
"""
This package contains the services for the knowledge graph functionality.
"""
from typing import List, Literal

# ------------------------------------------------- Constants ----------------------------------------------------------
USER_AGENT_HEADER_FLAG: str = "User-Agent"
AUTHORIZATION_HEADER_FLAG: str = "Authorization"
CONTENT_TYPE_HEADER_FLAG: str = "Content-Type"
TENANT_API_KEY: str = "x-tenant-api-key"
REFRESH_TOKEN_TAG: str = "refreshToken"
EXPIRATION_DATE_TAG: str = "expirationDate"
ACCESS_TOKEN_TAG: str = "accessToken"
ACTIVATION_TAG: str = "activation"
SEARCH_TERM: str = "searchTerm"
EXACT_MATCH: str = "exactMatch"
LANGUAGE_PARAMETER: str = "language"
TYPES_PARAMETER: str = "types"
LIMIT_PARAMETER: str = "limit"
LITERAL_PARAMETER: str = "Literal"
VALUE: str = "Value"
SEARCH_PATTERN_PARAMETER: str = "SearchPattern"
LISTING: str = "listing"
TOTAL_COUNT: str = "estimatedCount"
TARGET: str = "target"
OBJECT: str = "object"
PREDICATE: str = "predicate"
SUBJECT: str = "subject"
LIMIT: str = "limit"
OBJECT_URI: str = "objectUri"
RELATION_URI: str = "relationUri"
SUBJECT_URI: str = "subjectUri"
NEXT_PAGE_ID_TAG: str = "nextPageId"
TENANT_RIGHTS_TAG: str = "tenantRights"
GROUP_IDS_TAG: str = "groupIds"
OWNER_ID_TAG: str = "ownerId"
VISIBILITY_TAG: str = "visibility"
ESTIMATE_COUNT: str = "estimateCount"
GROUP_USER_RIGHTS_TAG: str = "groupUserRights"
JOIN_KEY_PARAM: str = "joinKey"
USER_TO_ADD_PARAM: str = "userToAddId"
USER_TO_REMOVE_PARAM: str = "userToRemoveId"
FORCE_PARAM: str = "force"
IS_OWNER_PARAM: str = "isOwner"
RELATION_TAG: str = "relation"
ENTITIES_TAG: str = "entities"
RESULT_TAG: str = "result"
EXTERNAL_USER_ID: str = "externalUserId"
PRUNE_PARAM: str = "prune"
NEL_PARAM: str = "nelType"

APPLICATION_JSON_HEADER: str = "application/json"
IndexType = Literal["NEL", "ElasticSearch", "VectorSearchWord", "VectorSearchDocument"]

DEFAULT_TIMEOUT: int = 60
DEFAULT_TOKEN_REFRESH_TIME: int = 360
STATUS_FORCE_LIST: List[int] = [502, 503, 504]
DEFAULT_BACKOFF_FACTOR: float = 0.1
DEFAULT_MAX_RETRIES: int = 3

"""
Refresh token time in seconds. 360 seconds = 6 minutes
"""

__all__ = [
    "base",
    "graph",
    "ontology",
    "tenant",
    "users",
    "search",
    "USER_AGENT_HEADER_FLAG",
    "AUTHORIZATION_HEADER_FLAG",
    "CONTENT_TYPE_HEADER_FLAG",
    "TENANT_API_KEY",
    "REFRESH_TOKEN_TAG",
    "EXPIRATION_DATE_TAG",
    "ACCESS_TOKEN_TAG",
    "ACTIVATION_TAG",
    "SEARCH_TERM",
    "LANGUAGE_PARAMETER",
    "TYPES_PARAMETER",
    "LIMIT_PARAMETER",
    "LITERAL_PARAMETER",
    "VALUE",
    "SEARCH_PATTERN_PARAMETER",
    "LISTING",
    "TOTAL_COUNT",
    "TARGET",
    "OBJECT",
    "PREDICATE",
    "SUBJECT",
    "LIMIT",
    "OBJECT_URI",
    "RELATION_URI",
    "SUBJECT_URI",
    "NEXT_PAGE_ID_TAG",
    "TENANT_RIGHTS_TAG",
    "GROUP_IDS_TAG",
    "OWNER_ID_TAG",
    "VISIBILITY_TAG",
    "ESTIMATE_COUNT",
    "GROUP_USER_RIGHTS_TAG",
    "JOIN_KEY_PARAM",
    "USER_TO_ADD_PARAM",
    "USER_TO_REMOVE_PARAM",
    "NEL_PARAM",
    "FORCE_PARAM",
    "RELATION_TAG",
    "APPLICATION_JSON_HEADER",
    "DEFAULT_TIMEOUT",
    "ENTITIES_TAG",
    "RESULT_TAG",
    "EXACT_MATCH",
    "DEFAULT_TOKEN_REFRESH_TIME",
    "EXTERNAL_USER_ID",
    "IS_OWNER_PARAM",
    "PRUNE_PARAM",
    "STATUS_FORCE_LIST",
    "DEFAULT_BACKOFF_FACTOR",
    "DEFAULT_MAX_RETRIES",
    "IndexType",
]

from knowledge.services import base
from knowledge.services import graph
from knowledge.services import ontology
from knowledge.services import tenant
from knowledge.services import users
