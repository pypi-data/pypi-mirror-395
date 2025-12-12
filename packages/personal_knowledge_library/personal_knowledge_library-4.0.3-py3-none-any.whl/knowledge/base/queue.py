# -*- coding: utf-8 -*-
# Copyright © 2025 Wacom. All rights reserved.
import json

from typing import List, Optional, Dict, Any


class QueueCount:
    """
    Represents a model for maintaining a queue's name and its count.

    This class is primarily designed to encapsulate the queue name and the
    count of items or occurrences associated with it. It can be utilized
    in various queue-related workflows or systems where such data is required.

    Attributes
    ----------
    queue_name : str
        The name of the queue being represented.
    count : int
        The count of items or occurrences associated with the queue.
    """

    def __init__(self, queue_name: str, count: int):
        self._queue_name = queue_name
        self._count = count

    @property
    def queue_name(self) -> str:
        """The name of the queue."""
        return self._queue_name

    @property
    def count(self) -> int:
        """The count of items or occurrences associated with the queue."""
        return self._count

    @classmethod
    def parse_json(cls, data: Dict[str, Any]) -> "QueueCount":
        """Parse a JSON string and return a QueueCount instance.

        Parameters
        ----------
        data: Dict[str, Any]
            Dictionary containing the queue name and count.

        Returns
        -------
        result: QueueCount
            An instance of QueueCount.
        """
        return cls(queue_name=data["queue_name"], count=data["count"])


class QueueNames:
    """Represents a model for handling queue names.

    This class provides a structure to store and manage names associated with
    queues. It can be useful in systems requiring organization or representation
    of multiple queues. This model ensures type safety and consistency.

    Attributes
    ----------
    names : List[str]
        List of names representing different queues.
    """

    def __init__(self, names: List[str]):
        self._names = names

    @property
    def names(self) -> List[str]:
        """List of names representing different queues."""
        return self._names

    @classmethod
    def parse_json(cls, data: Dict[str, Any]) -> "QueueNames":
        """Parse a JSON string and return a QueueNames instance.

        Parameters
        ----------
        data: Dict[str, Any]
            Dictionary containing the queue names.
        """
        return cls(names=data["names"])


class MessageRate:
    """
    Represents the rate at which messages are sent or processed.

    This class models a single attribute that tracks the speed or frequency
    of messaging events, typically measured as a float. It can be used in
    applications or systems where monitoring, regulating, or analyzing
    message throughput is required.

    Attributes
    ----------
    rate : float
        The rate at which messages are sent or processed.
    """

    def __init__(self, rate: float):
        self._rate = rate

    @property
    def rate(self) -> float:
        """The rate at which messages are sent or processed."""
        return self._rate

    @classmethod
    def parse_json(cls, json_str: str) -> "MessageRate":
        """Parse a JSON string and return a MessageRate instance."""
        data = json.loads(json_str)
        return cls(rate=data["rate"])


class MessageStats:
    """
    Represents statistics related to message publishing, delivery, and acknowledgments.

    This class is used to store statistics about messages such as their publish count,
    delivery count, acknowledgment count, and the corresponding details about rates.
    It serves as a structured model for handling message statistics data.

    Attributes
    ----------
    publish : Optional[int]
        The count of published messages.
    publish_details : Optional[MessageRate]
        Detailed rate information related to message publishing.
    deliver : Optional[int]
        The count of delivered messages.
    deliver_details : Optional[MessageRate]
        Detailed rate information related to message delivery.
    ack : Optional[int]
        The count of acknowledged messages.
    ack_details : Optional[MessageRate]
        Detailed rate information related to message acknowledgments.
    """

    def __init__(
        self,
        publish: Optional[int] = None,
        publish_details: Optional[MessageRate] = None,
        deliver: Optional[int] = None,
        deliver_details: Optional[MessageRate] = None,
        ack: Optional[int] = None,
        ack_details: Optional[MessageRate] = None,
    ):
        self._publish = publish
        self._publish_details = publish_details
        self._deliver = deliver
        self._deliver_details = deliver_details
        self._ack = ack
        self._ack_details = ack_details

    @property
    def publish(self) -> Optional[int]:
        """The count of published messages."""
        return self._publish

    @property
    def publish_details(self) -> Optional[MessageRate]:
        """Detailed rate information related to message publishing."""
        return self._publish_details

    @property
    def deliver(self) -> Optional[int]:
        """The count of delivered messages."""
        return self._deliver

    @property
    def deliver_details(self) -> Optional[MessageRate]:
        """Detailed rate information related to message delivery."""
        return self._deliver_details

    @property
    def ack(self) -> Optional[int]:
        """The count of acknowledged messages."""
        return self._ack

    @property
    def ack_details(self) -> Optional[MessageRate]:
        """Detailed rate information related to message acknowledgments."""
        return self._ack_details

    @classmethod
    def parse_json(cls, json_str: str) -> "MessageStats":
        """Parse a JSON string and return a MessageStats instance."""
        data = json.loads(json_str)
        return cls(
            publish=data.get("publish"),
            publish_details=MessageRate(**data["publish_details"]) if data.get("publish_details") else None,
            deliver=data.get("deliver"),
            deliver_details=MessageRate(**data["deliver_details"]) if data.get("deliver_details") else None,
            ack=data.get("ack"),
            ack_details=MessageRate(**data["ack_details"]) if data.get("ack_details") else None,
        )


