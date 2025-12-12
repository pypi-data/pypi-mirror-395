# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
import asyncio
from typing import Optional, Iterator, Tuple, AsyncIterator

import loguru

from knowledge.base.language import LocaleCode
from knowledge.base.ontology import OntologyClassReference, ThingObject
from knowledge.services.asyncio.graph import AsyncWacomKnowledgeService
from knowledge.services.graph import WacomKnowledgeService, Visibility

logger = loguru.logger


def count_things(
    wacom_client: WacomKnowledgeService,
    user_token: str,
    concept_type: OntologyClassReference,
    locale: Optional[LocaleCode] = None,
    visibility: Optional[Visibility] = None,
    only_own: Optional[bool] = None,
) -> int:
    """
    Counts the number of things.

    Parameters
    ----------
    wacom_client: WacomKnowledgeService
        The Wacom Knowledge Service
    user_token: str
        The user token
    concept_type: OntologyClassReference
        The concept type
    locale: Optional[LocaleCode]
        The locale
    visibility: Optional[Visibility]
        The visibility
    only_own: Optional[bool]
        Only own things
    Returns
    -------
    int
        The number of things
    """
    _, total, _ = wacom_client.listing(
        concept_type,
        visibility=visibility,
        locale=locale,
        is_owner=only_own,
        limit=1,
        estimate_count=True,
        auth_key=user_token,
    )
    return total


def count_things_session(
    wacom_client: WacomKnowledgeService,
    concept_type: OntologyClassReference,
    locale: Optional[LocaleCode] = None,
    visibility: Optional[Visibility] = None,
    only_own: Optional[bool] = None,
) -> int:
    """
    Counts the number of things.

    Parameters
    ----------
    wacom_client: WacomKnowledgeService
        The Wacom Knowledge Service
    concept_type: OntologyClassReference
        The concept type
    locale: Optional[LocaleCode] = [default:= None]
        The locale
    visibility: Optional[Visibility] = [default:= None]
        The visibility
    only_own: Optional[bool] = [default:= None]
        Only own things
    Returns
    -------
    int
        The number of things
    """
    _, total, _ = wacom_client.listing(
        concept_type, visibility=visibility, locale=locale, is_owner=only_own, limit=1, estimate_count=True
    )
    return total


def things_session_iter(
    wacom_client: WacomKnowledgeService,
    concept_type: OntologyClassReference,
    visibility: Optional[Visibility] = None,
    locale: Optional[LocaleCode] = None,
    only_own: bool = False,
    include_relations: Optional[bool] = None,
    fetch_size: int = 100,
    force_refresh_timeout: int = 360,
) -> Iterator[ThingObject]:
    """
    Iterates over all things using the current session configured for client.

    Parameters
    ----------
    wacom_client: WacomKnowledgeService
        The Wacom Knowledge Service
    concept_type: OntologyClassReference
        The class type
    visibility: Optional[Visibility] [default:= None]
        The visibility
    locale: Optional[LocaleCode] [default:= None]
        Only entities with this labels having a given locale
    only_own: bool [default:= False]
        Only own things
    include_relations: Optional[bool] = [default:= None]
        Include relations in the response.
    fetch_size: int [default:= 100]
        Fetch size.
    force_refresh_timeout: int [default:= 360]
        Force refresh timeout

    Yields
    -------
    ThingObject
        Next thing object

    Raises
    ------
    ValueError
        If no session is configured for client
    """
    next_page_id: Optional[str] = None
    if wacom_client.current_session is None:
        raise ValueError("No session configured for client")
    while True:
        # Refresh token if needed
        things, _, next_page_id = wacom_client.listing(
            concept_type,
            visibility=visibility,
            locale=locale,
            is_owner=only_own,
            limit=fetch_size,
            page_id=next_page_id,
            include_relations=include_relations,
        )
        if len(things) == 0:
            return
        for obj in things:
            # Refresh token if needed
            wacom_client.handle_token(force_refresh_timeout=force_refresh_timeout)
            yield obj


