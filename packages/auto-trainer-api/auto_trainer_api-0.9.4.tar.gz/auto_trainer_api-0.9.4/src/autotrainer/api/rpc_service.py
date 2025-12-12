import json
import logging
import time
from dataclasses import dataclass, asdict
from enum import IntEnum
from queue import Queue, Empty
from threading import Timer, Thread
from typing import Optional, Protocol, Any
from typing_extensions import Self

import humps

from .api_event_kind import ApiEventKind
from .api_options import RpcOptions

logger = logging.getLogger(__name__)


class ApiTopic(IntEnum):
    """
    A topic is required for all published messages.  This allows subscribers to filter messages through the message
    queue functionality rather than seeing all messages and filtering themselves.

    Any 4-byte integer value is valid.
    """
    ANY = 0
    HEARTBEAT = 1001
    """System heartbeat message indicating service availability."""
    EMERGENCY = 2001
    """Emergency only messages."""
    EVENT = 3001
    """
    Data generated from the published under the 'Event' umbrella, which is typically major system/application events.
    """
    COMMAND_RESULT = 4001
    """ Responses to asynchronous command handling. """


class ApiCommand(IntEnum):
    """
    A command value is required for all command requests.
    """
    NONE = 0
    START_ACQUISITION = 100
    STOP_ACQUISITION = 110
    EMERGENCY_STOP = 130
    EMERGENCY_RESUME = 135
    """No command.  Can be used to verify connection or that the receiver is configured to receive commands."""
    USER_DEFINED = 99999
    """A custom command defined between a particular commander and receiver.  Additional information can be 
    defined in the `data` field."""

    @classmethod
    def is_member(cls, value):
        return value in cls._value2member_map_


@dataclass(frozen=True)
class ApiCommandRequest:
    """
    A command request contains the command and any associated data.
    """
    command: ApiCommand
    custom_command: int = -1
    nonce: int = -1
    data: Optional[dict] = None

    @classmethod
    def parse_bytes(cls, message: bytes) -> Optional[Self]:
        obj = json.loads(humps.decamelize(message.decode("utf8")))

        return ApiCommandRequest.parse_object(obj)

    @classmethod
    def parse_object(cls, obj: Any) -> Optional[Self]:
        if "command" in obj:
            command = obj["command"]
            if ApiCommand.is_member(command):
                command = ApiCommand(command)
            else:
                command = ApiCommand.USER_DEFINED
            if "custom_command" in obj:
                custom_command = obj["custom_command"]
            else:
                custom_command = -1
            if "data" in obj:
                data = obj["data"]
            else:
                data = None
            if "nonce" in obj:
                nonce = obj["nonce"]
            else:
                nonce = 0

            return ApiCommandRequest(command=command, custom_command=custom_command, nonce=nonce, data=data)

        return None


class ApiCommandReqeustResult(IntEnum):
    """
    Result of a command request.
    """
    UNRECOGNIZED = 0
    """The client does not support this operation."""
    SUCCESS = 100
    """the command executed successfully."""
    PENDING = 200
    """The command was initiated but may not be complete."""
    PENDING_WITH_NOTIFICATION = 201
    """Command was initiated.  A specific event will post when the command completes."""
    FAILED = 400
    """The command was attempted, but could not be completed."""
    EXCEPTION = 500
    """The command was attempted and generated an exception."""
    UNAVAILABLE = 9999
    """The command is recognized, but not supported at this time."""


class ApiCommandRequestErrorKind(IntEnum):
    NONE = 0
    SYSTEM_ERROR = 0x01
    COMMAND_ERROR = 0x02


ApiCommandRequestSystemErrorSerialization: int = 0

NotificationEventKinds = [ApiEventKind.emergencyStop, ApiEventKind.emergencyResume]


