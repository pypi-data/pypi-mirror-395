# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import urllib.parse
from typing import List, Any, Optional, Dict

from requests import Response

from knowledge.base.access import GroupAccessRight
from knowledge.base.ontology import NAME_TAG
from knowledge.services import (
    GROUP_USER_RIGHTS_TAG,
    DEFAULT_TIMEOUT,
    JOIN_KEY_PARAM,
    USER_TO_ADD_PARAM,
    USER_TO_REMOVE_PARAM,
    FORCE_PARAM,
)
from knowledge.services.base import WacomServiceAPIClient, handle_error

# -------------------------------------- Constant flags ----------------------------------------------------------------
from knowledge.services.users import User, FORCE_TAG, LIMIT_TAG, OFFSET_TAG


class Group:
    """
    Entities and users can be assigned to groups.
    If the entity is assigned to a group the users have access to the entity with the rights defined in the group.

    Parameters
    ----------
    tenant_id: str
        Tenant id
    group_id: str
        Group id
    owner: str
        User id who has created the group.
    name: str
        Name of the group.
    join_key: str
        Key which is required to join the group
    rights: GroupAccessRight
        Access right for group.

    Attributes
    ----------
    id: str
        Group identifier
    tenant_id: str
        Tenant identifier
    owner_id: str
        Owner identifier
    name: str
        Name of the group
    join_key: str
        Key which is required to join the group
    group_access_rights: GroupAccessRight
        Access rights for the group
    """

    def __init__(self, tenant_id: str, group_id: str, owner: str, name: str, join_key: str, rights: GroupAccessRight):
        self.__tenant_id: str = tenant_id
        self.__group_id: str = group_id
        self.__owner_id: str = owner
        self.__name: str = name
        self.__join_key: str = join_key
        self.__rights: GroupAccessRight = rights

    @property
    def id(self) -> str:
        """Group id."""
        return self.__group_id

    @property
    def tenant_id(self) -> str:
        """Tenant ID."""
        return self.__tenant_id

    @property
    def owner_id(self) -> Optional[str]:
        """Owner id (internal id) of the user, who owns the group."""
        return self.__owner_id

    @property
    def name(self) -> str:
        """Name of the group."""
        return self.__name

    @property
    def join_key(self) -> str:
        """Key for joining the group."""
        return self.__join_key

    @property
    def group_access_rights(self) -> GroupAccessRight:
        """Rights for group."""
        return self.__rights

    @classmethod
    def parse(cls, param: Dict[str, Any]) -> "Group":
        """Parse group from dictionary.

        Arguments
        ---------
        param: Dict[str, Any]
            Dictionary containing group information.

        Returns
        -------
        instance: Group
            The group object
        """
        tenant_id: str = param.get("tenantId")
        owner_id: str = param.get("ownerId")
        join_key: str = param.get("joinKey")
        group_id: str = param.get("id")
        name: str = param.get("name")
        rights: GroupAccessRight = GroupAccessRight.parse(param.get("groupUserRights", ["Read"]))
        return Group(
            tenant_id=tenant_id, group_id=group_id, owner=owner_id, join_key=join_key, name=name, rights=rights
        )

    def __repr__(self):
        return f"<Group: id:={self.id}, name:={self.name}, group access right:={self.group_access_rights}]>"


class GroupInfo(Group):
    """
    Extended group information including the list of users in the group.

    Parameters
    ----------
    tenant_id : str
        Identifier of the tenant the group belongs to.
    group_id : str
        Unique identifier of the group.
    owner : str
        Owner id of the group.
    name : str
        Display name of the group.
    join_key : str
        Key required to join the group.
    rights : GroupAccessRight
        Access rights associated with the group.
    group_users : List[User]
        Users that belong to the group.

    Attributes
    ----------
    group_users : List[User]
        List of all users that are part of the group.
    """

    _group_users: List[User]

    def __init__(
        self,
        tenant_id: str,
        group_id: str,
        owner: str,
        name: str,
        join_key: str,
        rights: GroupAccessRight,
        group_users: List[User],
    ):
        self._group_users: List[User] = group_users
        super().__init__(tenant_id, group_id, owner, name, join_key, rights)

    @property
    def group_users(self) -> List:
        """List of all users that are part of the group."""
        return self._group_users

    @classmethod
    def parse(cls, param: Dict[str, Any]) -> "GroupInfo":
        tenant_id: str = param.get("tenantId")
        owner_id: str = param.get("ownerId")
        join_key: str = param.get("joinKey")
        group_id: str = param.get("id")
        name: str = param.get("name")
        rights: GroupAccessRight = GroupAccessRight.parse(param.get("groupUserRights", ["Read"]))
        return GroupInfo(
            tenant_id=tenant_id,
            group_id=group_id,
            owner=owner_id,
            join_key=join_key,
            name=name,
            rights=rights,
            group_users=[User.parse(u) for u in param.get("users", [])],
        )

    def __repr__(self):
        return (
            f"<GroupInfo: id:={self.id}, name:={self.name}, group access right:={self.group_access_rights}, "
            f"number of users:={len(self.group_users)}]>"
        )


