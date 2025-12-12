# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import enum
from datetime import datetime
from typing import Any, Union, Dict, List, Tuple, Optional

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from knowledge import logger
from knowledge.services import EXPIRATION_DATE_TAG, STATUS_FORCE_LIST, DEFAULT_MAX_RETRIES, DEFAULT_BACKOFF_FACTOR
from knowledge.services.base import WacomServiceAPIClient, handle_error

# -------------------------------------- Constant flags ----------------------------------------------------------------
TENANT_ID: str = "tenantId"
USER_ID_TAG: str = "userId"
LIMIT_TAG: str = "limit"
OFFSET_TAG: str = "offset"
ROLES_TAG: str = "roles"
META_DATA_TAG: str = "metadata"
INTERNAL_USER_ID_TAG: str = "internalUserId"
EXTERNAL_USER_ID_TAG: str = "externalUserId"
FORCE_TAG: str = "force"
CONTENT_TYPE_FLAG: str = "Content-Type"
TENANT_API_KEY_FLAG: str = "x-tenant-api-key"
USER_AGENT_TAG: str = "User-Agent"
DEFAULT_TIMEOUT: int = 60


class UserRole(enum.Enum):
    """
    UserRole
    --------
    Roles of the users in
    """

    USER = "User"
    """User only has control over his personal entities."""
    ADMIN = "TenantAdmin"
    """TenantAdmin has access to all entities independent of the access rights."""
    CONTENT_MANAGER = "ContentManager"
    """ContentManager is a special user for content accounts. The same visibility rules as for USER accounts apply."""


USER_ROLE_MAPPING: Dict[str, UserRole] = {str(r.value): r for r in UserRole}


class User:
    """
    User
    -----
    In Personal Knowledge backend is linking a user to a shadow user which is used within the personal knowledge graph.

    Parameters
    ----------
    tenant_id: str
        Tenant id
    user_id: str
        User id
    external_user_id: str
        External user id, referencing the user to an authentication system.
    meta_data: Dict[str, Any]
        Metadata associated with user.
    user_roles: List[UserRole]
        List of user roles.
    """

    def __init__(
        self, tenant_id: str, user_id: str, external_user_id: str, meta_data: Dict[str, Any], user_roles: List[UserRole]
    ):
        self.__tenant_id: str = tenant_id
        self.__user_id: str = user_id
        self.__external_user_id: str = external_user_id
        self.__meta_data: Dict[str, Any] = meta_data
        self.__user_roles: List[UserRole] = user_roles

    @property
    def id(self) -> str:
        """User id."""
        return self.__user_id

    @property
    def tenant_id(self) -> str:
        """Tenant ID."""
        return self.__tenant_id

    @property
    def external_user_id(self) -> str:
        """External user id, referencing to external user authentication."""
        return self.__external_user_id

    @property
    def meta_data(self) -> Dict[str, Any]:
        """Meta data for user."""
        return self.__meta_data

    @meta_data.setter
    def meta_data(self, value: Dict[str, Any]):
        self.__meta_data = value

    @property
    def user_roles(self) -> List[UserRole]:
        """List of user roles"""
        return self.__user_roles

    @classmethod
    def parse(cls, param: Dict[str, Any]) -> "User":
        """
        Parse user from dictionary.
        Parameters
        ----------
        param: Dict[str, Any]
            Dictionary containing user information.

        Returns
        -------
        user: User
            Instance of user.
        """
        user_id: str = param["id"]
        tenant_id: str = param[TENANT_ID]
        external_user_id: str = param["externalUserId"]
        meta_data: Dict[str, Any] = {}
        if META_DATA_TAG in param and param[META_DATA_TAG] is not None:
            meta_data = param[META_DATA_TAG]
        # Support the old version of the user management service
        elif "metaData" in param:
            meta_data = param["metaData"]
        user_roles: List[UserRole] = [USER_ROLE_MAPPING[r] for r in param["roles"]]
        return User(
            tenant_id=tenant_id,
            user_id=user_id,
            external_user_id=external_user_id,
            meta_data=meta_data,
            user_roles=user_roles,
        )

    def __repr__(self):
        return f"<User: id:={self.id}, external user id:={self.external_user_id}, user roles:= {self.user_roles}]>"