@dataclass(frozen=True)
class ApiCommandRequestResponse:
    """
    A command response contains the command and any associated data.

    If the command request will have a result asynchronously in the future, one pattern would be to return some form
    of context in the data field that the client can use as a reference in a future published message.
    """
    nonce: int
    """
    This will be set to 0 if a command request could not be deserialized.  Caller should set the nonce to any value > 0
    if they want to be able to identify commands that were not simple unrecognized, but unparseable.
    """
    command: ApiCommand
    result: ApiCommandReqeustResult = ApiCommandReqeustResult.UNRECOGNIZED
    data: Optional[dict] = None
    error_kind: ApiCommandRequestErrorKind = ApiCommandRequestErrorKind.NONE
    error_code: int = 0
    error_message: Optional[str] = None

    def as_bytes(self, allow_fallback: bool = True) -> bytes:
        """
        This is guaranteed to return a valid response, even if modified due to any errors in serialization.  It must
        not throw.

        :param allow_fallback: true to allow serialization without the 'data' element if serialization initially fails.
        :return: serialized message as bytes
        """
        try:
            return humps.camelize(json.dumps(self.__dict__)).encode("utf8")
        except Exception as ex:
            logger.error(ex)

        if allow_fallback:
            # Assume it is an issue w/the contents of the user-definable dictionary contents
            contents = self.__dict__
            contents["data"] = None
            # If the next attempt works, this will have been the situation.
            contents["error_kind"] = ApiCommandRequestErrorKind.SYSTEM_ERROR
            contents["error_code"] = ApiCommandRequestSystemErrorSerialization
            contents["error_message"] = "An error occurred serializing the 'data' element of the response."
            try:
                return humps.camelize(json.dumps(contents)).encode("utf8")
            except Exception as ex:
                logger.error(ex)

        serialization_error = {"nonce": self.nonce, "command": self.command, "result": self.result,
                               "error_kind": ApiCommandRequestErrorKind.SYSTEM_ERROR,
                               "error_code": ApiCommandRequestSystemErrorSerialization,
                               "error_message": "An error occurred serializing the response."}

        return humps.camelize(json.dumps(serialization_error)).encode("utf8")

    @staticmethod
    def for_exception(command: ApiCommand, nonce: int, ex: Exception):
        return ApiCommandRequestResponse(command=command, nonce=nonce, result=ApiCommandReqeustResult.EXCEPTION,
                                         error_message=str(ex))


class CommandRequestDelegate(Protocol):
    """
    This callback is expected to be fast.  It is intended to initiate a command, not necessarily complete it.  Any
    non-trivial action is expected to accept the command request and return, perform the action on a non-calling thread
    or process, and use the message publishing API to report changes, results, etc.
    """

    def __call__(self, request: ApiCommandRequest) -> ApiCommandRequestResponse: ...


class ApiMessageQueueService(Protocol):
    """
    Minimum requirements to fulfill the API service message queue interface.  Implementation details are left to the
    implementation.

    Implementations are required to be able to publish messages to one or more subscribers.
    """

    def send(self, topic: ApiTopic, data: bytes) -> bool: ...

    def send_string(self, topic: ApiTopic, message: str) -> bool: ...

    def send_dict(self, topic: ApiTopic, message: dict) -> bool: ...


class ApiCommandRequestService(Protocol):
    """
    Minimum requirements to fulfill the API service command provider interface.  Implementation details are left to the
    implementation.

    Implementations are required to be able to receive command requests from one or more clients, deliver those requests
    to a registered handler, and provide an immediate response to the requester.  The response is a response to the
    _command request_ not necessarily the response to the command itself.  See CommandCallback for additional details.
    """

    @property
    def command_request_delegate(self) -> Optional[CommandRequestDelegate]: ...

    @command_request_delegate.setter
    def command_request_delegate(self, value: Optional[CommandRequestDelegate]): ...


@dataclass
class HeartbeatMessage:
    identifier: str
    version: str
    timestamp: float


