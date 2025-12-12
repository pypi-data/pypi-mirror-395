# -*- coding: utf-8 -*-
# Copyright © 2025-present Wacom. All rights reserved.
from datetime import datetime
from typing import List, Optional, Dict, Any
from typing import Literal


class JobStatus:
    """
    JobStatus
    ---------
    Represents the status of a job.

    Parameters
    ----------
    user_id: str
        Identifies the user who started the job.
    tenant_id: str
        Identifies the tenant where the entities are imported.
    internal_job_id: str
        Identifies the internal job ID.
    job_id: str
        Identifies the job ID.
    status: Literal["Pending", "InProgress", "Completed", "Failed", "Retrying"]
        The status of the job. Possible values are:
        - Pending - The job is pending.
        - InProgress - The job is in progress.
        - Completed - The job is completed.
        - Failed - The job has failed.
        - Retrying - The job is being retried.
    processed_entities: int
        The number of processed entities.
    processed_relations: int
        The number of processed relations.
    processed_images: int
        The number of processed images.
    started_at: Optional[datetime]
        The timestamp when the job started.
    finished_at: Optional[datetime]
        The timestamp when the job finished.
    """

    PENDING: str = "Pending"
    """The job is pending. It has not started yet, as another job is in progress."""
    IN_PROGRESS: str = "InProgress"
    """The job is in progress. It has started but not yet completed."""
    COMPLETED: str = "Completed"
    """The job is completed."""
    FAILED: str = "Failed"
    """The job has failed."""
    RETRYING: str = "Retrying"
    """The job is being retried."""

    def __init__(
        self,
        user_id: str,
        tenant_id: str,
        internal_job_id: str,
        job_id: str,
        status: Literal["Pending", "InProgress", "Completed", "Failed", "Retrying"],
        processed_entities: int = 0,
        processed_relations: int = 0,
        processed_images: int = 0,
        started_at: Optional[datetime] = None,
        finished_at: Optional[datetime] = None,
        failures: int = 0,
    ):
        self._userId: str = user_id
        self._tenantId: str = tenant_id
        self._internalJobId: str = internal_job_id
        self._jobId: str = job_id
        self._status: Literal["Pending", "InProgress", "Completed", "Failed", "Retrying"] = status
        self._processed_entities: int = processed_entities
        self._processed_relations: int = processed_relations
        self._processed_images: int = processed_images
        self._started_at: Optional[datetime] = started_at
        self._finished_at: Optional[datetime] = finished_at
        self._failures: int = failures

    @property
    def user_id(self) -> str:
        """
        Identifies the user who started the job.
        """
        return self._userId

    @property
    def tenant_id(self) -> str:
        """
        Identifies the tenant where the entities are imported.
        """
        return self._tenantId

    @property
    def internal_job_id(self) -> str:
        """
        Identifies the internal job ID.
        """
        return self._internalJobId

    @property
    def job_id(self) -> str:
        """
        Identifies the job ID.
        """
        return self._jobId

    @property
    def status(self) -> Literal["Pending", "InProgress", "Completed", "Failed", "Retrying"]:
        """
        The status of the job. Possible values are:
        - Pending - The job is pending.
        - InProgress - The job is in progress.
        - Completed - The job is completed.
        - Failed - The job has failed.
        - Retrying - The job is being retried.
        """
        return self._status

    @property
    def processed_entities(self) -> int:
        """
        The number of processed entities.
        """
        return self._processed_entities

    @property
    def processed_relations(self) -> int:
        """
        The number of processed relations.
        """
        return self._processed_relations

    @property
    def processed_images(self) -> int:
        """
        The number of processed images.
        """
        return self._processed_images

    @property
    def started_at(self) -> Optional[datetime]:
        """
        The timestamp when the job started.
        """
        return self._started_at

    @property
    def finished_at(self) -> Optional[datetime]:
        """
        The timestamp when the job finished.
        """
        return self._finished_at

    @property
    def failures(self) -> int:
        """
        The number of failures encountered during the job.
        """
        return self._failures

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobStatus":
        """
        Create a JobStatus instance from a dictionary.
        Parameters
        ----------
        data: Dict[str, Any]
            Response data from the API.

        Returns
        -------
        instance: JobStatus
            Instance of JobStatus.
        """
        return cls(
            user_id=data.get("userId"),
            tenant_id=data.get("tenantId"),
            internal_job_id=data.get("internalJobId"),
            job_id=data.get("jobId"),
            status=data.get("status"),
            processed_entities=data.get("processed", {}).get("entities", 0),
            processed_relations=data.get("processed", {}).get("relations", 0),
            processed_images=data.get("processed", {}).get("images", 0),
            started_at=datetime.fromisoformat(data.get("startedAt", datetime.now().isoformat())),
            finished_at=datetime.fromisoformat(data.get("finishedAt", datetime.now().isoformat())),
            failures=data.get("failures", 0),
        )

    def __repr__(self):
        return (
            f"JobStatus(userId={self.user_id}, tenantId={self.tenant_id}, internalJobId={self.internal_job_id}, "
            f"jobId={self.job_id}, status={self.status}, failures={self.failures}, "
            f"processed_entities={self.processed_entities}, "
            f"processed_relations={self.processed_relations}, processed_images={self.processed_images}, "
            f"started_at={self.started_at}, finished_at={self.finished_at})"
        )


