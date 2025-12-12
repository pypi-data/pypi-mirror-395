from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, Mapping, Optional, TypedDict, TypeVar

C = TypeVar("C")
Encoder = Callable[[C], str]


class _ServerOptionsRequired(TypedDict):
    api_key: str


class _ServerOptionsOptional(TypedDict, total=False):
    base_url: str
    num_connect_retries: int
    connect_retry_delay_ms: int


class ServerOptionsDict(_ServerOptionsRequired, _ServerOptionsOptional):
    pass


class _StreamOptionsRequired(TypedDict):
    stream_id: str


class _StreamOptionsOptional(TypedDict, total=False):
    overwrite_existing_stream: bool
    encoder: Callable[[Any], str]
    keep_open: bool


class StreamOptionsDict(_StreamOptionsRequired, _StreamOptionsOptional):
    pass


@dataclass(slots=True)
class _ServerOptions:
    api_key: str
    base_url: str | None = None
    num_connect_retries: int | None = None
    connect_retry_delay_ms: int | None = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "_ServerOptions":
        api_key = data.get("api_key")
        base_url = data.get("base_url")
        num_connect_retries = data.get("num_connect_retries")
        connect_retry_delay_ms = data.get("connect_retry_delay_ms")

        if not api_key:
            raise ValueError("api_key is required")

        return cls(
            api_key=api_key,
            base_url=base_url,
            num_connect_retries=num_connect_retries,
            connect_retry_delay_ms=connect_retry_delay_ms,
        )


@dataclass(slots=True)
class _StreamOptions(Generic[C]):
    stream_id: str
    overwrite_existing_stream: bool = False
    encoder: Optional[Encoder[C]] = None
    keep_open: bool = False

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "_StreamOptions[Any]":
        stream_id = data.get("stream_id")
        overwrite_existing_stream = data.get("overwrite_existing_stream", False)
        encoder = data.get("encoder")
        keep_open = data.get("keep_open", False)

        if not stream_id:
            raise ValueError("stream_id is required")

        return cls(
            stream_id=stream_id,
            overwrite_existing_stream=bool(overwrite_existing_stream),
            encoder=encoder,
            keep_open=bool(keep_open),
        )


def normalize_server_options(
    options: _ServerOptions | ServerOptionsDict | Mapping[str, Any],
) -> _ServerOptions:
    if isinstance(options, _ServerOptions):
        return options
    return _ServerOptions.from_mapping(options)


def normalize_stream_options(
    options: _StreamOptions[C] | StreamOptionsDict | Mapping[str, Any],
) -> _StreamOptions[C]:
    if isinstance(options, _StreamOptions):
        return options
    return _StreamOptions.from_mapping(options)


__all__ = [
    "ServerOptionsDict",
    "StreamOptionsDict",
    "_ServerOptions",
    "_StreamOptions",
    "normalize_server_options",
    "normalize_stream_options",
]
