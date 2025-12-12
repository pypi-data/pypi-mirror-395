# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
from typing import List, Any, Dict, Optional

from knowledge.base.entity import Label
from knowledge.base.language import LocaleCode
from knowledge.base.ontology import OntologyClassReference


class LabelSearchResult:
    """
    LabelSearchResult
    =================
    This is a search result model.

    Properties
    ----------
    score: float
        Score of the search result.
    entity_uri: str
        Unique identifier of the entity.
    label: str
        Label of the search result.
    locale: LocaleCode
        Locale of the search result.
    concept_type: OntologyClassReference
        Concept type of the search result.
    metadata: Dict[str, Any]
        Metadata of the search result.
    """

    def __init__(self, score: float, content_uri: str, metadata: Dict[str, Any], content: str):
        self.__score: float = score
        self.__content_uri: str = content_uri
        self.__metadata: Dict[str, Any] = metadata
        self.__concept_type: OntologyClassReference = OntologyClassReference.parse(
            metadata.get("concept_type", "wacom:core#Topic")
        )
        self.__locale: LocaleCode = LocaleCode(metadata.get("locale", "en_US"))
        if "concept_type" in self.__metadata:
            del self.__metadata["concept_type"]
        if "locale" in self.__metadata:
            del self.__metadata["locale"]
        self.__label: Label = Label(content=content, language_code=self.__locale)

    @property
    def score(self) -> float:
        """Score of the search result."""
        return self.__score

    @property
    def entity_uri(self) -> str:
        """Unique identifier of the entity."""
        return self.__content_uri

    @property
    def locale(self) -> LocaleCode:
        """Locale of the search result."""
        return self.__locale

    @property
    def metadata(self) -> Dict[str, Any]:
        """Metadata of the search result."""
        return self.__metadata

    @property
    def label(self) -> Label:
        """Label of the search result."""
        return self.__label

    @property
    def concept_type(self) -> OntologyClassReference:
        """Concept type of the search result."""
        return self.__concept_type

    def __repr__(self):
        return (
            f"LabelSearchResult(score={self.score}, entity_uri={self.entity_uri}, label={self.label}, "
            f"locale={self.locale}, concept_type={self.concept_type}, metadata={self.metadata})"
        )


class DocumentSearchResult:
    """
    DocumentSearchResult
    ====================
    This is a search result model.

    Properties
    ----------
    score: float
        Score of the search result.
    content_uri: str
        Unique identifier of the entity.
    metadata: Dict[str, Any]
        Metadata of the search result.
    content_chunk: str
        Content chunk of the search result.
    concept_type: OntologyClassReference
        Concept type of the search result.
    locale: LocaleCode
        Locale of the search result.
    """

    def __init__(self, score: float, content_uri: str, metadata: Dict[str, Any], content: str):
        self.__score: float = score
        self.__content_uri: str = content_uri
        self.__content: str = content
        self.__metadata: Dict[str, Any] = metadata
        self.__concept_type: OntologyClassReference = OntologyClassReference.parse(
            metadata.get("concept_type", "wacom:core#Thing")
        )
        self.__locale: LocaleCode = LocaleCode(metadata.get("locale", "en_US"))
        if "concept_type" in self.__metadata:
            del self.__metadata["concept_type"]
        if "locale" in self.__metadata:
            del self.__metadata["locale"]

    @property
    def score(self) -> float:
        """Score of the search result."""
        return self.__score

    @property
    def content_uri(self) -> str:
        """Unique identifier of the content."""
        return self.__content_uri

    @property
    def content_chunk(self) -> str:
        """Chunk of the document."""
        return self.__content

    @property
    def metadata(self) -> Dict[str, Any]:
        """Metadata of the search result."""
        return self.__metadata

    @property
    def concept_type(self) -> OntologyClassReference:
        """Concept type of the search result."""
        return self.__concept_type

    @property
    def locale(self) -> LocaleCode:
        """Locale of the search result."""
        return self.__locale


