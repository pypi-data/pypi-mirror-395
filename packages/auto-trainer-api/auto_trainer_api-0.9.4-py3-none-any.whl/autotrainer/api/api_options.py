from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TelemetryOptions:
    enable: bool = False
    endpoint: Optional[str] = None
    api_key: str = ""


@dataclass(frozen=True)
class RpcOptions:
    enable: bool = True
    identifier: str = "autotrainer-device"
    heartbeat_interval: int = 5
    subscriber_port: int = 5556
    command_port: int = 5557


@dataclass(frozen=True)
class ApiOptions:
    rpc: Optional[RpcOptions] = None
    telemetry: Optional[TelemetryOptions] = None


def create_default_api_options() -> ApiOptions:
    """
    Create default API options for the Autotrainer API service.
    """

    return ApiOptions(rpc=RpcOptions(), telemetry=TelemetryOptions())
