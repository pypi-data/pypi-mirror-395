from __future__ import annotations

import os
from collections.abc import Callable
from threading import Event
from typing import Any, TypeVar

import zenoh

from common.message import Message

DEFAULT_COMMS_SUBSCRIBER_RING_DEPTH = 4096

T = TypeVar("T", bound=Message)


class CommsSession:
    """
    Lightweight, synchronous communication session built on top of Zenoh.

    This session provides send/publish operations, subscriber creation, and
    advanced features like queryables and direct publisher management.
    """

    def __init__(self):
        """
        Create a new communication session.
        """

        # Get router endpoint from environment or use localhost default
        router_endpoint = os.environ.get("ZENOH_ROUTER_ENDPOINT", "tcp/127.0.0.1:7447")

        self.config = zenoh.Config()
        self.config.insert_json5("mode", '"peer"')
        self.config.insert_json5("listen/endpoints", '["tcp/0.0.0.0:0"]')
        self.config.insert_json5("scouting/multicast/enabled", "false")
        self.config.insert_json5("connect/endpoints", f'["{router_endpoint}"]')  # Discovery via router
        self.session = zenoh.open(self.config)

    def __del__(self) -> None:
        """
        Ensure the session is closed when garbage collected.
        """

        self.close()

    def __enter__(self) -> CommsSession:
        """
        Enter the context manager.
        """

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit the context manager and close the session.
        """

        self.close()

    def get_session_info(self) -> dict[str, Any]:
        """
        Get information about the session.

        :return: Information about the Zenoh session.
        """

        return {
            "zid": self.session.info.zid(),
            "routers": self.session.info.routers_zid(),
            "peers": self.session.info.peers_zid(),
        }

    def declare_subscriber(self, path: str) -> CommsSubscriber:
        """
        Create a new subscriber for the given path.

        :param path: The path to subscribe to.
        :return: A new CommsSubscriber instance.
        """

        return CommsSubscriber(self.session, path)

    def declare_async_subscriber(self, path: str) -> CommsAsyncSubscriber:
        """
        Create a new async subscriber that uses callbacks for event-driven reception.

        :param path: The path to subscribe to.
        :return: A new CommsAsyncSubscriber instance.
        """

        return CommsAsyncSubscriber(self.session, path)

    def declare_callback_subscriber(
        self,
        path: str,
        callback: Callable[[zenoh.Sample], None],
    ) -> zenoh.Subscriber[None]:
        """
        Create a new callback subscriber for the given path.

        :param path: The path to subscribe to.
        :param callback: Callback function to handle incoming messages.
        :return: A new zenoh.Subscriber instance.
        """

        return self.session.declare_subscriber(path, callback)

    def declare_queryable(
        self,
        path: str,
        complete: bool = True,
    ) -> CommsQueryable:
        """
        Create a synchronous queryable endpoint for request-response patterns.

        Returns a queryable wrapper that provides a clean API for receiving queries.

        :param path: The path pattern to respond to queries on.
        :param complete: Whether this queryable provides complete information.
        :return: A new CommsQueryable instance.
        """

        return CommsQueryable(self.session, path, complete)

    def declare_callback_queryable(
        self,
        path: str,
        callback: Callable[[zenoh.Query], None],
        complete: bool = True,
    ) -> zenoh.Queryable[None]:
        """
        Create a callback-based queryable for async request-response patterns.

        The callback is invoked by Zenoh automatically for each query, allowing
        asynchronous handling without manual recv() calls.

        :param path: The path pattern to respond to queries on.
        :param callback: Callback function that receives zenoh.Query objects directly.
        :param complete: Whether this queryable provides complete information.
        :return: A new zenoh.Queryable instance.
        """

        return self.session.declare_queryable(path, callback, complete=complete)

    def declare_publisher(self, path: str) -> CommsPublisher:
        """
        Create a dedicated publisher for a path.

        :param path: The path to publish to.
        :return: A CommsPublisher instance.
        """

        return CommsPublisher(self.session, path)

    def query(
        self,
        path: str,
        response_type: type[T],
        request: Message | bytes | None = None,
        target: zenoh.QueryTarget = zenoh.QueryTarget.ALL,
        timeout: float = 10.0,
    ) -> T:
        """
        Send a typed query and wait for the first response.

        :param path: The path to query.
        :param response_type: The expected message type class for the response.
        :param request: Optional request message to send with the query.
        :param target: The target of the query.
        :param timeout: Maximum time to wait for a reply in seconds.
        :return: The first successful response message.
        :raises TimeoutError: When the query times out.
        """

        payload = None
        if request is not None:
            if isinstance(request, Message):
                request = request.pack()
            payload = request

        # Send query with payload
        replies = self.session.get(
            path,
            target=target,
            payload=payload,
            timeout=timeout,
            consolidation=zenoh.ConsolidationMode.NONE,
            congestion_control=zenoh.CongestionControl.DROP,
        )

        # Get first valid response
        for reply in replies:
            result = reply.result
            if isinstance(result, zenoh.ReplyError):
                error = result.payload.to_string()
                if "timeout" in error.lower():
                    raise TimeoutError(f"Query {path} timed out")
                raise RuntimeError(f"Query {path} failed: {error}")
            return response_type.unpack(result.payload.to_bytes())

        # Raise error if no response was received
        raise RuntimeError(f"No response received for query {path}")

    def close(self) -> None:
        """
        Close the communication session.
        """

        if not self.session.is_closed():
            self.session.close()


class CommsSubscriber:
    """
    Communication subscriber for handling message reception.

    Provides methods for receiving messages from a specific communication path.
    Each subscriber operates independently with its own message buffer.
    """

    def __init__(self, session: zenoh.Session, path: str) -> None:
        """
        Initialize the subscriber.

        :param session: The Zenoh session.
        :param path: The path to subscribe to.
        """

        handler = zenoh.handlers.RingChannel(DEFAULT_COMMS_SUBSCRIBER_RING_DEPTH)
        self._subscriber = session.declare_subscriber(path, handler)

    def recv(self, message_cls: type[T]) -> T:
        """
        Receive the next message, blocking until one is available.

        :param message_cls: The expected message type class.
        :return: The deserialized message.
        """

        sample = self._subscriber.handler.recv()
        data = sample.payload.to_bytes()
        return message_cls.unpack(data)

    def recv_latest(self, message_cls: type[T]) -> T:
        """
        Drain all messages and return the latest one, blocking if none available.

        This method prevents the "drain bug" by ensuring we always get the most
        recent message, discarding any stale messages that may have accumulated.

        :param message_cls: The expected message type class.
        :return: The latest deserialized message.
        """

        latest_sample = None

        # First, drain all available messages without blocking
        # We don't deserialize here - just keep the raw samples
        while True:
            sample = self._subscriber.handler.try_recv()
            if sample is None:
                break
            latest_sample = sample

        # If we have a latest sample, deserialize and return it
        if latest_sample is not None:
            data = latest_sample.payload.to_bytes()
            return message_cls.unpack(data)

        # Otherwise, wait for a new message
        return self.recv(message_cls)

    def try_recv(self, message_cls: type[T]) -> T | None:
        """
        Try to receive a message without blocking.

        :param message_cls: The expected message type class.
        :return: The deserialized message if available, None otherwise.
        """

        sample = self._subscriber.handler.try_recv()
        if sample is None:
            return None

        data = sample.payload.to_bytes()
        return message_cls.unpack(data)

    def try_recv_sample(self) -> zenoh.Sample | None:
        """
        Try to receive a raw sample without blocking.

        :return: The raw Zenoh sample if available, None otherwise.
        """

        return self._subscriber.handler.try_recv()

    def try_recv_latest(self, message_cls: type[T]) -> T | None:
        """
        Try to drain all messages and return the latest one without blocking.

        This is the non-blocking version of recv_latest. It prevents the "drain bug"
        by ensuring we always get the most recent message if any are available.

        :param message_cls: The expected message type class.
        :return: The latest deserialized message if available, None otherwise.
        """

        latest_sample = None

        # Drain all available messages without blocking
        # We don't deserialize here - just keep the raw samples
        while True:
            sample = self._subscriber.handler.try_recv()
            if sample is None:
                break
            latest_sample = sample

        # If we have a latest sample, deserialize and return it
        if latest_sample is not None:
            data = latest_sample.payload.to_bytes()
            return message_cls.unpack(data)

        return None

    def drain(self) -> bool:
        """
        Drain all queued messages without processing them.

        :return: True if any messages were drained, False otherwise.
        """

        drained_any = False
        while self._subscriber.handler.try_recv() is not None:
            drained_any = True

        return drained_any

    def close(self) -> None:
        """
        Close the subscriber and release resources.
        """

        self._subscriber.undeclare()


class CommsAsyncSubscriber:
    """
    Async subscriber that uses callbacks for event-driven message reception.

    Provides blocking recv with timeout and automatic wake-up on message arrival.
    Useful for event-driven loops that need to respond to both messages and shutdown events.
    """

    def __init__(self, session: zenoh.Session, path: str) -> None:
        """
        Initialize the async subscriber.

        :param session: The Zenoh session.
        :param path: The path to subscribe to.
        """

        self._message_available = Event()
        self._latest_sample: zenoh.Sample | None = None
        self._subscriber = session.declare_subscriber(path, self._on_message)

    def recv_timeout(self, message_cls: type[T], timeout: float | None = None) -> T | None:
        """
        Receive a message with optional timeout.

        Blocks until a message arrives or timeout expires. Uses event-driven
        approach to wake up immediately when messages arrive.

        :param message_cls: The expected message type class.
        :param timeout: Timeout in seconds (None for infinite).
        :return: The deserialized message if available, None on timeout.
        """

        # Wait for message with timeout
        if not self._message_available.wait(timeout):
            return None
        if self._latest_sample is None:
            raise RuntimeError("No message available")

        # Get the message and reset event
        data = self._latest_sample.payload.to_bytes()
        self._latest_sample = None
        self._message_available.clear()
        return message_cls.unpack(data)

    def close(self) -> None:
        """
        Close the subscriber and release resources.
        """

        self._subscriber.undeclare()

    def _on_message(self, sample: zenoh.Sample) -> None:
        """
        Callback invoked when a message arrives.

        :param sample: The received sample.
        """

        self._latest_sample = sample
        self._message_available.set()


class CommsPublisher:
    """
    Dedicated publisher for efficient message publication to a single path.
    """

    def __init__(self, session: zenoh.Session, path: str) -> None:
        """
        Initialize the publisher.

        :param session: The Zenoh session.
        :param path: The path to publish to.
        """

        self._publisher = session.declare_publisher(
            path,
            congestion_control=zenoh.CongestionControl.DROP,
            reliability=zenoh.Reliability.BEST_EFFORT,
        )

    def publish(self, data: bytes | Message) -> None:
        """
        Publish data to the publisher's path.

        :param data: Raw bytes or a Message that will be serialized.
        """

        if isinstance(data, Message):
            data = data.pack()
        self._publisher.put(data)

    def close(self) -> None:
        """
        Close the publisher and release resources.
        """

        self._publisher.undeclare()


class Query:
    """
    Communication query for handling response to a query request.

    Important: make sure you call drop() (or use the context manager) to make sure
    the query is finalized!
    """

    def __init__(self, query: zenoh.Query) -> None:
        """
        Initialize the query.

        :param query: The underlying Zenoh query.
        """

        self._query = query

    def __enter__(self) -> Query:
        """
        Enter the context manager.
        """

        self._query.__enter__()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit the context manager and drop the query.
        """

        self._query.__exit__(exc_type, exc_val, exc_tb)

    @property
    def key_expr(self) -> str:
        """
        Get the key expression of the query.

        :return: The key expression.
        """

        return str(self._query.key_expr)

    def payload(self, message_cls: type[T]) -> T:
        """
        Get the payload of the query.

        :param message_cls: The message type to unpack the payload into.
        :return: The unpacked message.
        :raises RuntimeError: If the query has no payload.
        """

        if self._query.payload is None:
            raise RuntimeError("Query has no payload")
        return message_cls.unpack(self._query.payload.to_bytes())

    def reply(self, data: Message | bytes) -> None:
        """
        Send a reply to the query.

        :param data: Response data. Raw bytes or a Message that will be serialized.
        """

        if isinstance(data, Message):
            data = data.pack()
        self._query.reply(
            self._query.key_expr,
            payload=data,
            congestion_control=zenoh.CongestionControl.DROP,
        )

    def drop(self) -> None:
        """
        Drop the query.
        """

        self._query.drop()


class CommsQueryable:
    """
    Lightweight wrapper around a Zenoh queryable for request-response patterns.

    Provides a clean API for receiving and processing queries without manual unwrapping.
    """

    def __init__(self, session: zenoh.Session, path: str, complete: bool = True) -> None:
        """
        Initialize the queryable wrapper.

        :param session: The Zenoh session.
        :param path: The path pattern to respond to queries on.
        :param complete: Whether this queryable provides complete information.
        """

        handler = zenoh.handlers.RingChannel(DEFAULT_COMMS_SUBSCRIBER_RING_DEPTH)
        self._queryable = session.declare_queryable(path, handler, complete=complete)

    def recv(self) -> Query:
        """
        Receive the next query, blocking until one is available.

        :return: The query wrapped in our Query helper.
        """

        zenoh_query = self._queryable.handler.recv()
        return Query(zenoh_query)

    def try_recv(self) -> Query | None:
        """
        Try to receive a query without blocking.

        :return: The query wrapped in our Query helper, or None if no query available.
        """

        zenoh_query = self._queryable.handler.try_recv()
        if zenoh_query is None:
            return None
        return Query(zenoh_query)

    def close(self) -> None:
        """
        Close the queryable and release resources.
        """

        self._queryable.undeclare()
