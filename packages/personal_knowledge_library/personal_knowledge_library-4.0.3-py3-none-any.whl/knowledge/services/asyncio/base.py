# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
import asyncio
import json
import socket
import ssl
from datetime import datetime
from typing import Any, Tuple, Dict, Optional, Union, Literal

import aiohttp
import certifi
import orjson
from aiohttp import ClientTimeout
from cachetools import TTLCache

from knowledge import __version__, logger
from knowledge.services import (
    USER_AGENT_HEADER_FLAG,
    TENANT_API_KEY,
    CONTENT_TYPE_HEADER_FLAG,
    REFRESH_TOKEN_TAG,
    DEFAULT_TIMEOUT,
    EXPIRATION_DATE_TAG,
    ACCESS_TOKEN_TAG,
    APPLICATION_JSON_HEADER,
    EXTERNAL_USER_ID,
    AUTHORIZATION_HEADER_FLAG,
)
from knowledge.services.base import WacomServiceException, RESTAPIClient
from knowledge.services.session import TokenManager, PermanentSession, RefreshableSession, TimedSession

# A cache for storing DNS resolutions
dns_cache: TTLCache = TTLCache(maxsize=100, ttl=300)  # Adjust size and ttl as needed
HTTPMethodFunction = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


async def cached_getaddrinfo(host: str, *args, **kwargs) -> Any:
    """
    Cached address information.

    Parameters
    ----------
    host: str
        Hostname
    args: Any
        Additional arguments
    kwargs: Any
        Additional keyword arguments

    Returns
    -------
    addr_info: Any
        Address information
    """
    if host in dns_cache:
        return dns_cache[host]
    try:
        addr_info = await asyncio.get_running_loop().getaddrinfo(host, port=None, *args, **kwargs)
        dns_cache[host] = addr_info
        return addr_info
    except (OSError, socket.gaierror) as e:
        logger.warning(f"DNS resolution failed for {host}: {e}")
        raise


class CachedResolver(aiohttp.resolver.AbstractResolver):
    """
    CachedResolver
    ==============
    Cached resolver for aiohttp.
    """

    async def close(self) -> None:
        pass

    async def resolve(self, host: str, port: int = 0, family: int = socket.AF_INET):
        """
        Resolves a hostname to a list of address information. This is an asynchronous
        method that fetches the address details for the given hostname. The result
        includes protocol, host address, port, and family information. The family
        parameter defaults to IPv4.

        Parameters
        ----------
        host : str
            The hostname or IP address to be resolved.
        port : int, optional
            The port number to include in the resolved information. Defaults to 0.
        family : int, optional
            The address family to use for the resolution. Defaults to socket.AF_INET.

        Returns
        -------
        list of dict
            A list of dictionaries containing resolved address information, including
            - `hostname`: The original host input.
            - `host`: The resolved host address.
            - `port`: The port number.
            - `family`: The address family used for resolution.
            - `proto`: Protocol number, set to 0.
            - `flags`: Address information flags, set to socket.AI_NUMERICHOST.
        """
        infos = await cached_getaddrinfo(host)
        return [
            {
                "hostname": host,
                "host": info[4][0],
                "port": port,
                "family": family,
                "proto": 0,
                "flags": socket.AI_NUMERICHOST,
            }
            for info in infos
        ]


