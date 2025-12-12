from __future__ import annotations

from typing import Any, Mapping, TypeVar

from .options import (
    ServerOptionsDict,
    StreamOptionsDict,
    _ServerOptions,
    _StreamOptions,
    normalize_server_options,
    normalize_stream_options,
)
from .server import StreamstraightServer

C = TypeVar("C")


async def streamstraight_server(
    server_options: _ServerOptions | ServerOptionsDict | Mapping[str, Any],
    stream_options: _StreamOptions[C] | StreamOptionsDict | Mapping[str, Any],
) -> StreamstraightServer[C]:
    normalized_server_options = normalize_server_options(server_options)
    normalized_stream_options = normalize_stream_options(stream_options)

    server: StreamstraightServer[C] = StreamstraightServer(normalized_server_options)
    await server.connect(normalized_stream_options)
    return server


__all__ = ["streamstraight_server"]