class PerformanceStats:
    """
    PerformanceStats
    ================
    This is a performance stats model.

    Properties
    ----------
    locale_code: LocaleCode
        Performance for the model with the given locale.
    model_name: str
        Name of the model used for the search.
    top_k: int
        Top-k results requested.
    model_loading_time: float
        Loading time in milliseconds for the embedding model.
    embedding_time: float
        Embedding time in milliseconds for the search query.
    vector_db_response_time: float
        Response time in milliseconds for the vector database.
    """

    def __init__(self, stats: Dict[str, Any]):
        self.__locale: LocaleCode = stats.get("locale")
        self.__model_name: str = stats.get("model-name", "unknown")
        self.__top_k: int = stats.get("top-k", 10)
        self.__loading_time: float = stats.get("loading", 0.0) * 1000
        self.__embedding_time: float = stats.get("embedding", 0.0) * 1000
        self.__vector_db_response_time: float = stats.get("request", 0.0) * 1000
        self.__overall_time: float = stats.get("overall", 0.0) * 1000

    @property
    def locale_code(self) -> LocaleCode:
        """Performance for the model with the given locale."""
        return self.__locale

    @property
    def model_name(self) -> str:
        """Name of the model used for the search."""
        return self.__model_name

    @property
    def top_k(self) -> int:
        """Top-k results requested."""
        return self.__top_k

    @property
    def model_loading_time(self) -> float:
        """Loading time in milliseconds for the embedding model."""
        return self.__loading_time

    @property
    def embedding_time(self) -> float:
        """Embedding time in milliseconds for the search query."""
        return self.__embedding_time

    @property
    def vector_db_response_time(self) -> float:
        """Response time in milliseconds for the vector database."""
        return self.__vector_db_response_time

    @property
    def overall_time(self) -> float:
        """Overall time in milliseconds for the search query."""
        return self.__overall_time

    def __repr__(self):
        return (
            f"PerformanceStats(locale_code={self.locale_code}, model_name={self.model_name}, top_k={self.top_k}, "
            f"model_loading_time={self.model_loading_time}, embedding_time={self.embedding_time}, "
            f"vector_db_response_time={self.vector_db_response_time})"
        )


class DocumentSearchStats(PerformanceStats):
    """
    DocumentSearchStats
    ====================
    This is a performance stats model for document search.

    Properties
    ----------
    locale_code: LocaleCode
        Performance for the model with the given locale.
    model_name: str
        Name of the model used for the search.
    top_k: int
        Top-k results requested.
    model_loading_time: float
        Loading time in milliseconds for the embedding model.
    embedding_time: float
        Embedding time in milliseconds for the search query.
    vector_db_response_time: float
        Response time in milliseconds for the vector database.
    preprocessing_time: float
        Preprocessing time in milliseconds for search query.

    """

    def __init__(self, stats: Dict[str, Any]):
        super().__init__(stats)
        self.__preprocessing: float = stats.get("preprocessing", 0.0) * 1000.0

    @property
    def preprocessing_time(self) -> float:
        """Preprocessing time in milliseconds for search query."""
        return self.__preprocessing

    def __repr__(self):
        return (
            f"DocumentSearchStats(locale_code={self.locale_code}, model_name={self.model_name}, "
            f"top_k={self.top_k}, "
            f"model_loading_time={self.model_loading_time}, embedding_time={self.embedding_time}, "
            f"vector_db_response_time={self.vector_db_response_time}, preprocessing_time={self.preprocessing_time})"
        )


class LabelSearchStats(PerformanceStats):
    """
    LabelSearchStats
    ================
    This is a performance stats model for label search.

    Properties
    ----------
    locale_code: LocaleCode
        Performance for the model with the given locale.
    model_name: str
        Name of the model used for the search.
    top_k: int
        Top-k results requested.
    model_loading_time: float
        Loading time in milliseconds for the embedding model.
    embedding_time: float
        Embedding time in milliseconds for the search query.
    vector_db_response_time: float
        Response time in milliseconds for the vector database.
    tokenizer_time: float
        Tokenizer time in milliseconds for search query.
    number_of_tokens: int
        Number of tokens in the search query.
    """

    def __init__(self, stats: Dict[str, Any]):
        super().__init__(stats)
        self.__tokenizer: float = stats.get("tokenizer")
        self.__number_of_tokens: int = stats.get("number-of-tokens")

    @property
    def tokenizer_time(self) -> float:
        """Tokenizer time in milliseconds for search query."""
        return self.__tokenizer

    @property
    def number_of_tokens(self) -> int:
        """Number of tokens in the search query."""
        return self.__number_of_tokens

    def __repr__(self):
        return (
            f"LabelSearchStats(locale_code={self.locale_code}, model_name={self.model_name}, "
            f"top_k={self.top_k}, "
            f"model_loading_time={self.model_loading_time}, embedding_time={self.embedding_time}, "
            f"vector_db_response_time={self.vector_db_response_time}, tokenizer_time={self.tokenizer_time}, "
            f"number_of_tokens={self.number_of_tokens})"
        )