class AsyncSession:
    """
    Represents an asynchronous session manager for making HTTP requests.

    The `AsyncSession` class is designed to handle and manage asynchronous HTTP
    requests using the `aiohttp` library. It manages session creation,
    handles headers, manages authentication, and supports multiple HTTP methods
    (GET, POST, PUT, DELETE, PATCH). It is intended to simplify structured
    HTTP requests in an asynchronous context.

    Parameters
    ----------
    client: AsyncServiceAPIClient
        The client instance.
    timeout: int
        The default timeout duration in seconds for requests.

    """

    def __init__(
        self,
        client: "AsyncServiceAPIClient",
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self._client = client
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_lock: asyncio.Lock = asyncio.Lock()
        self._timeout: int = timeout

    @staticmethod
    def _async_session(timeout: int) -> aiohttp.ClientSession:
        """
        Returns an asynchronous session.

        Returns
        -------
        session: aiohttp.ClientSession
            Asynchronous session
        """
        client_timeout: ClientTimeout = ClientTimeout(total=timeout)
        ssl_context: ssl.SSLContext = ssl.create_default_context(cafile=certifi.where())
        connector: aiohttp.TCPConnector = aiohttp.TCPConnector(ssl=ssl_context, resolver=CachedResolver())
        return aiohttp.ClientSession(
            json_serialize=lambda x: orjson.dumps(x).decode(), timeout=client_timeout, connector=connector
        )

    async def _create_session(self) -> aiohttp.ClientSession:
        """
        Creates and manages an asynchronous HTTP session for the client instance. This
        method ensures that the session is safely created, retrieved, or recreated if
        necessary, maintaining a proper state to avoid session-related conflicts or
        errors during asynchronous HTTP operations.

        Returns
        -------
        aiohttp.ClientSession
            An instance of aiohttp.ClientSession ready for asynchronous HTTP requests.

        Raises
        ------
        RuntimeError
            Raised if there is an attempt to close an HTTP session while the event loop
            is already closed. This error is safely handled inside the method.
        """
        async with self._session_lock:
            loop = asyncio.get_running_loop()

            # Case 1: no session yet
            if self._session is None:
                self._session = AsyncSession._async_session(self._timeout)
                self._session._loop = loop
                return self._session

            # Case 2: session invalid or closed
            if self._session.closed or self._session._loop is not loop or loop.is_closed():
                try:
                    if not self._session.closed:
                        await self._session.close()
                except RuntimeError:
                    pass  # loop already dead, nothing to do

                self._session = self._async_session(self._timeout)
                self._session._loop = loop
                return self._session

            # Case 3: session is healthy
            return self._session

    async def _prepare_headers(
        self,
        headers: Optional[Dict[str, str]] = None,
        overwrite_auth_token: Optional[str] = None,
        ignore_content_type: bool = False,
        ignore_auth: Optional[bool] = None,
    ) -> Dict[str, str]:
        """
        Prepares and returns a dictionary of headers for an HTTP request, validating and
        adding required headers based on the provided options.

        Parameters
        ----------
        headers : Optional[Dict[str, str]]
            A dictionary containing initial headers to be included in the request. If not
            provided, an empty dictionary will be used.
        overwrite_auth_token : Optional[str]
            A token to overwrite the default authorization token for the request. If not
            provided, the client will use the default authentication mechanism.
        ignore_content_type : bool
            A flag to indicate whether the `Content-Type` header should be ignored. Defaults
            to False, which ensures the `Content-Type` is set to the application's default.
        ignore_auth : Optional[bool]
            A flag to indicate whether authentication headers should be omitted from the
            prepared headers. Defaults to None, implying authentication will be added.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the finalized headers for the HTTP request.
        """
        request_headers: Dict[str, Any] = headers.copy() if headers else {}
        if USER_AGENT_HEADER_FLAG not in request_headers:
            request_headers[USER_AGENT_HEADER_FLAG] = self._client.user_agent
        if not ignore_content_type:
            if CONTENT_TYPE_HEADER_FLAG not in request_headers:
                request_headers[CONTENT_TYPE_HEADER_FLAG] = APPLICATION_JSON_HEADER
        if not ignore_auth:
            if overwrite_auth_token is None:
                auth_token, _ = await self._client.handle_token()
                request_headers[AUTHORIZATION_HEADER_FLAG] = f"Bearer {auth_token}"
            else:
                request_headers[AUTHORIZATION_HEADER_FLAG] = f"Bearer {overwrite_auth_token}"
        return request_headers

    async def request(
        self,
        method: HTTPMethodFunction,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """
        Executes an HTTP request using the specified method, URL, headers, and additional options.

        Parameters
        ----------
        method : HTTPMethodFunction
            The HTTP method to execute (e.g., "GET", "POST", "PUT", "DELETE", or "PATCH").
        url : str
            The URL to which the request should be sent.
        headers : Optional[Dict[str, str]]
            Headers to include in the request. Defaults to None.
        kwargs : dict
            Additional arguments to pass to the request method of aiohttp.ClientSession.

        Returns
        -------
        aiohttp.ClientResponse
            The response object resulting from the HTTP request.

        Raises
        ------
        ValueError
            If the specified HTTP method is unsupported.
        """
        request_timeout: int = kwargs.pop("timeout", self._timeout)
        request_headers = await self._prepare_headers(
            headers,
            overwrite_auth_token=kwargs.pop("overwrite_auth_token", None),
            ignore_auth=kwargs.pop("ignore_auth", False),
            ignore_content_type=kwargs.pop("ignore_content_type", False),
        )
        session: aiohttp.ClientSession = await self._create_session()
        # Use provided timeout or fall back to session default
        if method == "GET":
            return await session.get(url=url, headers=request_headers, timeout=request_timeout, **kwargs)
        if method == "POST":
            return await session.post(url=url, headers=request_headers, timeout=request_timeout, **kwargs)
        if method == "PUT":
            return await session.put(url=url, headers=request_headers, timeout=request_timeout, **kwargs)
        if method == "DELETE":
            return await session.delete(url=url, headers=request_headers, timeout=request_timeout, **kwargs)
        if method == "PATCH":
            return await session.patch(url=url, headers=request_headers, timeout=request_timeout, **kwargs)
        raise ValueError(f"Unsupported method: {method}")

    async def get(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        """
        Asynchronously sends an HTTP GET request to the specified URL.

        This method allows sending GET requests with optional additional parameters
        passed through `kwargs`. It leverages the `request` method to handle the
        operation and returns the corresponding response.

        Parameters
        ----------
        url : str
            The target URL for the HTTP GET request.
        **kwargs
            Additional keyword arguments to configure the GET request. These may
            include headers, query parameters, or other request-specific options.

        Returns
        -------
        aiohttp.ClientResponse
            The response object resulting from the GET request, containing status,
            headers, and body data.
        """
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        """
        Sends an asynchronous HTTP POST request to the specified URL with the given parameters.

        This method uses the underlying `request` method to perform the HTTP POST
        operation. Any additional keyword arguments provided will be forwarded
        to the `request` method for customization of the request. Returns the
        response object resulting from the POST operation.

        Parameters
        ----------
        url : str
            The URL to which the POST request will be sent.
        **kwargs
            Arbitrary keyword arguments that will be passed to the `request`
            method, allowing customization of the request (e.g., headers,
            json data, params).

        Returns
        -------
        aiohttp.ClientResponse
            Represents the response object from the POST request.

        """
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        """
        Asynchronously performs an HTTP PUT request.

        The method sends an HTTP PUT request to the specified URL with the given
        arguments. Typically used to update or create data at the target URL.

        Parameters
        ----------
        url : str
            The URL to which the PUT request is sent.
        **kwargs : dict
            Additional request parameters passed to the underlying request method.

        Returns
        -------
        aiohttp.ClientResponse
            The response object returned after the PUT request is completed.
        """
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        """
        Asynchronously performs an HTTP DELETE request.

        This method sends a DELETE request to the specified URL with additional
        optional parameters provided as keyword arguments. It utilizes the
        `request` method internally for executing the DELETE operation.

        Parameters
        ----------
        url : str
            The URL to which the DELETE request should be sent.
        **kwargs
            Optional parameters to include in the DELETE request, such as
            headers, data, or additional request configurations.

        Returns
        -------
        aiohttp.ClientResponse
            The response object resulting from the DELETE request. This
            provides access to the response data, status, and headers.
        """
        return await self.request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        """
        Asynchronously sends a HTTP PATCH request to the specified URL.

        This method is a coroutine that simplifies sending PATCH requests
        using the underlying `request` method. It allows adding additional
        parameters such as headers, data, or query parameters to the request,
        passed via `**kwargs`. The response is returned as an instance of
        `aiohttp.ClientResponse`.

        Parameters
        ----------
        url : str
            The target URL for the HTTP PATCH request.
        **kwargs
            Additional request parameters like headers, data, or query parameters.

        Returns
        -------
        aiohttp.ClientResponse
            The response object resulting from the PATCH request, which provides
            methods for accessing the content, status, and headers of the HTTP
            response.
        """
        return await self.request("PATCH", url, **kwargs)

    async def close(self):
        """
        Closes the existing session asynchronously.

        This method ensures that the session is properly closed and reset to `None`.
        It acquires a session lock to guarantee thread-safe operations.

        Notes
        -----
        It is essential to invoke this method to release system resources
        associated with the session.

        Raises
        ------
        Exception
            If an error occurs during the session closure operation.
        """
        async with self._session_lock:
            if self._session:
                await self._session.close()
                self._session = None
        # Clear DNS cache to prevent memory leaks
        dns_cache.clear()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.wait_for(self.close(), timeout=self._timeout)


async def handle_error(
    message: str,
    response: aiohttp.ClientResponse,
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
    response: aiohttp.ClientResponse
        Response
    parameters: Optional[Dict[str, Any]] (Default:= None)
        Parameters
    payload: Optional[Dict[str, Any]] (Default:= None)
        Payload
    headers: Optional[Dict[str, str]] (Default:= None)
        Headers

    Returns
    -------
    WacomServiceException
        Create exception.
    """
    try:
        response_text: str = await response.text()
    except Exception as _:
        response_text: str = ""
    return WacomServiceException(
        message,
        method=response.method,
        url=response.url.human_repr(),
        params=parameters,
        payload=payload,
        headers=headers,
        status_code=response.status,
        service_response=response_text,
    )


class AsyncServiceAPIClient(RESTAPIClient):
    """
    Async Wacom Service API Client
    ------------------------------
    Abstract class for Wacom service APIs.

    Parameters
    ----------
    service_url: str
        URL of the service
    base_auth_url: Optional[str] (Default:= None)
        Authentication URL for local development
    service_endpoint: str
        Base endpoint for the service
    verify_calls: bool (Default:= True)
        Flag if API calls should be verified.
    timeout: int (Default:= DEFAULT_TIMEOUT)
        Timeout for the request in seconds.
    """

    USER_ENDPOINT: str = "user"
    USER_LOGIN_ENDPOINT: str = f"graph/v1/{USER_ENDPOINT}/login"
    USER_REFRESH_ENDPOINT: str = f"{USER_ENDPOINT}/refresh"

    def __init__(
        self,
        service_url: str,
        application_name: str = "Async Knowledge Client",
        base_auth_url: Optional[str] = None,
        service_endpoint: str = "graph/v1",
        verify_calls: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self._service_endpoint: str = service_endpoint
        self._auth_url: str = base_auth_url if base_auth_url is not None else service_url
        self._application_name: str = application_name
        self._token_manager: TokenManager = TokenManager()
        self._current_session_id: Optional[str] = None
        self._session: Optional[AsyncSession] = None
        self._token_refresh_lock: asyncio.Lock = asyncio.Lock()
        self._session_lock: asyncio.Lock = asyncio.Lock()
        self._timeout: int = timeout
        super().__init__(service_url, verify_calls)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Handles the asynchronous exit of a context manager.

        This method is invoked when exiting the runtime context, particularly for
        closing out active sessions to release resources properly.

        Parameters
        ----------
        exc_type : type or None
            The exception type, if an exception occurred, otherwise None.
        exc_val : BaseException or None
            The exception instance, if an exception occurred, otherwise None.
        exc_tb : TracebackType or None
            The traceback object, if an exception occurred, otherwise None.

        Returns
        -------
        None
        """
        try:
            await asyncio.wait_for(self.close(), timeout=5.0)
        except (asyncio.TimeoutError, RuntimeError) as e:
            # Log but don't raise - event loop might be closing
            if "Event loop is closed" not in str(e):
                logger.warning(f"Cleanup warning: {e}")
        return False

    async def __aenter__(self):
        """
        Handles the operations required when an asynchronous context manager is entered.

        Returns
        -------
        self : object
            The current instance of the class that is being used as an asynchronous
            context manager.
        """
        return self

    async def close(self):
        """
        Closes the asynchronous session if it is open.

        This method ensures that the session is closed in a thread-safe manner. It acquires
        a session lock to prevent concurrent access during the session closure process.
        If the session is already closed, the method will not perform any additional
        operations.
        """
        async with self._session_lock:
            if self._session:
                await self._session.close()

    @property
    def application_name(self) -> str:
        """Application name."""
        return self._application_name

    @property
    def user_agent(self) -> str:
        """User agent."""
        return (
            f"Personal Knowledge Library({self.application_name})/{__version__}"
            f"(+https://github.com/Wacom-Developer/personal-knowledge-library)"
        )

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
        if self._current_session_id is None:
            raise WacomServiceException("No session set. Please login first.")
        session: Union[RefreshableSession, TimedSession, PermanentSession, None] = self._token_manager.get_session(
            self._current_session_id
        )
        if session is None:
            raise WacomServiceException(f"Unknown session id:= {self._current_session_id}. Please login first.")
        return session

    async def use_session(self, session_id: str):
        """Use session.
        Parameters
        ----------
        session_id: str
            Session id
        """
        if self._token_manager.has_session(session_id):
            self._current_session_id = session_id
        else:
            raise WacomServiceException(f"Unknown session id:= {session_id}.")

    async def handle_token(self, force_refresh: bool = False, force_refresh_timeout: float = 120) -> Tuple[str, str]:
        """
        Handles the token and refreshes it if needed.

        Parameters
        ----------
        force_refresh: bool
            Force refresh token
        force_refresh_timeout: float
            Force refresh timeout in seconds
        Returns
        -------
        user_token: str
            The user token
        refresh_token: str
            The refresh token
        """
        if self.current_session is None:
            raise WacomServiceException("Authentication key is not set. Please login first.")

        async with self._token_refresh_lock:
            # Re-check session state after acquiring lock
            if not self.current_session.refreshable and self.current_session.expired:
                raise WacomServiceException(
                    "Authentication key is expired and cannot be refreshed. Please login again."
                )

            if not self.current_session.refreshable and force_refresh:
                raise WacomServiceException("Authentication key is not refreshable. Please login again.")

            # Refresh token if needed
            if self.current_session.refreshable and (
                self.current_session.expires_in < force_refresh_timeout or force_refresh
            ):
                try:
                    auth_key, refresh_token, _ = await self.refresh_token(self.current_session.refresh_token)
                except WacomServiceException as e:
                    if isinstance(self.current_session, PermanentSession):
                        permanent_session: PermanentSession = self.current_session
                        auth_key, refresh_token, _ = await self.request_user_token(
                            permanent_session.tenant_api_key, permanent_session.external_user_id
                        )
                    else:
                        logger.error(f"Error refreshing token: {e}")
                        raise e
                self.current_session.update_session(auth_key, refresh_token)

            return self.current_session.auth_token, self.current_session.refresh_token

    async def asyncio_session(self) -> AsyncSession:
        """
        Returns an asynchronous session.

        Returns
        -------
        session: AsyncSession
            Asynchronous session
        """
        async with self._session_lock:
            if self._session is None:
                self._session = AsyncSession(self, self._timeout)
        return self._session

    async def request_user_token(
        self, tenant_api_key: str, external_id: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Tuple[str, str, datetime]:
        """
        Login as a user by using the tenant key and its external user id.

        Parameters
        ----------
        tenant_api_key: str
            Tenant api key
        external_id: str
            External id.
        timeout: int = DEFAULT_TIMEOUT
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
        headers: Dict[str, str] = {
            USER_AGENT_HEADER_FLAG: self.user_agent,
            TENANT_API_KEY: tenant_api_key,
            CONTENT_TYPE_HEADER_FLAG: APPLICATION_JSON_HEADER,
        }
        payload: dict = {EXTERNAL_USER_ID: external_id}
        session = await self.asyncio_session()  # Await the session

        response = await session.post(
            self.auth_endpoint, data=json.dumps(payload), timeout=timeout, headers=headers, ignore_auth=True
        )

        if response.ok:
            response_token: Dict[str, str] = await response.json(loads=orjson.loads)
            try:
                date_object: datetime = datetime.fromisoformat(response_token[EXPIRATION_DATE_TAG])
            except (TypeError, ValueError) as _:
                date_object: datetime = datetime.now()
                logger.warning(f"Parsing of expiration date failed. {response_token[EXPIRATION_DATE_TAG]}")
        else:
            raise await handle_error("Login failed.", response, payload=payload, headers=headers)
        return response_token["accessToken"], response_token["refreshToken"], date_object

    async def refresh_token(self, refresh_token: str, timeout: int = DEFAULT_TIMEOUT) -> Tuple[str, str, datetime]:
        """
        Refreshing a token.

        Parameters
        ----------
        refresh_token: str
            Refresh token
        timeout: int = DEFAULT_TIMEOUT
            Timeout for the request in seconds.

        Returns
        -------
        auth_key: str
            Authentication key for identifying the user for the service calls.
        refresh_key: str
            Refresh token
        expiration_time: str
            Expiration time

        Raises
        ------
        WacomServiceException
            Exception if the service returns HTTP error code.
        """
        url: str = f"{self.service_base_url}{AsyncServiceAPIClient.USER_REFRESH_ENDPOINT}/"
        headers: Dict[str, str] = {
            USER_AGENT_HEADER_FLAG: self.user_agent,
            CONTENT_TYPE_HEADER_FLAG: "application/json",
        }
        payload: Dict[str, str] = {REFRESH_TOKEN_TAG: refresh_token}
        session = await self.asyncio_session()  # Await the session
        response = await session.post(
            url, headers=headers, json=payload, timeout=timeout, verify_ssl=self.verify_calls, ignore_auth=True
        )
        if response.ok:
            response_token: Dict[str, str] = await response.json()
            timestamp_str_truncated: str = ""
            try:
                timestamp_str_truncated = response_token[EXPIRATION_DATE_TAG]
                date_object: datetime = datetime.fromisoformat(timestamp_str_truncated)
            except (TypeError, ValueError) as _:
                date_object: datetime = datetime.now()
                logger.warning(f"Parsing of expiration date failed. {timestamp_str_truncated}")
            return response_token[ACCESS_TOKEN_TAG], response_token[REFRESH_TOKEN_TAG], date_object
        raise await handle_error("Refresh of token failed.", response, payload=payload, headers=headers)

    async def login(self, tenant_api_key: str, external_user_id: str) -> PermanentSession:
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
        auth_key, refresh_token, _ = await self.request_user_token(tenant_api_key, external_user_id)
        session: PermanentSession = self._token_manager.add_session(
            auth_token=auth_key,
            refresh_token=refresh_token,
            tenant_api_key=tenant_api_key,
            external_user_id=external_user_id,
        )
        self._current_session_id = session.id
        return session

    async def logout(self):
        """
        Logs out the user from the current session.

        This method handles the removal of the current session from the token manager
        and triggers any necessary cleanup operations. If all sessions are terminated,
        it invokes additional resource-closing routines.
        """
        if self._current_session_id:
            self._token_manager.remove_session(self._current_session_id)
            if len(self._token_manager.sessions) == 0:
                await self.close()
        self._current_session_id = None

    async def register_token(
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
        session = self._token_manager.add_session(auth_token=auth_key, refresh_token=refresh_token)
        self._current_session_id = session.id
        if isinstance(session, (RefreshableSession, TimedSession)):
            return session
        raise WacomServiceException(f"Wrong session type:= {type(session)}.")

    @property
    def service_endpoint(self):
        """Service endpoint."""
        return "" if len(self._service_endpoint) == 0 else f"{self._service_endpoint}/"

    @property
    def service_base_url(self):
        """Service endpoint."""
        return f"{self.service_url}/{self.service_endpoint}"

    @property
    def base_auth_url(self):
        """Base authentication URL."""
        return self._auth_url

    @property
    def auth_endpoint(self) -> str:
        """Authentication endpoint."""
        # This is in the graph service REST API
        return f"{self.base_auth_url}/{self.USER_LOGIN_ENDPOINT}"
