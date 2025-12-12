# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import threading
from abc import ABC
from datetime import datetime
from typing import Any, Tuple, Dict, Optional, Union, List

import requests
from requests import Response
from requests.sessions import HTTPAdapter
from urllib3 import Retry

from knowledge import __version__, logger
from knowledge.services import DEFAULT_TIMEOUT, AUTHORIZATION_HEADER_FLAG
from knowledge.services import (
    USER_AGENT_HEADER_FLAG,
    TENANT_API_KEY,
    CONTENT_TYPE_HEADER_FLAG,
    REFRESH_TOKEN_TAG,
    EXPIRATION_DATE_TAG,
    ACCESS_TOKEN_TAG,
    APPLICATION_JSON_HEADER,
    EXTERNAL_USER_ID,
)
from knowledge.services.session import TokenManager, RefreshableSession, TimedSession, PermanentSession

STATUS_FORCE_LIST: List[int] = [502, 503, 504]
DEFAULT_BACKOFF_FACTOR: float = 0.1
DEFAULT_MAX_RETRIES: int = 3


class WacomServiceException(Exception):
    """Exception thrown if Wacom service fails.

    Parameters
    ----------
    message: str
        Error message
    payload: Optional[Dict[str, Any]] (Default:= None)
        Payload
    params: Optional[Dict[str, Any]] (Default:= None)
        Parameters
    method: Optional[str] (Default:= None)
        Method
    url: Optional[str] (Default:= None)
        URL
    service_response: Optional[str] (Default:= None)
        Service response
    status_code: int (Default:= 500)
        Status code
    """

    def __init__(
        self,
        message: str,
        headers: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        method: Optional[str] = None,
        url: Optional[str] = None,
        service_response: Optional[str] = None,
        status_code: int = 500,
    ):
        super().__init__(message)
        self.__status_code: int = status_code
        self.__service_response: Optional[str] = service_response
        self.__message: str = message
        self.__headers: Optional[Dict[str, Any]] = headers
        self.__payload: Optional[Dict[str, Any]] = payload
        self.__params: Optional[Dict[str, Any]] = params
        self.__method: Optional[str] = method
        self.__url: Optional[str] = url

    @property
    def headers(self) -> Optional[Dict[str, Any]]:
        """Headers of the exception."""
        return self.__headers

    @property
    def method(self) -> Optional[str]:
        """Method of the exception."""
        return self.__method

    @property
    def params(self) -> Optional[Dict[str, Any]]:
        """Parameters of the exception."""
        return self.__params

    @property
    def payload(self) -> Optional[Dict[str, Any]]:
        """Payload of the exception."""
        return self.__payload

    @property
    def url(self) -> Optional[str]:
        """URL of the exception."""
        return self.__url

    @property
    def message(self) -> str:
        """Message of the exception."""
        return self.__message

    @property
    def service_response(self) -> Optional[str]:
        """Service response."""
        return self.__service_response

    @property
    def status_code(self) -> int:
        """Status code of the exception."""
        return self.__status_code