def things_iter(
    wacom_client: WacomKnowledgeService,
    user_token: str,
    refresh_token: str,
    concept_type: OntologyClassReference,
    visibility: Optional[Visibility] = None,
    locale: Optional[LocaleCode] = None,
    only_own: bool = False,
    include_relations: Optional[bool] = None,
    fetch_size: int = 100,
    force_refresh_timeout: int = 360,
    tenant_api_key: Optional[str] = None,
    external_user_id: Optional[str] = None,
) -> Iterator[Tuple[ThingObject, str, str]]:
    """
    Iterates over all things.

    Parameters
    ----------
    wacom_client: WacomKnowledgeService
        The Wacom Knowledge Service
    user_token: str
        The user token
    refresh_token: str
        The refresh token
    concept_type: OntologyClassReference
        The class type
    visibility: Optional[Visibility] [default:= None]
        The visibility
    locale: Optional[LocaleCode] [default:= None]
        Only entities with this labels having a given locale
    only_own: bool [default:= False]
        Only own things
    include_relations: Optional[bool] = [default:= None]
        Include relations in the response.
    fetch_size: int [default:= 100]
        Fetch size.
    force_refresh_timeout: int [default:= 360]
        Force refresh timeout
    tenant_api_key: Optional[str] [default:= None]
        The tenant API key
    external_user_id: Optional[str] [default:= None]
        The external user ID

    Yields
    -------
    obj: ThingObject
        Current thing
    user_token: str
        The user token
    refresh_token: str
        The refresh token
    """
    next_page_id: Optional[str] = None
    if tenant_api_key is not None and external_user_id is not None:
        # First login
        wacom_client.login(tenant_api_key=tenant_api_key, external_user_id=external_user_id)
    else:
        wacom_client.register_token(user_token, refresh_token)
    while True:
        # Refresh token if needed
        things, _, next_page_id = wacom_client.listing(
            concept_type,
            visibility=visibility,
            locale=locale,
            is_owner=only_own,
            limit=fetch_size,
            page_id=next_page_id,
            include_relations=include_relations,
        )
        if len(things) == 0:
            return
        for obj in things:
            # Refresh token if needed
            wacom_client.handle_token(force_refresh_timeout=force_refresh_timeout)
            yield obj, user_token, refresh_token


async def async_count_things(
    async_client: AsyncWacomKnowledgeService,
    user_token: str,
    concept_type: OntologyClassReference,
    locale: Optional[LocaleCode] = None,
    visibility: Optional[Visibility] = None,
    only_own: Optional[bool] = None,
) -> int:
    """
    Async counting of things given a concept type.

    Parameters
    ----------
    async_client: AsyncWacomKnowledgeService
        The Wacom Knowledge Service
    user_token: str
        The user token
    concept_type: OntologyClassReference
        The concept type
    locale: Optional[LocaleCode] = [default:= None]
        The locale
    visibility: Optional[Visibility] = [default:= None]
        The visibility
    only_own: Optional[bool] = [default:= None]
        Only own things

    Returns
    -------
    int
        The number of things
    """
    _, total, _ = await async_client.listing(
        concept_type,
        visibility=visibility,
        locale=locale,
        limit=1,
        estimate_count=True,
        is_owner=only_own,
        auth_key=user_token,
    )
    return total


async def async_count_things_session(
    async_client: AsyncWacomKnowledgeService,
    concept_type: OntologyClassReference,
    locale: Optional[LocaleCode] = None,
    visibility: Optional[Visibility] = None,
    only_own: Optional[bool] = None,
) -> int:
    """
    Async counting of things given a concept type using session.

    Parameters
    ----------
    async_client: AsyncWacomKnowledgeService
        The Wacom Knowledge Service
    concept_type: OntologyClassReference
        The concept type
    locale: Optional[LocaleCode] = [default:= None]
        The locale
    visibility: Optional[Visibility] = [default:= None]
        The visibility
    only_own: Optional[bool] = [default:= None]
        Only own things

    Returns
    -------
    int
        The number of things
    """
    _, total, _ = await async_client.listing(
        concept_type, visibility=visibility, is_owner=only_own, locale=locale, limit=1, estimate_count=True
    )
    return total