class DocumentSearchResponse:
    """
    DocumentSearchResponse
    ======================
    Response model for semantic search service.

    Properties
    ----------
    results: List[DocumentSearchResult]
        Search results
    max_results: int
        Maximum number of results
    stats: Optional[PerformanceStats]
        Performance stats
    """

    def __init__(
        self, results: List[DocumentSearchResult], max_results: int = 10, stats: Optional[DocumentSearchStats] = None
    ):
        self.__results: List[DocumentSearchResult] = results
        self.__max_results = max_results
        self.__stats: Optional[DocumentSearchStats] = stats

    @property
    def results(self) -> List[DocumentSearchResult]:
        """List of search results."""
        return self.__results

    @property
    def max_results(self) -> int:
        """Maximum number of results."""
        return self.__max_results

    @property
    def stats(self) -> Optional[DocumentSearchStats]:
        """Performance stats."""
        return self.__stats

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DocumentSearchResponse":
        """
        Create a DocumentSearchResponse from a dictionary.
        Parameters
        ----------
        data: Dict[str, Any]
            Dictionary with the response data.

        Returns
        -------
        DocumentSearchResponse
            SegmentedContent search response.
        """
        return DocumentSearchResponse(
            results=[DocumentSearchResult(**result) for result in data["results"]],
            max_results=data["max_results"],
            stats=DocumentSearchStats(data["stats"]) if "stats" in data and data["stats"] else None,
        )


class LabelMatchingResponse:
    """
    SemanticSearchResponse
    ======================
    Response model for semantic search service.

    Properties
    ----------
    results: List[LabelSearchResult]
        Search results
    max_results: int
        Maximum number of results
    stats: Optional[LabelSearchStats]
        Performance stats
    """

    def __init__(
        self, results: List[LabelSearchResult], max_results: int = 10, stats: Optional[LabelSearchStats] = None
    ):
        self.__results = results
        self.__max_results = max_results
        self.__stats: Optional[LabelSearchStats] = stats

    @property
    def results(self) -> List[LabelSearchResult]:
        """List of label search results."""
        return self.__results

    @property
    def max_results(self) -> int:
        """Maximum number of results."""
        return self.__max_results

    @property
    def stats(self) -> Optional[LabelSearchStats]:
        """Performance stats."""
        return self.__stats

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """
        Create a LabelMatchingResponse from a dictionary.
        Parameters
        ----------
        data: Dict[str, Any]
            Dictionary with the response data.

        Returns
        -------
        LabelMatchingResponse
            Label matching response.
        """
        return LabelMatchingResponse(
            results=[LabelSearchResult(**result) for result in data["results"]],
            max_results=data["max_results"],
            stats=LabelSearchStats(data["stats"]) if "stats" in data and data["stats"] else None,
        )


class VectorDBDocument:
    """
    Represents a document stored in a vector database.

    This class is used for handling documents with associated metadata within a vector
    database. It provides properties to access the document's ID, content, URI, and
    metadata, making it suitable for systems that manage search or retrieval of
    semantic data in vectorized form.

    Attributes
    ----------
    id : str
        A unique identifier for the document.
    content : str
        The textual content of the document.
    uri : str
        A URI associated with the document.
    metadata : Dict[str, Any]
        Additional metadata associated with the document.
    """

    def __init__(self, data: Dict[str, Any]):
        self.__id: str = data.get("id", "")
        self.__content: str = data.get("content", "")
        self.__uri: str = data.get("uri", "")
        self.__metadata: Dict[str, Any] = data.get("meta", {})

    @property
    def id(self) -> str:
        """ID of the document."""
        return self.__id

    @property
    def content(self) -> str:
        """Content of the document."""
        return self.__content

    @property
    def uri(self) -> str:
        """URI of the document."""
        return self.__uri

    @property
    def metadata(self) -> Dict[str, Any]:
        """Metadata of the document."""
        return self.__metadata

    def __repr__(self):
        return f"VectorDatabaseDocument(content={self.content}, uri={self.uri}, metadata={self.metadata})"