class RequestsSession:
    """
    Reusable requests session with automatic token management.

    This session wrapper provides connection pooling, automatic token refresh,
    and proper cleanup of resources.

    Parameters
    ----------
    client: WacomServiceAPIClient
        The API client instance
    pool_connections: int (Default:= 10)
        Number of connection pools to cache
    pool_maxsize: int (Default:= 10)
        Maximum number of connections to save in the pool
    max_retries: int (Default:= 3)
        Maximum number of retries for failed requests
    """

    def __init__(
        self,
        client: "WacomServiceAPIClient",
        pool_connections: int = 10,
        pool_maxsize: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        self._client = client
        self._session: Optional[requests.Session] = None
        self._pool_connections = pool_connections
        self._pool_maxsize = pool_maxsize
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor
        self._lock = threading.Lock()

    @property
    def max_retries(self) -> int:
        """Maximum number of retries for failed requests."""
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int):
        if value != self._max_retries:
            self.close()
            self._max_retries = value

    @property
    def backoff_factor(self) -> float:
        """Backoff factor for failed requests."""
        return self._backoff_factor

    @backoff_factor.setter
    def backoff_factor(self, value: float):
        if value != self._backoff_factor:
            # Close the session to release resources
            self.close()
            self._backoff_factor = value

    @property
    def pool_connections(self) -> int:
        """Number of connection pools to cache."""
        return self._pool_connections

    @pool_connections.setter
    def pool_connections(self, value: int):
        if value != self._pool_connections:
            self.close()
            self._pool_connections = value

    @property
    def pool_maxsize(self) -> int:
        """Maximum number of connections to save in the pool."""
        return self._pool_maxsize

    @pool_maxsize.setter
    def pool_maxsize(self, value: int):
        if value != self._pool_maxsize:
            self.close()
            self._pool_maxsize = value

    def _create_session(self) -> requests.Session:
        """
        Creates and configures an HTTP session for making requests.

        This method creates a thread-safe session instance with retry logic,
        connection pooling, and default headers for HTTP communication. If a
        session already exists, it will return the existing session.

        Returns
        -------
        requests.Session
            A configured requests.Session object to handle HTTP requests with
            retry logic and connection pooling.
        """
        with self._lock:
            if self._session is None:
                self._session = requests.Session()
                retries: Retry = Retry(
                    total=self.max_retries,
                    backoff_factor=self.backoff_factor,
                    status_forcelist=STATUS_FORCE_LIST,
                    raise_on_status=False,
                    respect_retry_after_header=True,
                    allowed_methods=frozenset(["GET", "POST", "PUT", "PATCH", "DELETE"]),
                )

                # Configure connection pooling
                adapter = HTTPAdapter(
                    pool_connections=self.pool_connections,
                    pool_maxsize=self.pool_maxsize,
                    max_retries=retries,
                )

                self._session.mount("https://", adapter)
                self._session.mount("http://", adapter)

                self._session.verify = self._client.verify_calls
        return self._session

    def _prepare_headers(
        self,
        headers: Optional[Dict[str, str]] = None,
        overwrite_auth_token: Optional[str] = None,
        ignore_content_type: bool = False,
        ignore_auth: Optional[bool] = None,
    ) -> Dict[str, str]:
        """Prepare headers with authentication token.

        Parameters
        ----------
        headers: Optional[Dict[str, str]] (Default:= None)
            Request headers.
        overwrite_auth_token: Optional[str] (Default:= None)
            Overwrite the authentication token.
        ignore_content_type: bool (Default:= False)
            Ignore the content type header.
        ignore_auth: Optional[bool] (Default:= None)
            Ignore the authentication token.

        Returns
        -------
        headers: Dict[str, str]
            Complete request headers
        """
        request_headers: Dict[str, Any] = headers.copy() if headers else {}
        if USER_AGENT_HEADER_FLAG not in request_headers:
            request_headers[USER_AGENT_HEADER_FLAG] = self._client.user_agent
        if not ignore_content_type:
            if CONTENT_TYPE_HEADER_FLAG not in request_headers:
                request_headers[CONTENT_TYPE_HEADER_FLAG] = APPLICATION_JSON_HEADER
        if not ignore_auth:
            if overwrite_auth_token is None:
                auth_token, _ = self._client.handle_token()
                request_headers[AUTHORIZATION_HEADER_FLAG] = f"Bearer {auth_token}"
            else:
                request_headers[AUTHORIZATION_HEADER_FLAG] = f"Bearer {overwrite_auth_token}"
        return request_headers

    def request(
        self, method: str, url: str, headers: Optional[Dict[str, str]] = None, timeout: int = DEFAULT_TIMEOUT, **kwargs
    ) -> Response:
        """Execute a request with automatic token handling."""
        request_headers = self._prepare_headers(
            headers,
            overwrite_auth_token=kwargs.pop("overwrite_auth_token", None),
            ignore_auth=kwargs.pop("ignore_auth", False),
            ignore_content_type=kwargs.pop("ignore_content_type", False),
        )
        session = self._create_session()
        return session.request(method=method, url=url, headers=request_headers, timeout=timeout, **kwargs)

    def get(self, url: str, **kwargs) -> Response:
        """
        Execute GET request.

        Parameters
        ----------
        url: str
            URL for the request.
        kwargs: Dict[str, Any] (Default:= {})
            Additional arguments for the request.

        Returns
        -------
        response: Response
            Response from the service.
        """
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        """
        Execute POST request.

        Parameters
        ----------
        url: str
            URL for the request.
        kwargs: Dict[str, Any] (Default:= {})
            Additional arguments for the request.

        Returns
        -------
        response: Response
            Response from the service.
        """
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> Response:
        """
        Execute a PUT request.

        Parameters
        ----------
        url: str
            URL for the request.
        kwargs: Dict[str, Any] (Default:= {})
            Additional arguments for the request.

        Returns
        -------
        response: Response
            Response from the service.
        """
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        """
        Execute a DELETE request.

        Parameters
        ----------
        url: str
            URL for the request.
        kwargs: Dict[str, Any] (Default:= {})
            Additional arguments for the request.

        Returns
        -------
        response: Response
            Response from the service.
        """
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str, **kwargs) -> Response:
        """
        Execute a PATCH request.

        Parameters
        ----------
        url: str
            URL for the request.
        kwargs: Dict[str, Any] (Default:= {})
            Additional arguments for the request.

        Returns
        -------
        response: Response
            Response from the service.
        """
        return self.request("PATCH", url, **kwargs)

    def close(self):
        """
        Close the session and release resources.
        """
        with self._lock:
            if self._session is not None:
                self._session.close()
                self._session = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.close()