async def async_things_iter(
    async_client: AsyncWacomKnowledgeService,
    user_token: str,
    refresh_token: str,
    concept_type: OntologyClassReference,
    visibility: Optional[Visibility] = None,
    locale: Optional[LocaleCode] = None,
    only_own: Optional[bool] = None,
    include_relations: Optional[bool] = None,
    fetch_size: int = 100,
    force_refresh_timeout: int = 360,
    tenant_api_key: Optional[str] = None,
    external_user_id: Optional[str] = None,
) -> AsyncIterator[Tuple[ThingObject, str, str]]:
    """
    Generates an asynchronous iterator that retrieves and yields objects along with user and refresh tokens.

    Parameters
    ----------
    async_client : AsyncWacomKnowledgeService
        The asynchronous client used to communicate with the Wacom knowledge service.
    user_token : str
        The current user's authentication token.
    refresh_token : str
        The token used to refresh the user’s session when expired.
    concept_type : OntologyClassReference
        The type of concept to filter the retrieved objects by.
    visibility : Optional[Visibility], optional
        The visibility level used to filter the retrieved objects.
    locale : Optional[LocaleCode], optional
        The locale used to localize object retrieval.
    only_own : Optional[bool], optional
        If True, restricts retrieval to objects owned by the current user.
    include_relations : Optional[bool], optional
        If True, includes relations in the retrieved objects.
    fetch_size : int, optional
        The number of objects to fetch per page. Default is 100.
    force_refresh_timeout : int, optional
        Forces a timeout duration for token refresh handling. Default is 360 seconds.
    tenant_api_key : Optional[str], optional
        The tenant-specific API key for the user’s organization.
    external_user_id : Optional[str], optional
        The external identifier for the user in the tenant's system.

    Returns
    -------
    AsyncIterator[Tuple[ThingObject, str, str]]
        An asynchronous iterator yielding retrieved objects, the updated user token, and the refresh token.
    """
    next_page_id: Optional[str] = None
    if tenant_api_key is not None and external_user_id is not None:
        # First login
        await async_client.login(tenant_api_key=tenant_api_key, external_user_id=external_user_id)
    else:
        await async_client.register_token(user_token, refresh_token)
    while True:
        things, _, next_page_id = await async_client.listing(
            concept_type,
            visibility=visibility,
            locale=locale,
            is_owner=only_own,
            limit=fetch_size,
            page_id=next_page_id,
            include_relations=include_relations,
        )
        if len(things) == 0:
            return
        for obj in things:
            user_token, refresh_token = await async_client.handle_token(force_refresh_timeout=force_refresh_timeout)
            yield obj, user_token, refresh_token


async def async_things_session_iter(
    async_client: AsyncWacomKnowledgeService,
    concept_type: OntologyClassReference,
    visibility: Optional[Visibility] = None,
    locale: Optional[LocaleCode] = None,
    only_own: Optional[bool] = None,
    include_relations: Optional[bool] = None,
    fetch_size: int = 100,
    force_refresh_timeout: int = 360,
) -> AsyncIterator[ThingObject]:
    """
    Asynchronous iterator over all things of a given type using session.

    Parameters
    ----------
    async_client: AsyncWacomKnowledgeService
        The Wacom Knowledge Service
    concept_type: OntologyClassReference
        The class type
    visibility: Optional[Visibility] [default:= None]
        The visibility
    locale: Optional[LocaleCode] [default:= None]
        Only entities with this label having a given locale
    only_own: Optional[bool] = [default:= None]
        Only own things
    include_relations: Optional[bool] = [default:= None]
        Include relations
    fetch_size: int [default:= 100]
        Fetch size.
    force_refresh_timeout: int [default:= 360]
        Force refresh timeout

    Yields
    -------
    ThingObject
        Next thing object
    """
    next_page_id: Optional[str] = None
    if async_client.current_session is None:
        raise ValueError("No session configured for client")

    while True:
        try:
            things, _, next_page_id = await async_client.listing(
                concept_type,
                visibility=visibility,
                is_owner=only_own,
                locale=locale,
                limit=fetch_size,
                page_id=next_page_id,
                include_relations=include_relations,
            )
            if len(things) == 0:
                return
            for obj in things:
                await async_client.handle_token(force_refresh_timeout=force_refresh_timeout)
                if obj.owner or not only_own:
                    yield obj
        except TimeoutError as e:
            logger.error(f"Timeout error while fetching things: {e}")
            await asyncio.sleep(2)  # Wait before retrying
