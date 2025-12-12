"""Protocol definitions mirroring the TypeScript SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

CURRENT_PROTOCOL_VERSION = "stream-v1"


class ConnectionServerToClientEvents:
    ERROR = "connection:error"


class ProducerClientToServerEvents:
    CHUNK = "producer:chunk"
    END = "producer:end"
    HEARTBEAT = "producer:heartbeat"


class ProducerServerToClientEvents:
    ACK = "producer:ack"
    ERROR = "stream:error"
    INFO = "stream:info"


class ConsumerClientToServerEvents:
    READY = "consumer:ready"


class ConsumerServerToClientEvents:
    CHUNK = "stream:chunk"
    END = "stream:end"
    ERROR = "stream:error"
    INFO = "stream:info"


StreamEndReason = Literal[
    "completed",
    "producer-error",
    "producer-disconnected",
    "inactivity-timeout",
    "not-found",
    "ignore-ended",
]


class StreamChunkPushPayload(TypedDict, total=False):
    seq: int
    data: str
    terminal: bool


class StreamChunkAckPayload(TypedDict):
    seq: int
    redisId: str


class StreamEndNotification(TypedDict, total=False):
    reason: StreamEndReason
    lastSeq: int
    redisId: str | None


class StreamErrorPayload(TypedDict, total=False):
    message: str
    code: str | None
    retryInMs: int | None


class StreamInfoPayload(TypedDict, total=False):
    streamId: str
    deploymentId: str
    lastSeq: int | None
    ended: bool


class StreamEndAckSuccess(TypedDict):
    success: Literal[True]
    endRedisId: str


class StreamEndAckError(TypedDict):
    success: Literal[False]
    error: str


StreamEndAck = StreamEndAckSuccess | StreamEndAckError


class ProducerHandshakeAuth(TypedDict, total=False):
    role: Literal["producer"]
    streamId: str
    version: str
    sdkVersion: str
    overwriteExistingStream: bool


@dataclass(slots=True)
class ClientTokenResponse:
    token: str