def format_exception(exception: WacomServiceException) -> str:
    """
    Formats the exception.

    Parameters
    ----------
    exception: WacomServiceException
        Exception

    Returns
    -------
    formatted_exception: str
        Formatted exception
    """
    return (
        f"WacomServiceException: {exception.message}\n"
        "--------------------------------------------------\n"
        f"URL:= {exception.url},\n"
        f"method:= {exception.method},\n"
        f"parameters:= {exception.params},\n"
        f"payload:= {exception.payload},\n"
        f"headers:= {exception.headers},\n"
        f"status code=: {exception.status_code},\n"
        f"service response:= {exception.service_response}"
    )


def handle_error(
    message: str,
    response: Response,
    parameters: Optional[Dict[str, Any]] = None,
    payload: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> WacomServiceException:
    """
    Handles an error response.

    Parameters
    ----------
    message: str
        Error message
    response: Response
        Response from the service
    parameters: Optional[Dict[str, Any]] (Default:= None)
        Parameters
    payload: Optional[Dict[str, Any]] (Default:= None)
        Payload
    headers: Optional[Dict[str, str]] (Default:= None)
        Headers

    Returns
    -------
    WacomServiceException
        Returns the generated exception.
    """
    return WacomServiceException(
        message,
        url=response.url,
        method=response.request.method,
        params=parameters,
        payload=payload,
        headers=headers,
        status_code=response.status_code,
        service_response=response.text,
    )


class RESTAPIClient(ABC):
    """
    Abstract REST API client
    ------------------------
    REST API client handling the service url.

    Arguments
    ---------
    service_url: str
        Service URL for service
    verify_calls: bool (default:= False)
        Flag if the service calls should be verified
    """

    def __init__(self, service_url: str, verify_calls: bool = False):
        self.__service_url: str = service_url.rstrip("/")
        self.__verify_calls: bool = verify_calls

    @property
    def service_url(self) -> str:
        """Service URL."""
        return self.__service_url

    @property
    def verify_calls(self):
        """Certificate verification activated."""
        return self.__verify_calls

    @verify_calls.setter
    def verify_calls(self, value: bool):
        self.__verify_calls = value


class WacomServiceAPIClient(RESTAPIClient):
    """
    Wacom Service API Client
    ------------------------
    Abstract class for Wacom service APIs.

    Parameters
    ----------
    application_name: str
        Name of the application using the service
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    verify_calls: bool (Default:= True)
        Flag if API calls should be verified.
    """

    USER_ENDPOINT: str = "user"
    USER_LOGIN_ENDPOINT: str = f"graph/v1/{USER_ENDPOINT}/login"
    USER_REFRESH_ENDPOINT: str = f"graph/v1/{USER_ENDPOINT}/refresh"

    def __init__(
        self,
        service_url: str,
        application_name: str = "Knowledge Client",
        base_auth_url: Optional[str] = None,
        service_endpoint: str = "graph/v1",
        verify_calls: bool = True,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ):
        self.__application_name: str = application_name
        self.__service_endpoint: str = service_endpoint
        self.__base_auth_url: str = base_auth_url if base_auth_url is not None else service_url
        self.__token_manager: TokenManager = TokenManager()
        self.__current_session_id: Optional[str] = None
        self.__session: Optional[RequestsSession] = None
        self.__max_retries: int = max_retries
        self.__backoff_factor: float = backoff_factor
        self.__session_lock: threading.Lock = threading.Lock()
        super().__init__(service_url, verify_calls)

    @property
    def request_session(self) -> RequestsSession:
        """Request session."""
        with self.__session_lock:
            if self.__session is None:
                self.__session = RequestsSession(
                    self, max_retries=self.__max_retries, backoff_factor=self.__backoff_factor
                )
        return self.__session

    @property
    def token_manager(self) -> TokenManager:
        """Token manager."""
        return self.__token_manager

    @property
    def auth_endpoint(self) -> str:
        """Authentication endpoint."""
        # This is in the graph service REST API
        return f"{self.base_auth_url}/{self.USER_LOGIN_ENDPOINT}"

    @property
    def current_session(self) -> Union[RefreshableSession, TimedSession, PermanentSession, None]:
        """Current session.

        Returns
        -------
        session: Union[TimedSession, RefreshableSession, PermanentSession]
            Current session

        Raises
        ------
        WacomServiceException
            Exception if no session is available.
        """
        if self.__current_session_id is None:
            raise WacomServiceException("No session set. Please login first.")
        session: Union[RefreshableSession, TimedSession, PermanentSession, None] = self.__token_manager.get_session(
            self.__current_session_id
        )
        if session is None:
            raise WacomServiceException(f"Unknown session id:= {self.__current_session_id}. Please login first.")
        return session

    @property
    def user_agent(self) -> str:
        """User agent."""
        return (
            f"Personal Knowledge Library({self.application_name})/{__version__}"
            f"(+https://github.com/Wacom-Developer/personal-knowledge-library)"
        )

    @property
    def service_endpoint(self):
        """Service endpoint."""
        return "" if len(self.__service_endpoint) == 0 else f"{self.__service_endpoint}/"

    @property
    def service_base_url(self):
        """Service endpoint."""
        return f"{self.service_url}/{self.service_endpoint}"

    @property
    def base_auth_url(self):
        """Base authentication endpoint."""
        return self.__base_auth_url

    @property
    def application_name(self):
        """Application name."""
        return self.__application_name

    def request_user_token(
        self, tenant_api_key: str, external_id: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Tuple[str, str, datetime]:
        """
        Login as a user by using the tenant key and its external user id.

        Parameters
        ----------
        tenant_api_key: str
            Tenant API key
        external_id: str
            External id.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.

        Returns
        -------
        auth_key: str
            Authentication key for identifying the user for the service calls.
        refresh_key: str
            Refresh token
        expiration_time: datatime
            Expiration time

        Raises
        ------
        WacomServiceException
            Exception if the service returns HTTP error code.
        """
        url: str = f"{self.auth_endpoint}"
        headers: dict = {
            USER_AGENT_HEADER_FLAG: self.user_agent,
            TENANT_API_KEY: tenant_api_key,
            CONTENT_TYPE_HEADER_FLAG: APPLICATION_JSON_HEADER,
        }
        payload: dict = {EXTERNAL_USER_ID: external_id}
        response: Response = self.request_session.post(
            url,
            headers=headers,
            json=payload,
            timeout=timeout,
            verify=self.verify_calls,
            allow_redirects=True,
            ignore_auth=True,
        )
        if response.ok:
            try:
                response_token: Dict[str, str] = response.json()
                timestamp_str_truncated: str = ""
                try:
                    timestamp_str_truncated = response_token[EXPIRATION_DATE_TAG]
                    date_object: datetime = datetime.fromisoformat(timestamp_str_truncated)
                except (TypeError, ValueError) as _:
                    date_object: datetime = datetime.now()
                    logger.warning(
                        f"Parsing of expiration date failed. {response_token[EXPIRATION_DATE_TAG]} "
                        f"-> {timestamp_str_truncated}"
                    )
                return response_token["accessToken"], response_token["refreshToken"], date_object
            except Exception as e:
                raise handle_error(f"Parsing of response failed. {e}", response) from e
        raise handle_error("User login failed.", response)

    def login(self, tenant_api_key: str, external_user_id: str) -> PermanentSession:
        """Login as a user by using the tenant id and its external user id.
        Parameters
        ----------
        tenant_api_key: str
            Tenant id
        external_user_id: str
            External user id
        Returns
        -------
        session: PermanentSession
            Session. The session is stored in the token manager, and the client is using the session id for further
            calls.
        """
        auth_key, refresh_token, _ = self.request_user_token(tenant_api_key, external_user_id)
        session: PermanentSession = self.__token_manager.add_session(
            auth_token=auth_key,
            refresh_token=refresh_token,
            tenant_api_key=tenant_api_key,
            external_user_id=external_user_id,
        )
        self.__current_session_id = session.id
        return session

    def logout(self):
        """Logout user."""
        self.__token_manager.remove_session(self.__current_session_id)
        self.__current_session_id = None

    def register_token(
        self, auth_key: str, refresh_token: Optional[str] = None
    ) -> Union[RefreshableSession, TimedSession]:
        """Register a token.
        Parameters
        ----------
        auth_key: str
            Authentication key for identifying the user for the service calls.
        refresh_token: str
            Refresh token

        Returns
        -------
        session: Union[RefreshableSession, TimedSession]
            Session. The session is stored in the token manager, and the client is using the session id for further
            calls.
        """
        session = self.__token_manager.add_session(auth_token=auth_key, refresh_token=refresh_token)
        self.__current_session_id = session.id
        if isinstance(session, (RefreshableSession, TimedSession)):
            return session
        raise WacomServiceException(f"Wrong session type:= {type(session)}.")

    def use_session(self, session_id: str):
        """Use session.
        Parameters
        ----------
        session_id: str
            Session id
        """
        if self.__token_manager.has_session(session_id):
            self.__current_session_id = session_id
        else:
            raise WacomServiceException(f"Unknown session id:= {session_id}.")

    def refresh_token(self, refresh_token: str) -> Tuple[str, str, datetime]:
        """
        Refreshing a token.

        Parameters
        ----------
        refresh_token: str
            Refresh token

        Returns
        -------
        auth_key: str
            Authentication key for identifying the user for the service calls.
        refresh_key: str
            Refresh token
        expiration_time: datetime
            Expiration time

        Raises
        ------
        WacomServiceException
            Exception if the service returns HTTP error code.
        """
        url: str = f"{self.service_base_url}{WacomServiceAPIClient.USER_REFRESH_ENDPOINT}/"
        headers: Dict[str, str] = {
            USER_AGENT_HEADER_FLAG: self.user_agent,
            CONTENT_TYPE_HEADER_FLAG: APPLICATION_JSON_HEADER,
        }
        payload: Dict[str, str] = {REFRESH_TOKEN_TAG: refresh_token}
        response: Response = self.request_session.post(
            url,
            headers=headers,
            json=payload,
            timeout=DEFAULT_TIMEOUT,
            verify=self.verify_calls,
            ignore_auth=True,
        )
        if response.ok:
            response_token: Dict[str, str] = response.json()
            try:
                date_object: datetime = datetime.fromisoformat(response_token[EXPIRATION_DATE_TAG])
            except (TypeError, ValueError) as _:
                date_object: datetime = datetime.now()
                logger.warning(f"Parsing of expiration date failed. {response_token[EXPIRATION_DATE_TAG]}")
            return response_token[ACCESS_TOKEN_TAG], response_token[REFRESH_TOKEN_TAG], date_object
        raise handle_error("Refreshing token failed.", response)

    def handle_token(self, force_refresh: bool = False, force_refresh_timeout: float = 120) -> Tuple[str, str]:
        """
        Handles the token and refreshes it if needed.

        Parameters
        ----------
        force_refresh: bool
            Force refresh token
        force_refresh_timeout: int
            Force refresh timeout
        Returns
        -------
        user_token: str
            The user token
        refresh_token: str
            The refresh token
        """
        session = self.current_session
        expires_in: float = session.expires_in
        # The session is not set
        if session is None:
            raise WacomServiceException("Authentication key is not set. Please login first.")

        # The token expired and is not refreshable
        if not session.refreshable and session.expired:
            raise WacomServiceException("Authentication key is expired and cannot be refreshed. Please login again.")

        # The token is not refreshable and the force refresh flag is set
        if not session.refreshable and force_refresh:
            raise WacomServiceException("Authentication key is not refreshable. Please login again.")

        # Refresh token if needed
        if session.refreshable and (expires_in < force_refresh_timeout or force_refresh):
            try:
                auth_key, refresh_token, _ = self.refresh_token(session.refresh_token)
            except WacomServiceException as e:
                if isinstance(session, PermanentSession):
                    permanent_session: PermanentSession = session
                    auth_key, refresh_token, _ = self.request_user_token(
                        permanent_session.tenant_api_key, permanent_session.external_user_id
                    )
                else:
                    logger.error(f"Error refreshing token: {e}")
                    raise e
            session.update_session(auth_key, refresh_token)
            return auth_key, refresh_token
        return session.auth_token, session.refresh_token
