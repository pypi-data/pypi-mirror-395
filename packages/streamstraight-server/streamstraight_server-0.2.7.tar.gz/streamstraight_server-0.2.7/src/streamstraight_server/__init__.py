"""Python server SDK for Streamstraight."""

import logging

from .jwt_token import StreamstraightTokenError, fetch_client_token
from .main import streamstraight_server
from .options import ServerOptionsDict, StreamOptionsDict
from .server import (
    StreamstraightServer,
    StreamstraightServerAbortError,
    StreamstraightServerError,
    StreamWriter,
)

# Set default logging level to ERROR for the SDK
# Users can override this by calling logging.getLogger("streamstraight_server").setLevel(...)
logging.getLogger(__name__).setLevel(logging.ERROR)

__all__ = [
    "ServerOptionsDict",
    "StreamOptionsDict",
    "StreamWriter",
    "StreamstraightServer",
    "StreamstraightServerAbortError",
    "StreamstraightServerError",
    "streamstraight_server",
    "fetch_client_token",
    "StreamstraightTokenError",
]
