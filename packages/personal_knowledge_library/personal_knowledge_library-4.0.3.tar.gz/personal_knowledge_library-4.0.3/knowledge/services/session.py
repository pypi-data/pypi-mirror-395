# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
"""
This module contains the session management.
There are three types of sessions:
    - **TimedSession**: The session is only valid until the token expires.
        There is no refresh token, thus the session cannot be refreshed.
    - **RefreshableSession**: The session is valid until the token expires.
        There is a refresh token, thus the session can be refreshed.
    - **PermanentSession**: The session is valid until the token expires.
        There is a refresh token, thus the session can be refreshed.
        Moreover, the session is bound to then _tenant api key_ and the _external user id_, which can be used to
        re-login when the refresh token expires.
"""
import hashlib
import logging
import threading
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Union, Optional, Dict, Any

import jwt

logger: logging.Logger = logging.getLogger(__name__)


class Session(ABC):
    """
    Session
    -------

    Represents an abstract session for managing authentication tokens and tracking session state.

    This class provides an interface for managing sessions, including properties for authentication and
    refresh tokens, session expiration status, and time until expiration. It enforces implementation of
    essential methods for handling sessions in derived classes.

    Attributes
    ----------
    id : str
        Unique session id, which will be the same for the same external user id, tenant, and instance of the service.
    auth_token : str
        Authentication key used to identify an external user within private knowledge.
    tenant_id : str
        Tenant id.
    refresh_token : Optional[str]
        Refresh token used to refresh the session.
    refreshable : bool
        Indicator of whether the session is refreshable.
    expired : bool
        Indicator of whether the session is expired.
    expires_in : float
        Seconds remaining until the token expires.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique session id, which will be the same for the same external user id, tenant,
        and instance of the service."""
        raise NotImplementedError

    @property
    @abstractmethod
    def auth_token(self) -> str:
        """Authentication key. The authentication key is used to identify an external user within private knowledge."""
        raise NotImplementedError

    @property
    @abstractmethod
    def tenant_id(self) -> str:
        """Tenant id."""
        raise NotImplementedError

    @property
    def refresh_token(self) -> Optional[str]:
        """Refresh token. The refresh token is used to refresh the session."""
        return None

    @property
    @abstractmethod
    def refreshable(self) -> bool:
        """Is the session refreshable."""
        raise NotImplementedError

    @property
    @abstractmethod
    def expired(self) -> bool:
        """Is the session expired."""
        raise NotImplementedError

    @property
    @abstractmethod
    def expires_in(self) -> float:
        """Seconds until token is expired in seconds."""
        raise NotImplementedError

    @abstractmethod
    def update_session(self, auth_token: str, refresh_token: str):
        """
        Update the session.

        Parameters
        ----------
        auth_token: str
            The refreshed authentication token.
        refresh_token: str
            The refreshed refresh token.
        """
        raise NotImplementedError


