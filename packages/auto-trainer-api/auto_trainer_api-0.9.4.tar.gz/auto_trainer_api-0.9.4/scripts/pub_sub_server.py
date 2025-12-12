"""
Create an instance of an Api Service implementation to received published messages and send command requests.
"""

import logging

from autotrainer.api import ApiCommandRequest, ApiCommandRequestResponse, ApiCommandReqeustResult
from autotrainer.api import create_api_service
from autotrainer.api import create_default_api_options


def _respond_to_command_request(request: ApiCommandRequest) -> ApiCommandRequestResponse:
    logger.debug("Received command request: %s", request.command)
    return ApiCommandRequestResponse(command=request.command, data={"seen": True},
                                     result=ApiCommandReqeustResult.SUCCESS, nonce=request.nonce)


def run_server():
    options = create_default_api_options()

    service = create_api_service(options)

    service.command_request_delegate = _respond_to_command_request

    service.start()

    input("Press enter to stop the service...\n")

    service.stop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s\t [%(name)s] %(message)s")
    logging.getLogger('autotrainer').setLevel(logging.DEBUG)
    logging.getLogger('tools').setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)

    run_server()