class QueueMonitor:
    """
    Represents a monitor for a queue in a message broker.

    This class is used to monitor and manage the state and statistics of a
    message queue. It provides details such as the name of the queue,
    virtual host, current state, message-related statistics, and resource
    usage. It can be integrated into monitoring or operational tools to
    track queue performance and behavior.

    Attributes
    ----------
    name : str
        Name of the queue being monitored.
    vhost : str
        Name of the virtual host to which the queue belongs.
    state : str
        Current state of the queue (e.g., running, idle).
    messages : int
        Total number of messages in the queue.
    messages_ready : int
        Number of messages ready to be delivered to consumers.
    messages_unacknowledged : int
        Number of messages delivered to consumers but not yet acknowledged.
    consumers : int
        Number of consumers currently subscribed to the queue.
    memory : int
        Amount of memory used by the queue (in bytes).
    message_stats : Optional[MessageStats]
        Detailed statistics about messages in the queue, if available.
    """

    def __init__(
        self,
        name: str,
        vhost: str,
        state: str,
        messages: int,
        messages_ready: int,
        messages_unacknowledged: int,
        consumers: int,
        memory: int,
        message_stats: Optional[MessageStats] = None,
    ):
        self._name = name
        self._vhost = vhost
        self._state = state
        self._messages = messages
        self._messages_ready = messages_ready
        self._messages_unacknowledged = messages_unacknowledged
        self._consumers = consumers
        self._memory = memory
        self._message_stats = message_stats

    @property
    def name(self) -> str:
        """Name of the queue being monitored."""
        return self._name

    @property
    def vhost(self) -> str:
        """Name of the virtual host to which the queue belongs."""
        return self._vhost

    @property
    def state(self) -> str:
        """Current state of the queue (e.g., running, idle)."""
        return self._state

    @property
    def messages(self) -> int:
        """Total number of messages in the queue."""
        return self._messages

    @property
    def messages_ready(self) -> int:
        """Number of messages ready to be delivered to consumers."""
        return self._messages_ready

    @property
    def messages_unacknowledged(self) -> int:
        """Number of messages delivered to consumers but not yet acknowledged."""
        return self._messages_unacknowledged

    @property
    def consumers(self) -> int:
        """Number of consumers currently subscribed to the queue."""
        return self._consumers

    @property
    def memory(self) -> int:
        """Amount of memory used by the queue (in bytes)."""
        return self._memory

    @property
    def message_stats(self) -> Optional[MessageStats]:
        """Detailed statistics about messages in the queue, if available."""
        return self._message_stats

    @classmethod
    def parse_json(cls, data: Dict[str, Any]) -> "QueueMonitor":
        """Parse a JSON string and return a QueueMonitor instance.

        Parameters
        ----------
        data: Dict[str, Any]
            Dictionary containing queue monitor data.

        Returns
        -------
        Instance of QueueMonitor.
        """
        return cls(
            name=data["name"],
            vhost=data["vhost"],
            state=data["state"],
            messages=data["messages"],
            messages_ready=data["messages_ready"],
            messages_unacknowledged=data["messages_unacknowledged"],
            consumers=data["consumers"],
            memory=data["memory"],
            message_stats=(
                MessageStats.parse_json(json.dumps(data["message_stats"])) if data.get("message_stats") else None
            ),
        )