class UserManagementServiceAPI(WacomServiceAPIClient):
    """
    User-Management Service API
    -----------------------------

    Functionality:
        - List all users
        - Create / update / delete users

    Parameters
    ----------
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """

    USER_DETAILS_ENDPOINT: str = f"{WacomServiceAPIClient.USER_ENDPOINT}/internal-id"

    def __init__(
        self,
        service_url: str,
        application_name: str = "UserManagement Service API",
        base_auth_url: Optional[str] = None,
        service_endpoint: str = "graph/v1",
        verify_calls: bool = True,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ):
        super().__init__(
            service_url=service_url,
            application_name=application_name,
            base_auth_url=base_auth_url,
            service_endpoint=service_endpoint,
            verify_calls=verify_calls,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

    # ------------------------------------------ Users handling --------------------------------------------------------

    def create_user(
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
        timeout: int - [optional]
            Timeout for the request. [DEFAULT:= 60]

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
        url: str = f"{self.service_base_url}{UserManagementServiceAPI.USER_ENDPOINT}"

        payload: dict = {
            EXTERNAL_USER_ID_TAG: external_id,
            META_DATA_TAG: meta_data if meta_data is not None else {},
            ROLES_TAG: [r.value for r in roles] if roles is not None else [UserRole.USER.value],
        }
        response: Response = self.request_session.post(
            url,
            json=payload,
            timeout=timeout,
            verify=self.verify_calls,
            headers={TENANT_API_KEY_FLAG: tenant_key},
            ignore_auth=True,
        )
        if response.ok:
            results: Dict[str, Union[str, Dict[str, str], List[str]]] = response.json()
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
        raise handle_error("Failed to create user.", response)

    def update_user(
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
        timeout: int - [optional]
            Timeout for the request. [DEFAULT:= 60]

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{UserManagementServiceAPI.USER_ENDPOINT}"
        payload: Dict[str, Any] = {
            META_DATA_TAG: meta_data if meta_data is not None else {},
            ROLES_TAG: [r.value for r in roles] if roles is not None else [UserRole.USER.value],
        }
        params: Dict[str, str] = {USER_ID_TAG: internal_id, EXTERNAL_USER_ID_TAG: external_id}
        response: Response = self.request_session.patch(
            url,
            json=payload,
            params=params,
            timeout=timeout,
            verify=self.verify_calls,
            headers={TENANT_API_KEY_FLAG: tenant_key},
            ignore_auth=True,
        )
        if not response.ok:
            raise handle_error("Updating of user failed.", response)

    def delete_user(
        self,
        tenant_key: str,
        external_id: str,
        internal_id: str,
        force: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
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
        timeout: int - [optional]
            Timeout for the request. [DEFAULT:= 60]

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{UserManagementServiceAPI.USER_ENDPOINT}"
        params: Dict[str, str] = {USER_ID_TAG: internal_id, EXTERNAL_USER_ID_TAG: external_id, FORCE_TAG: force}
        response: Response = self.request_session.delete(
            url,
            params=params,
            timeout=timeout,
            verify=self.verify_calls,
            headers={TENANT_API_KEY_FLAG: tenant_key},
            ignore_auth=True,
        )
        if not response.ok:
            raise handle_error("Deletion of user failed.", response)

    def user_internal_id(
        self,
        tenant_key: str,
        external_id: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> str:
        """User internal id.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        external_id: str
            External id of user
        timeout: int - [optional]
            Timeout for the request. [DEFAULT:= 60]

        Returns
        -------
        internal_user_id: str
            Internal id of users

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{UserManagementServiceAPI.USER_DETAILS_ENDPOINT}"
        parameters: Dict[str, str] = {EXTERNAL_USER_ID_TAG: external_id}
        response: Response = self.request_session.get(
            url,
            params=parameters,
            timeout=timeout,
            verify=self.verify_calls,
            headers={TENANT_API_KEY_FLAG: tenant_key},
            ignore_auth=True,
        )
        if response.ok:
            response_dict: Dict[str, Any] = response.json()
            return response_dict[INTERNAL_USER_ID_TAG]
        raise handle_error("Retrieval of user internal id failed.", response)

    def listing_users(
        self,
        tenant_key: str,
        offset: int = 0,
        limit: int = 20,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> List[User]:
        """
        Listing all users configured for this instance.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        offset: int - [optional]
            Offset value to define the starting position in a list. [DEFAULT:= 0]
        limit: int - [optional]
            Define the limit of the list size. [DEFAULT:= 20]
        timeout: int - [optional]
            Timeout for the request. [DEFAULT:= 60]

        Returns
        -------
        user: List[User]
            List of users.
        """
        url: str = f"{self.service_base_url}{UserManagementServiceAPI.USER_ENDPOINT}"
        params: Dict[str, int] = {OFFSET_TAG: offset, LIMIT_TAG: limit}
        response: Response = self.request_session.get(
            url,
            params=params,
            timeout=timeout,
            verify=self.verify_calls,
            headers={TENANT_API_KEY_FLAG: tenant_key},
            ignore_auth=True,
        )
        if response.ok:
            users: List[Dict[str, Any]] = response.json()
            results: List[User] = []
            for u in users:
                results.append(User.parse(u))
            return results
        raise handle_error("Listing of users failed.", response)