class GroupManagementService(WacomServiceAPIClient):
    """
    Group Management Service API
    -----------------------------
    The service is managing groups.

    Functionality:
        - List all groups
        - Create group
        - Assign users to group
        - Share entities with group

    Parameters
    ----------
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """

    GROUP_ENDPOINT: str = "group"
    """"Endpoint for all group related functionality."""

    def __init__(
        self,
        service_url: str,
        application_name: str = "Group Management Service",
        service_endpoint: str = "graph/v1",
    ):
        super().__init__(service_url=service_url, application_name=application_name, service_endpoint=service_endpoint)

    # ------------------------------------------ Groups handling ------------------------------------------------------

    def create_group(
        self,
        name: str,
        rights: GroupAccessRight = GroupAccessRight(read=True),
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> Group:
        """
        Creates a group.

        Parameters
        ----------
        name: str
            Name of the tenant
        rights: GroupAccessRight
            Access rights
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Returns
        -------
        group: Group
            Instance of the group.

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}"
        payload: Dict[str, str] = {NAME_TAG: name, GROUP_USER_RIGHTS_TAG: rights.to_list()}
        response: Response = self.request_session.post(
            url,
            json=payload,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            return Group.parse(response.json())
        raise handle_error("Creating of group failed.", response, payload=payload)

    def update_group(
        self,
        group_id: str,
        name: str,
        rights: GroupAccessRight = GroupAccessRight,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Updates a group.

        Parameters
        ----------
        group_id: str
            ID of the group.
        name: str
            Name of the tenant
        rights: GroupAccessRight
            Access rights
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}"
        payload: Dict[str, str] = {NAME_TAG: name, GROUP_USER_RIGHTS_TAG: rights.to_list()}
        response: Response = self.request_session.patch(
            url,
            json=payload,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Update of group failed.", response, payload=payload)

    def delete_group(
        self,
        group_id: str,
        force: bool = False,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Delete a group.

        Parameters
        ----------
        group_id: str
            ID of the group.
        force: bool (Default = False)
            If True, the group will be deleted even if it is not empty.
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)

        Raises
        ------
        WacomServiceException
        If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}"
        params: Dict[str, str] = {FORCE_TAG: str(force).lower()}
        response: Response = self.request_session.delete(
            url,
            params=params,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Deletion of group failed.", response, parameters=params)

    def listing_groups(
        self,
        admin: bool = False,
        limit: int = 20,
        offset: int = 0,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> List[Group]:
        """
        Listing all groups configured for this instance.

        Parameters
        ----------
        admin: bool (default:= False)
            Uses admin privilege to show all groups of the tenants.
            Requires user to have the role: TenantAdmin
        limit: int (default:= 20)
            Maximum number of groups to return.
        offset: int (default:= 0)
            Offset of the first group to return.
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Returns
        -------
        user:  List[Groups]
            List of groups.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}"
        params: Dict[str, int] = {}
        if admin:
            url += "/admin"
            params[LIMIT_TAG] = limit
            params[OFFSET_TAG] = offset
        response: Response = self.request_session.get(
            url,
            params=params,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            groups: List[Dict[str, Any]] = response.json()
            return [Group.parse(g) for g in groups]
        raise handle_error("Listing of groups failed.", response, parameters=params)

    def group(
        self,
        group_id: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> GroupInfo:
        """Get a group.

        Parameters
        ----------
        group_id: str
            Group ID
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Returns
        -------
        group: GroupInfo
            Instance of the group

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}"
        response: Response = self.request_session.get(
            url,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            group: Dict[str, Any] = response.json()
            return GroupInfo.parse(group)
        raise handle_error("Getting of group information failed.", response)

    def join_group(
        self,
        group_id: str,
        join_key: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """User joining a group with his auth token.

        Parameters
        ----------
        group_id: str
            Group ID
        join_key: str
            Key which is used to join the group.
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}/join"
        params: Dict[str, str] = {
            JOIN_KEY_PARAM: join_key,
        }
        response: Response = self.request_session.post(
            url,
            params=params,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Joining of group failed.", response, parameters=params)

    def leave_group(
        self,
        group_id: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """User leaving a group with his auth token.

        Parameters
        ----------
        group_id: str
            Group ID
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}/leave"
        response: Response = self.request_session.post(
            url,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Leaving of group failed.", response)

    def add_user_to_group(
        self,
        group_id: str,
        user_id: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Adding a user to a group.

        Parameters
        ----------
        group_id: str
            Group ID
        user_id: str
            User who is added to the group
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}/user/add"
        params: Dict[str, str] = {
            USER_TO_ADD_PARAM: user_id,
        }
        response: Response = self.request_session.post(
            url,
            params=params,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Adding of user to group failed.", response, parameters=params)

    def remove_user_from_group(
        self,
        group_id: str,
        user_id: str,
        force: bool = False,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Remove a user from a group.

        Parameters
        ----------
        group_id: str
            Group ID
        user_id: str
            User who is remove from the group
        force: bool
            If true remove user and entities owned by the user if any
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}/user/remove"
        params: Dict[str, str] = {USER_TO_REMOVE_PARAM: user_id, FORCE_PARAM: force}
        response: Response = self.request_session.post(
            url,
            params=params,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Removing of user from group failed.", response, parameters=params)

    def add_entity_to_group(
        self,
        group_id: str,
        entity_uri: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Adding an entity to a group.

        Parameters
        ----------
        group_id: str
            Group ID
        entity_uri: str
            Entity URI
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        uri: str = urllib.parse.quote(entity_uri)
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}/entity/{uri}/add"

        response: Response = self.request_session.post(
            url,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Adding of entity to group failed.", response)

    def remove_entity_to_group(
        self,
        group_id: str,
        entity_uri: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Remove an entity from group.

        Parameters
        ----------
        group_id: str
            Group ID
        entity_uri: str
            URI of entity
        auth_key: Optional[str]
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int
            Timeout for the request (default: 60 seconds)
        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        uri: str = urllib.parse.quote(entity_uri)
        url: str = f"{self.service_base_url}{GroupManagementService.GROUP_ENDPOINT}/{group_id}/entity/{uri}/remove"

        response: Response = self.request_session.post(
            url,
            verify=self.verify_calls,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if not response.ok:
            raise handle_error("Removing of entity from group failed.", response)
