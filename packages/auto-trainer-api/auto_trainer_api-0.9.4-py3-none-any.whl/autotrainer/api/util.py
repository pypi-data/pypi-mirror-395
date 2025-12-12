import socket
from datetime import datetime
from json import JSONEncoder
from uuid import UUID

_IS_JSON_ENCODER_PATCHED = False


def get_ip4_addr_str() -> str:
    # gethostname() and gethostbyname() and associated IP lookup have proven unreliable on deployed devices where the
    # configuration is not perfect.  This method assumes access to the internet (Google DNS) which has its own
    # limitations.  A more complex implementation to manage all conditions but avoid ending up with 12.0.0.1 when an
    # actual address is available is needed.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()

    return ip


def patch_uuid_encoder():
    global _IS_JSON_ENCODER_PATCHED

    if not _IS_JSON_ENCODER_PATCHED:
        JSONEncoder.default = UUIDEncoder.default
        _IS_JSON_ENCODER_PATCHED = True


class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.timestamp()
        return super().default(obj)
