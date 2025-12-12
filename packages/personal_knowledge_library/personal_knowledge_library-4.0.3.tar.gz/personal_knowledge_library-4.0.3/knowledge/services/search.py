# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
from typing import Dict, Any, Optional, List, Literal

from requests import Response

from knowledge.base.language import LocaleCode
from knowledge.base.queue import QueueMonitor, QueueCount, QueueNames
from knowledge.base.search import DocumentSearchResponse, LabelMatchingResponse, VectorDBDocument
from knowledge.services import (
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_RETRIES,
    DEFAULT_BACKOFF_FACTOR,
)
from knowledge.services.base import WacomServiceAPIClient, handle_error


class SemanticSearchClient(WacomServiceAPIClient):
    """
    Semantic Search Client
    ======================
    Client for searching semantically similar documents and labels.

    Parameters
    ----------
    service_url: str
        Service URL for the client.
    service_endpoint: str (Default:= 'vector/v1')
        Service endpoint for the client.
    """

    def __init__(
        self,
        service_url: str,
        application_name: str = "Semantic Search Client",
        base_auth_url: Optional[str] = None,
        service_endpoint: str = "vector/api/v1",
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

    def retrieve_documents_chunks(
        self,
        locale: LocaleCode,
        uri: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> List[VectorDBDocument]:
        """
        Retrieve document chunks from the vector index. The service is automatically chunking the document into
        smaller parts. The chunks are returned as a list of dictionaries, with metadata and content.

        Parameters
        ----------
        locale: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        uri: str
            URI of the document
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.
        Returns
        -------
        document: List[VectorDBDocument]:
            List of document chunks with metadata and content related to the document.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}documents/"
        response = self.request_session.get(
            url,
            params={"locale": locale, "uri": uri},
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            return [VectorDBDocument(elem) for elem in response.json()]
        raise handle_error("Failed to retrieve the document.", response, parameters={"locale": locale, "uri": uri})

    def retrieve_labels(
        self,
        locale: LocaleCode,
        uri: str,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> List[VectorDBDocument]:
        """
        Retrieve labels from the vector index.

        Parameters
        ----------
        locale: LocaleCode
            Locale
        uri: str
            URI of the document
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.

        Returns
        -------
        document: List[VectorDBDocument]
            List of labels with metadata and content related to the entity with uri.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}labels/"
        response: Response = self.request_session.get(
            url,
            params={"uri": uri, "locale": locale},
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            return [VectorDBDocument(elem) for elem in response.json()]
        raise handle_error("Failed to retrieve the labels.", response, parameters={"locale": locale, "uri": uri})

    def count_documents(
        self,
        locale: LocaleCode,
        concept_type: Optional[str] = None,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> int:
        """
        Count all documents for a tenant.

        Parameters
        ----------
        locale: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        concept_type: Optional[str] (Default:= None)
            Concept type.
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.

        Returns
        -------
        number_of_docs: int
            Number of documents.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}documents/count/"
        params: Dict[str, Any] = {"locale": locale}
        if concept_type:
            params["concept_type"] = concept_type
        response = self.request_session.get(
            url,
            params=params,
            overwrite_auth_token=auth_key,
            timeout=timeout,
        )
        if response.ok:
            return response.json().get("count", 0)
        raise handle_error("Counting documents failed.", response, parameters={"locale": locale})

    def count_documents_filter(
        self,
        locale: LocaleCode,
        filters: Dict[str, Any],
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> int:
        """
        Count all documents for a tenant with filters.

        Parameters
        ----------
        locale: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        filters: Dict[str, Any]
            Filters for the search
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.

        Returns
        -------
        number_of_docs: int
            Number of documents.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}documents/count/filter/"
        response: Response = self.request_session.post(
            url, json={"locale": locale, "filter": filters}, timeout=timeout, overwrite_auth_token=auth_key
        )
        if response.ok:
            return response.json().get("count", 0)
        raise handle_error("Counting documents failed.", response, parameters={"locale": locale, "filter": filters})

    def count_labels(
        self,
        locale: LocaleCode,
        concept_type: Optional[str] = None,
        auth_key: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> int:
        """
        Count all labels entries for a tenant.

        Parameters
        ----------
        locale: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        concept_type: Optional[str] (Default:= None)
            Concept type.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.
        auth_key: Optional[str] (Default:= None)
            If an auth key is provided, it will be used for the request.
        Returns
        -------
        count: int
            Number of words.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}labels/count/"
        params: Dict[str, Any] = {"locale": locale}
        if concept_type:
            params["concept_type"] = concept_type
        response = self.request_session.get(
            url,
            params=params,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            return response.json().get("count", 0)
        raise handle_error("Counting labels failed.", response, parameters={"locale": locale})

    def count_labels_filter(
        self,
        locale: LocaleCode,
        filters: Dict[str, Any],
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> int:
        """
        Count all labels for a tenant with filters.

        Parameters
        ----------
        locale: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        filters: Dict[str, Any]
            Filters for the search
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.
        Returns
        -------
        number_of_docs: int
            Number of labels.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}labels/count/filter/"
        response: Response = self.request_session.post(
            url,
            json={"locale": locale, "filter": filters},
            overwrite_auth_token=auth_key,
            timeout=timeout,
        )
        if response.ok:
            return response.json().get("count", 0)
        raise handle_error("Counting labels failed.", response, parameters={"locale": locale, "filter": filters})

    def document_search(
        self,
        query: str,
        locale: LocaleCode,
        filters: Optional[Dict[str, Any]] = None,
        max_results: int = 10,
        filter_mode: Optional[Literal["AND", "OR"]] = None,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> DocumentSearchResponse:
        """
        Async Semantic search.

        Parameters
        ----------
        query: str
            Query text for the search
        locale: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        filters: Optional[Dict[str, Any]] = None
            Filters for the search
        max_results: int
            Maximum number of results
        filter_mode: Optional[Literal["AND", "OR"]] = None
            Filter mode for the search. If None is provided, the default is "AND".
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.
        Returns
        -------
        search_results: DocumentSearchResponse
            Search results response.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}documents/search/"
        params: Dict[str, Any] = {
            "query": query,
            "metadata": filters if filters else {},
            "locale": locale,
            "max_results": max_results,
        }
        if filter_mode:
            params["filter_mode"] = filter_mode
        response: Response = self.request_session.post(
            url,
            json=params,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            response_dict: Dict[str, Any] = response.json()
            return DocumentSearchResponse.from_dict(response_dict)
        raise handle_error("Semantic Search failed.", response, parameters=params)

    def labels_search(
        self,
        query: str,
        locale: LocaleCode,
        filters: Optional[Dict[str, Any]] = None,
        filter_mode: Optional[Literal["AND", "OR"]] = None,
        max_results: int = 10,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> LabelMatchingResponse:
        """
        Async search for semantically similar labels.

        Parameters
        ----------
        query: str
            Query text for the search
        locale: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., en_US.
        filters: Optional[Dict[str, Any]] = None
            Filters for the search
        max_results: int
            Maximum number of results
        filter_mode: Optional[Literal["AND", "OR"]] = None
            Filter mode for the search. If None is provided, the default is "AND".
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        timeout: int (Default:= DEFAULT_TIMEOUT)
            Timeout for the request in seconds.

        Returns
        -------
        list_entities: Dict[str, Any]
            Search results response.
        """
        url: str = f"{self.service_base_url}labels/match/"
        params: Dict[str, Any] = {
            "query": query,
            "metadata": filters if filters else {},
            "locale": locale,
            "max_results": max_results,
        }
        if filter_mode:
            params["filter_mode"] = filter_mode
        response = self.request_session.post(
            url,
            json=params,
            timeout=timeout,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            response_dict: Dict[str, Any] = response.json()
            return LabelMatchingResponse.from_dict(response_dict)
        raise handle_error("Label fuzzy matching failed.", response, parameters=params)

    def list_queue_names(self, auth_key: Optional[str] = None) -> QueueNames:
        """
        List all available queues in the semantic search service.

        Parameters
        ----------
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.

        Returns
        -------
        queues: QueueNames
            List of queue names.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}queues/names/"
        response = self.request_session.get(
            url,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            queues: Dict[str, List[str]] = response.json()
            return QueueNames.parse_json(queues)
        raise handle_error(
            "Failed to list queues.",
            response,
        )

    def list_queues(self, auth_key: Optional[str] = None) -> List[QueueMonitor]:
        """

        Parameters
        ----------
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.

        Returns
        -------
        queues: List[QueueMonitor]
            List of queues.

        Raises
        ------
        WacomServiceException
            If the request fails.
        """
        url: str = f"{self.service_base_url}queues/all/"
        response = self.request_session.get(
            url,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            queues: List[Dict[str, Any]] = response.json()
            return [QueueMonitor.parse_json(queue) for queue in queues]
        raise handle_error(
            "Failed to list queues.",
            response,
        )

    def queue_is_empty(self, queue_name: str, auth_key: Optional[str] = None) -> bool:
        """
        Checks if a given queue is empty.

        This asynchronous method checks whether the specified queue exists and if it is
        empty by interacting with a remote service. It uses an authorization key for
        authentication, and if not provided, retrieves it using a helper method.

        Parameters
        ----------
        queue_name : str
            The name of the queue to check.
        auth_key : Optional[str], optional
            Authorization key used for authenticating with the service. Defaults
            to None, in which case the method will fetch an appropriate token.

        Returns
        -------
        bool
            True if the specified queue is empty, False otherwise.
        """
        url: str = f"{self.service_base_url}queues/empty/"
        params: Dict[str, str] = {"queue_name": queue_name}
        response = self.request_session.get(
            url,
            params=params,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            is_empty: bool = response.json()
            return is_empty
        raise handle_error("Failed to check if the queue is empty.", response)

    def queue_size(self, queue_name: str, auth_key: Optional[str] = None) -> QueueCount:
        """
        Gets the size of a specified queue by making an asynchronous request to the service's
        queue management endpoint. The method interacts with a remote API, utilizing prepared
        headers and query parameters, and parses the returned data into the appropriate
        response structure upon a successful response.

        Parameters
        ----------
        queue_name : str
            The name of the queue whose size is being retrieved.
        auth_key : Optional[str], optional
            An optional authentication key to overwrite the default one when preparing headers.

        Returns
        -------
        QueueCount
            The parsed response encapsulating the size and additional metadata of the specified
            queue.

        Raises
        ------
        Exception
            If the API request fails, an error is raised with the relevant information.
        """
        url: str = f"{self.service_base_url}queues/count/"
        params: Dict[str, str] = {"queue_name": queue_name}
        response = self.request_session.get(
            url,
            params=params,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            response_structure: Dict[str, Any] = response.json()
            return QueueCount.parse_json(response_structure)
        raise handle_error("Failed to get the queue size.", response)

    def queue_monitor_information(self, queue_name: str, auth_key: Optional[str] = None) -> QueueMonitor:
        """
        Gets the monitoring information for a specific queue.

        Parameters
        ----------
        queue_name : str
            The name of the queue for which monitoring information is requested.
        auth_key : Optional[str], optional
            An optional authentication key to be used for the request. If not provided,
            an internal token will be fetched and used.

        Returns
        -------
        QueueMonitor
            A parsed representation of the queue monitoring information.

        Raises
        ------
        Exception
            Raised if the request fails or if there is an issue with fetching the
            monitoring data. Details of the failure are included.
        """
        url: str = f"{self.service_base_url}queues/"
        params: Dict[str, str] = {"queue_name": queue_name}
        response = self.request_session.get(
            url,
            params=params,
            overwrite_auth_token=auth_key,
        )
        if response.ok:
            response_structure: Dict[str, Any] = response.json()
            return QueueMonitor.parse_json(response_structure)
        raise handle_error("Failed to get the queue monitor information.", response)
