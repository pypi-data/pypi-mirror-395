"""
API Service functionality for Autotrainer.
"""

from typing import Optional

from .api_options import ApiOptions, create_default_api_options
from .rpc_service import ApiTopic, ApiCommandRequest, ApiCommandRequestResponse, ApiCommandReqeustResult, RpcService

from .util import patch_uuid_encoder


def create_api_service(options: ApiOptions) -> Optional[RpcService]:
    from .zeromq import ZeroMQApiService

    # Several autotrainer messages may contain a UUID, which is not handled by the default JSON encoder.
    # patch_uuid_encoder()

    # TODO Enable when ready
    # configure_telemetry(options.telemetry)

    if options.rpc.enable:
        return ZeroMQApiService(options.rpc)
    else:
        return None
