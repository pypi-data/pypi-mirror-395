import json
import logging
from typing import Optional

import zmq
import humps

from ..rpc_service import RpcService, RpcOptions, ApiTopic, ApiCommandRequestResponse, ApiCommandRequest, ApiCommand
from ..util import get_ip4_addr_str, UUIDEncoder

logger = logging.getLogger(__name__)


class ZeroMQApiService(RpcService):
    def __init__(self, options: RpcOptions):
        super().__init__(options)

        ips = [get_ip4_addr_str()]

        if ips[0] != "127.0.0.1":
            ips.append("127.0.0.1")

        self._pub_addresses = [f"tcp://{ip}:{self.subscriber_port}" for ip in ips]
        self._pub_socket = None

        self._cmd_addresses = [f"tcp://{ip}:{self.command_port}" for ip in ips]
        self._cmd_socket = None

        self._response_pending = False

    def _start(self) -> bool:
        if self._pub_socket is not None:
            return True

        try:
            context = zmq.Context()

            self._pub_socket = context.socket(zmq.PUB)
            for address in self._pub_addresses:
                self._pub_socket.bind(address)
                logger.debug(f"ZMQ PUB socket bound to {address}")

            context = zmq.Context()

            self._cmd_socket = context.socket(zmq.REP)
            for address in self._cmd_addresses:
                self._cmd_socket.bind(address)
                logger.debug(f"ZMQ REP socket bound to {address}")
        except zmq.error.ZMQError:
            self._pub_socket = None
            self._cmd_socket = None
            logger.info(f"ZMQ not started.  Address may already be in use.")
            return False

        return True

    def _stop(self):
        if self._pub_socket is not None:
            for address in self._pub_addresses:
                self._pub_socket.disconnect(address)
            self._pub_socket = None
        if self._cmd_socket is not None:
            for address in self._cmd_addresses:
                self._cmd_socket.disconnect(address)
            self._cmd_socket = None

    def _send(self, topic: ApiTopic, data: bytes):
        if self._pub_socket is not None:
            self._pub_socket.send(topic.to_bytes(4, "little"), flags=zmq.SNDMORE)
            self._pub_socket.send(data)

    def _send_string(self, topic: ApiTopic, message: str):
        if self._pub_socket is not None:
            self._pub_socket.send(topic.to_bytes(4, "little"), flags=zmq.SNDMORE)
            self._pub_socket.send(message.encode("utf8"))

    def _send_dict(self, topic: ApiTopic, message: dict):
        if self._pub_socket is not None:
            try:
                # Convert the dictionary to a JSON string and then encode it to bytes.
                json_data = humps.camelize(json.dumps(message, cls=UUIDEncoder))
                self._pub_socket.send(topic.to_bytes(4, "little"), flags=zmq.SNDMORE)
                self._pub_socket.send_json(json_data)
            except Exception as ex:
                logger.error(ex)

    def _get_next_command_request(self) -> Optional[ApiCommandRequest]:
        if self._cmd_socket is not None and not self._response_pending:
            try:
                message = self._cmd_socket.recv(flags=zmq.NOBLOCK)

                self._response_pending = True

                request = ZeroMQApiService._parse_command_request(message)

                logger.info(f"Received command request: {request.command}")

                if request is None:
                    # If a request was received, but could not be parsed, the requester is still expecting a response.
                    # Otherwise, the ZeroMQ socket on both ends will be in a lingering state.  Send it ourselves since
                    # returning None will not generate a response by the caller.
                    self._send_command_response(ApiCommandRequestResponse(command=ApiCommand.NONE, nonce=0))

                # A response will be sent by the caller if a request is returned.
                return request

            except zmq.Again:
                # No messages available from recv().
                pass

        return None

    def _send_command_response(self, response: ApiCommandRequestResponse):
        if self._cmd_socket is not None:
            # This is guaranteed to return a valid response, even if modified due to any errors in serialization.
            data = response.as_bytes(True)

            self._cmd_socket.send(data)

            self._response_pending = False

    @staticmethod
    def _parse_command_request(message: bytes) -> Optional[ApiCommandRequest]:
        try:
            return ApiCommandRequest.parse_bytes(message)
        except json.decoder.JSONDecodeError as ex:
            # Might do something different here.
            logger.error(ex)
        except Exception as ex:
            logger.error(ex)

        return None