class ErrorDetail:
    """
    ErrorDetail
    ----------
    Represents an error detail.

    Parameters
    ----------
    severity: str
        The severity of the error.
    reason: str
        The reason for the error.
    position_offset: int
        The position offset of the error in the file.
    timestamp: str
        The timestamp of the error in ISO 8601 format.
    """

    def __init__(self, severity: str, reason: str, position_offset: int, timestamp: str):
        self._severity = severity
        self._reason = reason
        self._position_offset = position_offset
        self._timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    @property
    def severity(self) -> str:
        """The severity of the error."""
        return self._severity

    @property
    def reason(self) -> str:
        """The reason for the error."""
        return self._reason

    @property
    def position_offset(self) -> int:
        """The position offset of the error in the file."""
        return self._position_offset

    @property
    def timestamp(self) -> datetime:
        """The timestamp of the error in ISO 8601 format."""
        return self._timestamp


class ErrorLogEntry:
    """
    ErrorLogEntry
    -------------
    Represents an entry in the error log.

    """

    def __init__(self, source_reference_id: Optional[str], errors: List[ErrorDetail]):
        self._source_reference_id = source_reference_id
        self._errors = errors

    @property
    def source_reference_id(self) -> Optional[str]:
        """The source reference ID."""
        return self._source_reference_id

    @property
    def errors(self) -> List[ErrorDetail]:
        """The list of errors."""
        return self._errors


class ErrorLogResponse:
    """
    ErrorLogResponse
    ----------------
    Represents the response for error log.
    """

    def __init__(self, next_page_id: str, error_log: List[ErrorLogEntry]):
        self._next_page_id = next_page_id
        self._error_log = error_log

    @property
    def next_page_id(self) -> str:
        """The ID of the next page."""
        return self._next_page_id

    @property
    def error_log(self) -> List[ErrorLogEntry]:
        """The list of error log entries."""
        return self._error_log

    @classmethod
    def from_dict(cls, param: Dict[str, Any]) -> "ErrorLogResponse":
        """
        Create an ErrorLogResponse instance from a dictionary.
        Parameters
        ----------
        param: Dict[str, Any]
            Response data from the API.

        Returns
        -------
        instance: ErrorLogResponse
            Instance of ErrorLogResponse.
        """
        error_log_entries = []
        for entry in param.get("errorLog", []):
            errors = [
                ErrorDetail(
                    severity=e["severity"],
                    reason=e["reason"],
                    position_offset=e["positionOffset"],
                    timestamp=e["timestamp"],
                )
                for e in entry.get("errors", [])
            ]
            error_log_entries.append(ErrorLogEntry(source_reference_id=entry.get("sourceReferenceId"), errors=errors))

        return ErrorLogResponse(next_page_id=param["nextPageId"], error_log=error_log_entries)


class NewEntityUrisResponse:
    """
    NewEntityUrisResponse
    -------------------
    Represents the response for new entities.

    Parameters
    ----------
    new_entities_uris: Dict[str, str]
        The mapping of entity IDs to URIs (ref_id -> uri).
    next_page_id: Optional[str]
        Next page ID for pagination.
    """

    def __init__(self, new_entities_uris: List[Dict[str, str]], next_page_id: Optional[str]):
        self._new_entities_uris: Dict[str, str] = {entry["ref_id"]: entry["uri"] for entry in new_entities_uris}
        self._next_page_id: Optional[str] = next_page_id

    @property
    def new_entities_uris(self) -> Dict[str, str]:
        """The mapping of entity IDs to URIs."""
        return self._new_entities_uris

    @property
    def next_page_id(self) -> Optional[str]:
        """The ID of the next page."""
        return self._next_page_id

    @classmethod
    def from_dict(cls, param: Dict[str, Any]) -> "NewEntityUrisResponse":
        """
        Create a NewEntityUrisResponse instance from a dictionary.
        Parameters
        ----------
        param: Dict[str, Any]
            Response data from the API.

        Returns
        -------
        instance: NewEntityUrisResponse
            Instance of NewEntityUrisResponse.
        """
        return cls(new_entities_uris=param["uris"], next_page_id=param.get("nextPage"))