class RpcService(ApiMessageQueueService, ApiCommandRequestService):
    def __init__(self, options: RpcOptions):
        self._subscriber_port = options.subscriber_port
        self._command_port = options.command_port
        self._identifier = options.identifier
        self._heartbeat_interval = options.heartbeat_interval
        self._heartbeat_timer = None
        self._heartbeat: HeartbeatMessage = HeartbeatMessage(
            identifier=options.identifier,
            version="0.9.3",
            timestamp=0.0
        )

        self._command_callback = None

        self._thread = None

        self._termination_requested = False

        self._queue = Queue()

    @property
    def subscriber_port(self) -> int:
        return self._subscriber_port

    @property
    def command_port(self) -> int:
        return self._command_port

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def heartbeat_interval(self) -> int:
        return self._heartbeat_interval

    @property
    def command_request_delegate(self) -> Optional[CommandRequestDelegate]:
        return self._command_callback

    @command_request_delegate.setter
    def command_request_delegate(self, value: Optional[CommandRequestDelegate]):
        if not self._termination_requested:
            self._command_callback = value
        else:
            logger.warning("The RPC service has been terminated. command_request_delegate not set")

    def start(self):
        if self._thread is None and not self._termination_requested:
            self._queue = Queue()
            self._thread = Thread(target=self._run, name="RpcServiceThread")
            self._thread.start()
        else:
            raise RuntimeError("The RPC service has already been started.")

    def stop(self):
        if self._thread is not None and not self._termination_requested:
            self._termination_requested = True
            self._command_callback = None
            if self._thread.is_alive():
                self._thread.join()

    def send(self, topic: ApiTopic, data: bytes) -> bool:
        if self._queue is None:
            raise RuntimeError("The RPC service has not been started.")

        if not self._termination_requested:
            self._queue.put(lambda: self._send(topic, data))
            return True

        logger.warning("The RPC service has been terminated.  Message not sent.")
        return False

    def send_string(self, topic: ApiTopic, message: str) -> bool:
        if self._queue is None:
            raise RuntimeError("The RPC service has not been started.")

        if not self._termination_requested:
            self._queue.put(lambda: self._send_string(topic, message))
            return True

        logger.warning("The RPC service has been terminated.  Message not sent.")
        return False

    def send_dict(self, topic: ApiTopic, message: dict) -> bool:
        if self._queue is None:
            raise RuntimeError("The RPC service has not been started.")

        if not self._termination_requested:
            if topic == ApiTopic.EVENT and "kind" in message and message["kind"] in NotificationEventKinds:
                # If an emergency event is posted in the normal event channel, ensure it goes out on the emergency
                # topic as well.
                self._queue.put(lambda: self._send_dict(ApiTopic.EMERGENCY, message))
            self._queue.put(lambda: self._send_dict(topic, message))

            return True

        logger.warning("The RPC service has been terminated.  Message not sent.")
        return False

    def _run(self):
        try:
            if not self._start():
                logger.error(f"failed to start api service")
                self._update_after_run()
                return
        except Exception:
            logger.exception("exception starting api service")
            self._update_after_run()
            return

        self._queue_heartbeat()

        while not self._termination_requested:
            # Required to be non-blocking and exception safe by the rpc-specific implementation.
            request = self._get_next_command_request()

            if request is not None:
                # Expected to happen fast.  Most message queue implementations that provide a request/response-type
                # pattern require that a response be sent before the next request is received.  And the associated
                # client/caller implementation requires the response before accepting another request.
                #
                # If this becomes an untenable requirement, a different pattern will be required for command
                # requests (and the underlying implementations update).  However, anything that allows interleaving
                # multiple requests from the same client with responses would effectively be the same as this
                # pattern where there is an immediate _request_ response and a delayed _command_ response through
                # the message queue.
                #
                # NOTE: There is no inherent limitation in this pattern with multiple requests from multiple
                # clients.  This is related to the handling of each individual client.

                if self._command_callback is not None:
                    try:
                        # Can not assume the registered delegate will be well-behaved.
                        self._send_command_response(self._command_callback(request))
                    except Exception as e:
                        self._send_command_response(
                            ApiCommandRequestResponse.for_exception(request.command, request.nonce, e))
                else:
                    # Must provide a response, even if no one that registered this service cares (using for the
                    # message queue only, etc.).
                    self._send_command_response(
                        ApiCommandRequestResponse(command=request.command, nonce=request.nonce,
                                                  result=ApiCommandReqeustResult.UNAVAILABLE))

            try:
                action = self._queue.get(timeout=0.05)

                # This is performed by the internal rpc implementation.  It should be exception safe or the
                # implementation should be corrected.
                action()

            except Empty:
                # Expected from get_nowait() if there is nothing in the queue.
                pass

        self._update_after_run()

    def _update_after_run(self):
        self._cancel_heartbeat()

        self._stop()

    def _queue_heartbeat(self):
        self._heartbeat_timer = Timer(self._heartbeat_interval, self._heartbeat_timer_callback)
        self._heartbeat_timer.start()

    def _cancel_heartbeat(self):
        if self._heartbeat_timer is not None:
            self._heartbeat_timer.cancel()
            self._heartbeat_timer = None

    def _heartbeat_timer_callback(self):
        # Must happen on the queue processing thread.
        if not self._termination_requested:
            self._heartbeat.timestamp = time.time()
            self._send_dict(ApiTopic.HEARTBEAT, asdict(self._heartbeat))
            self._queue_heartbeat()

    def _start(self) -> bool:
        raise NotImplementedError("Subclasses must implement _start()")

    def _stop(self):
        raise NotImplementedError("Subclasses must implement _stop()")

    def _send(self, topic: ApiTopic, data: bytes) -> bool:
        return False

    def _send_string(self, topic: ApiTopic, message: str) -> bool:
        return False

    def _send_dict(self, topic: ApiTopic, message: dict) -> bool:
        return False

    def _get_next_command_request(self) -> Optional[ApiCommandRequest]:
        """
        If a command request is returned, the subclass/implementation can assume that a responses will be sent
        (via the `_command_response()_` method).  If something is received by the implementation that can not be
        returned as a valid command request (malformed, incomplete, etc.), it is the responsibility of the
        implementation to provide a response if that is required by the particular implementation (e.g., request/reply
        requiring a response to every request, etc.).

        :return: a command request if available, None otherwise
        """
        return None

    def _send_command_response(self, response: ApiCommandRequestResponse):
        pass
