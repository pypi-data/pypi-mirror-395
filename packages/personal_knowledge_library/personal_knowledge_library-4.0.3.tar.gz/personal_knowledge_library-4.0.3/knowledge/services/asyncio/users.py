# -*- coding: utf-8 -*-
# Copyright © 2024 Wacom. All rights reserved.
from datetime import datetime
from typing import Any, Union, Dict, List, Tuple, Optional

import orjson

from knowledge import logger
from knowledge.services import APPLICATION_JSON_HEADER, EXPIRATION_DATE_TAG
from knowledge.services.asyncio.base import AsyncServiceAPIClient, handle_error
from knowledge.services.base import WacomServiceAPIClient
from knowledge.services.users import (
    UserRole,
    USER_AGENT_TAG,
    TENANT_API_KEY_FLAG,
    OFFSET_TAG,
    LIMIT_TAG,
    User,
    USER_ID_TAG,
    EXTERNAL_USER_ID_TAG,
    FORCE_TAG,
    ROLES_TAG,
    META_DATA_TAG,
    CONTENT_TYPE_FLAG,
    DEFAULT_TIMEOUT,
    INTERNAL_USER_ID_TAG,
)


class AsyncUserManagementService(AsyncServiceAPIClient):
    """
    Async User-Management Service API
    ---------------------------------
    Functionality:
        - List all users
        - Create / update / delete users

    Parameters
    ----------
    application_name: str
        Name of the application
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """

    USER_DETAILS_ENDPOINT: str = f"{WacomServiceAPIClient.USER_ENDPOINT}/internal-id"

    def __init__(
        self,
        service_url: str,
        application_name: str = "UserManagementServiceAPI",
        base_auth_url: Optional[str] = None,
        service_endpoint: str = "graph/v1",
        verify_calls: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        super().__init__(
            service_url=service_url,
            application_name=application_name,
            base_auth_url=base_auth_url,
            service_endpoint=service_endpoint,
            verify_calls=verify_calls,
            timeout=timeout,
        )

    # ------------------------------------------ Users handling --------------------------------------------------------

    async def create_user(
        self,
        tenant_key: str,
        external_id: str,
        meta_data: Dict[str, str] = None,
        roles: List[UserRole] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> Tuple[User, str, str, datetime]:
        """
        Creates a user for a tenant.

        Parameters
        ----------
        tenant_key: str -
            API key for tenant
        external_id: str -
            External id of user identification service.
        meta_data: Dict[str, str]
            Meta-data dictionary.
        roles: List[UserRole]
            List of roles.
        timeout: int
            Denotes the timeout for the request in seconds (default: 60 seconds).

        Returns
        -------
        user: User
            Instance of the user
        token: str
            Auth token for user
        refresh_key: str
            Refresh token
        expiration_time: datetime
            Expiration time
        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{AsyncUserManagementService.USER_ENDPOINT}"
        headers: dict = {
            USER_AGENT_TAG: self.user_agent,
            TENANT_API_KEY_FLAG: tenant_key,
            CONTENT_TYPE_FLAG: "application/json",
        }
        payload: dict = {
            EXTERNAL_USER_ID_TAG: external_id,
            META_DATA_TAG: meta_data if meta_data is not None else {},
            ROLES_TAG: [r.value for r in roles] if roles is not None else [UserRole.USER.value],
        }
        session = await self.asyncio_session()
        response = await session.post(
            url, headers=headers, json=payload, timeout=timeout, verify_ssl=self.verify_calls, ignore_auth=True
        )
        if response.ok:
            results: Dict[str, Union[str, Dict[str, str], List[str]]] = await response.json(loads=orjson.loads)
            try:
                date_object: datetime = datetime.fromisoformat(results["token"][EXPIRATION_DATE_TAG])
            except (TypeError, ValueError) as _:
                date_object: datetime = datetime.now()
                logger.warning(f'Parsing of expiration date failed. {results["token"][EXPIRATION_DATE_TAG]}')
            return (
                User.parse(results["user"]),
                results["token"]["accessToken"],
                results["token"]["refreshToken"],
                date_object,
            )
        raise await handle_error("Failed to create the user.", response, headers=headers, payload=payload)

    async def update_user(
        self,
        tenant_key: str,
        internal_id: str,
        external_id: str,
        meta_data: Dict[str, str] = None,
        roles: List[UserRole] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Updates user for a tenant.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        internal_id: str
            Internal id of semantic service.
        external_id: str
            External id of user identification service.
        meta_data: Dict[str, str]
            Meta-data dictionary.
        roles: List[UserRole]
            List of roles.
        timeout: int
            Denotes the timeout for the request in seconds (default: 60 seconds).

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{AsyncUserManagementService.USER_ENDPOINT}"
        headers: Dict[str, str] = {
            USER_AGENT_TAG: self.user_agent,
            TENANT_API_KEY_FLAG: tenant_key,
            CONTENT_TYPE_FLAG: APPLICATION_JSON_HEADER,
        }
        payload: Dict[str, Any] = {
            META_DATA_TAG: meta_data if meta_data is not None else {},
            ROLES_TAG: [r.value for r in roles] if roles is not None else [UserRole.USER.value],
        }
        params: Dict[str, str] = {USER_ID_TAG: internal_id, EXTERNAL_USER_ID_TAG: external_id}
        session = await self.asyncio_session()
        response = await session.patch(
            url,
            headers=headers,
            json=payload,
            params=params,
            timeout=timeout,
            verify_ssl=self.verify_calls,
            ignore_auth=True,
        )
        if not response.ok:
            raise await handle_error("Failed to update the user.", response, headers=headers, payload=payload)

    async def delete_user(
        self, tenant_key: str, external_id: str, internal_id: str, force: bool = False, timeout: int = DEFAULT_TIMEOUT
    ):
        """Deletes user from tenant.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        external_id: str
            External id of user identification service.
        internal_id: str
            Internal id of user.
        force: bool
            If set to true, removes all user data including groups and entities.
        timeout: int
            Default timeout for the request (in seconds) (Default:= 60 seconds).

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{AsyncUserManagementService.USER_ENDPOINT}"
        headers: Dict[str, str] = {TENANT_API_KEY_FLAG: tenant_key}
        params: Dict[str, str] = {USER_ID_TAG: internal_id, EXTERNAL_USER_ID_TAG: external_id, FORCE_TAG: str(force)}
        session = await self.asyncio_session()
        response = await session.delete(
            url, headers=headers, params=params, timeout=timeout, verify_ssl=self.verify_calls, ignore_auth=True
        )
        if not response.ok:
            raise await handle_error("Failed to delete the user.", response, headers=headers)

    async def user_internal_id(self, tenant_key: str, external_id: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """User internal id.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        external_id: str
            External id of user
        timeout: int
            Default timeout for the request (in seconds) (Default:= 60 seconds).
        Returns
        -------
        internal_user_id: str
            Internal id of users

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{AsyncUserManagementService.USER_DETAILS_ENDPOINT}"
        headers: dict = {TENANT_API_KEY_FLAG: tenant_key}
        parameters: Dict[str, str] = {EXTERNAL_USER_ID_TAG: external_id}
        session = await self.asyncio_session()
        response = await session.get(
            url, headers=headers, params=parameters, timeout=timeout, verify_ssl=self.verify_calls, ignore_auth=True
        )
        if response.ok:
            response_dict: Dict[str, Any] = await response.json(loads=orjson.loads)
        else:
            raise await handle_error("Failed to get the user.", response, headers=headers)
        return response_dict[INTERNAL_USER_ID_TAG]

    async def listing_users(
        self, tenant_key: str, offset: int = 0, limit: int = 20, timeout: int = DEFAULT_TIMEOUT
    ) -> List[User]:
        """
        Listing all users configured for this instance.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        offset: int - [optional]
            Offset value to define starting position in a list. [DEFAULT:= 0]
        limit: int - [optional]
            Define the limit of the list size. [DEFAULT:= 20]
        timeout: int - [optional]
            Default timeout for the request (in seconds) (Default:= 60 seconds).

        Returns
        -------
        user: List[User]
            List of users.
        """
        url: str = f"{self.service_base_url}{AsyncUserManagementService.USER_ENDPOINT}"
        headers: Dict[str, str] = {TENANT_API_KEY_FLAG: tenant_key}
        params: Dict[str, int] = {OFFSET_TAG: offset, LIMIT_TAG: limit}
        session = await self.asyncio_session()
        response = await session.get(
            url, headers=headers, params=params, timeout=timeout, verify_ssl=self.verify_calls, ignore_auth=True
        )
        if response.ok:
            users: List[Dict[str, Any]] = await response.json(loads=orjson.loads)
            results: List[User] = []
            for u in users:
                results.append(User.parse(u))
            return results
        raise await handle_error("Listing of users failed.", response, headers=headers, parameters=params)