class TimedSession(Session):
    """
    TimedSession
    ------------
    Manages a time-limited authentication session with a service.

    This class represents a session authenticated via a JWT token with an expiration timestamp.
    It provides utilities to decode and extract information such as roles, tenant id, service URL,
    and external user ID. Additionally, it generates and validates session IDs and keeps track of
    expiration and refreshability.

    Attributes
    ----------
    tenant_id : str
        ID of the tenant associated with the session.
    roles : str
        Roles assigned to the session.
    service_url : str
        URL of the service the session is authenticated with.
    external_user_id : str
        External user identifier for the session.
    expiration : datetime
        Timestamp indicating when the session token expires.
    auth_token : str
        JWT token used for authenticating the session.
    id : str
        Unique identifier for the session derived from the service URL, tenant ID, and external user ID.
    expires_in : float
        Number of seconds until the session token expires.
    expired : bool
        Indicates whether the session has expired.
    refreshable : bool
        Indicates whether the session token can be refreshed.
    """

    def __init__(self, auth_token: str):
        self.__auth_token: str = auth_token
        self._auth_token_details_(auth_token)

    def _auth_token_details_(self, auth_token: str):
        """
        Extract the details from the authentication token.
        Parameters
        ----------
        auth_token: str
            Authentication token
        """
        structures: Dict[str, Any] = jwt.decode(auth_token, options={"verify_signature": False})
        if (
            "tenant" not in structures
            or "roles" not in structures
            or "exp" not in structures
            or "iss" not in structures
            or "ext-sub" not in structures
        ):
            raise ValueError("Invalid authentication token.")
        self.__tenant_id: str = structures["tenant"]
        self.__roles: str = structures["roles"]
        self.__timestamp: datetime = datetime.fromtimestamp(structures["exp"], tz=timezone.utc)
        self.__service_url: str = structures["iss"]
        self.__external_user_id: str = structures["ext-sub"]
        self.__id: str = TimedSession._session_id_(self.__service_url, self.__tenant_id, self.__external_user_id)

    @staticmethod
    def _session_id_(service_url: str, tenant_id: str, external_user_id: str):
        """
        Create a session id.

        Parameters
        ----------
        service_url: str
            Service url.
        tenant_id: str
            Tenant id.
        external_user_id: str
            External user id.

        Returns
        -------
        session_id: str
            Session id.
        """
        unique: str = f"{service_url}{tenant_id}{external_user_id}"
        return hashlib.sha256(unique.encode()).hexdigest()

    @staticmethod
    def extract_session_id(auth_key: str) -> str:
        """
        Extract the session id from the authentication key.
        Parameters
        ----------
        auth_key: str
            Authentication key.

        Returns
        -------
        session_id: str
            Session id.
        """
        structures: Dict[str, Any] = jwt.decode(auth_key, options={"verify_signature": False})
        if "ext-sub" not in structures:
            raise ValueError("Invalid authentication key.")
        service_url: str = structures["iss"]
        tenant_id: str = structures["tenant"]
        external_user_id: str = structures["ext-sub"]
        return TimedSession._session_id_(service_url, tenant_id, external_user_id)

    @property
    def tenant_id(self) -> str:
        """Tenant id."""
        return self.__tenant_id

    @property
    def roles(self) -> str:
        """Roles."""
        return self.__roles

    @property
    def service_url(self) -> str:
        """Service url."""
        return self.__service_url

    @property
    def external_user_id(self) -> str:
        """External user id."""
        return self.__external_user_id

    @property
    def expiration(self) -> datetime:
        """Timestamp when the token expires."""
        return self.__timestamp

    @property
    def auth_token(self) -> str:
        """JWT token for the session encoding the user id."""
        return self.__auth_token

    @auth_token.setter
    def auth_token(self, value: str):
        self.__auth_token = value

    @property
    def id(self) -> str:
        """Session id."""
        return self.__id

    @property
    def expires_in(self) -> float:
        """Seconds until token is expired in seconds."""
        timestamp: datetime = datetime.now(tz=timezone.utc)
        return self.expiration.timestamp() - timestamp.timestamp()

    @property
    def expired(self) -> bool:
        """Is the session expired."""
        return self.expires_in <= 0.0

    @property
    def refreshable(self) -> bool:
        """Is the session refreshable."""
        return False

    def update_session(self, auth_token: str, refresh_token: str):
        raise NotImplementedError

    def __str__(self):
        return f"TimedSession(auth_token={self.auth_token})"


class RefreshableSession(TimedSession):
    """
    RefreshableSession
    ------------------

    Class that extends TimedSession to provide functionality for refreshable session management.

    Detailed description of the class, its purpose, and usage. Allows handling of authentication
    and refresh tokens while ensuring thread-safe updates to the session. This class provides
    property-based access and management for the refresh token state and validation of session
    tokens, ensuring compatibility with user, tenant, and instance details.

    Attributes
    ----------
    auth_token : str
        The authentication token required for session authentication.
    refresh_token : str
        The refresh token used to renew the session.
    """

    def __init__(self, auth_token: str, refresh_token: str):
        super().__init__(auth_token)
        self.__refresh_token: str = refresh_token
        self.__lock: threading.Lock = threading.Lock()

    @property
    def refresh_token(self) -> str:
        """Refresh token for the session."""
        return self.__refresh_token

    @refresh_token.setter
    def refresh_token(self, value: str):
        self.__refresh_token = value

    def update_session(self, auth_token: str, refresh_token: str):
        """
        Refresh the session.
        Parameters
        ----------
        auth_token: str
            The refreshed authentication token.
        refresh_token: str
            The refreshed refresh token.
        """
        with self.__lock:
            structures = jwt.decode(auth_token, options={"verify_signature": False})
            if (
                "tenant" not in structures
                or "roles" not in structures
                or "exp" not in structures
                or "iss" not in structures
                or "ext-sub" not in structures
            ):
                raise ValueError("Invalid authentication token.")
            if (
                self.tenant_id != structures["tenant"]
                or self.external_user_id != structures["ext-sub"]
                or self.service_url != structures["iss"]
            ):
                raise ValueError("The token is from a different user, tenant, or instance.")
            self._auth_token_details_(auth_token)
            self.auth_token = auth_token
            self.refresh_token = refresh_token

    @property
    def refreshable(self) -> bool:
        """Is the session refreshable?"""
        return self.refresh_token is not None

    def __str__(self):
        return f"RefreshableSession(auth_token={self.auth_token}, refresh_token={self.refresh_token})"


class PermanentSession(RefreshableSession):
    """
    PermanentSession
    ----------------

    A session that retains a tenant API key and an external user ID for
    permanent identification and authorization.

    This class extends the RefreshableSession by encapsulating additional
    information such as a unique tenant API key and an external user ID, which
    are immutable properties. It is used to establish and maintain a session
    that requires these parameters alongside authentication and refresh tokens.

    Attributes
    ----------
    tenant_api_key : str
        The API key associated with the tenant for this session.
    external_user_id : str
        The external user identifier for the session.
    """

    def __init__(self, tenant_api_key: str, external_user_id: str, auth_token: str, refresh_token: str):
        super().__init__(auth_token, refresh_token)
        self.__tenant_api_key: str = tenant_api_key
        self.__external_user_id: str = external_user_id

    @property
    def tenant_api_key(self) -> str:
        """Tenant api key."""
        return self.__tenant_api_key

    @property
    def external_user_id(self) -> str:
        """External user id."""
        return self.__external_user_id

    def __str__(self):
        return (
            f"PermanentSession(tenant_api_key={self.tenant_api_key}, external_user_id={self.external_user_id}, "
            f"auth_token={self.auth_token}, refresh_token={self.refresh_token})"
        )


class TokenManager:
    """
    TokenManager
    ------------

    Manages sessions for authentication and authorization.

    The `TokenManager` class provides functionality to handle different types of
    sessions including permanent, refreshable, and timed sessions. It ensures thread-safe
    operations for adding, retrieving, removing, and maintaining sessions. It also
    includes utilities for cleaning up expired sessions.

    Attributes
    ----------
    sessions : Dict[str, Union[TimedSession, RefreshableSession, PermanentSession]]
        A dictionary mapping session ids to their corresponding session objects.
    """

    def __init__(self):
        self.sessions: Dict[str, Union[TimedSession, RefreshableSession, PermanentSession]] = {}
        self.__lock: threading.Lock = threading.Lock()

    def add_session(
        self,
        auth_token: str,
        refresh_token: Optional[str] = None,
        tenant_api_key: Optional[str] = None,
        external_user_id: Optional[str] = None,
    ) -> Union[PermanentSession, RefreshableSession, TimedSession]:
        """
        Add a session.
        Parameters
        ----------
        auth_token: str
            The authentication token.
        refresh_token: Optional[str] [default := None]
            The refresh token.
        tenant_api_key: Optional[str] [default := None]
            The tenant api key.
        external_user_id: Optional[str] [default := None]
            The external user id.

        Returns
        -------
        session: Union[PermanentSession, RefreshableSession, TimedSession]
            The logged-in session.
        """
        with self.__lock:
            if tenant_api_key is not None and external_user_id is not None:
                session = PermanentSession(
                    tenant_api_key=tenant_api_key,
                    external_user_id=external_user_id,
                    auth_token=auth_token,
                    refresh_token=refresh_token,
                )
                # If there is a tenant api key and an external user id, then the session is permanent
            elif refresh_token is not None:
                session = RefreshableSession(auth_token=auth_token, refresh_token=refresh_token)
                # If there is a refresh token, then the session is refreshable
            else:
                session = TimedSession(auth_token=auth_token)
                # If there is no refresh token, then the session is timed
            if session.id in self.sessions:
                existing_type = type(self.sessions[session.id])
                new_type = type(session)
                if existing_type != new_type:
                    logger.warning(
                        f"Session {session.id} already exists. "
                        f"Overwriting with new type of session {new_type.__name__}, "
                        f"before {existing_type.__name__}."
                    )

            self.sessions[session.id] = session
            return session

    def get_session(self, session_id: str) -> Union[RefreshableSession, TimedSession, PermanentSession, None]:
        """
        Get a session by its id.

        Parameters
        ----------
        session_id: str
            Session id.

        Returns
        -------
        session: Union[RefreshableSession, TimedSession, PermanentSession]
            Depending on the session type, the session is returned.
        """
        with self.__lock:
            return self.sessions.get(session_id)

    def remove_session(self, session_id: str):
        """
        Remove a session by its id.

        Parameters
        ----------
        session_id: str
            Session id.
        """
        with self.__lock:
            if session_id in self.sessions:
                del self.sessions[session_id]

    def has_session(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Parameters
        ----------
        session_id: str
            Session id.

        Returns
        -------
        available: bool
            True if the session exists, otherwise False.
        """
        with self.__lock:
            return session_id in self.sessions

    def cleanup_expired_sessions(self) -> int:
        """
        Removes expired sessions from the session store.

        Returns
        -------
        int
            The number of expired sessions removed.
        """
        with self.__lock:
            expired_ids = [sid for sid, session in self.sessions.items() if session.expired and not session.refreshable]
            for sid in expired_ids:
                del self.sessions[sid]
            return len(expired_ids)

    @property
    def session_count(self) -> int:
        """Number of active sessions."""
        with self.__lock:
            return len(self.sessions)
