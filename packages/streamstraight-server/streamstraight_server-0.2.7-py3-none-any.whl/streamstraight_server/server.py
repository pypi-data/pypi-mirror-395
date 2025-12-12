from __future__ import annotations

import asyncio
import json
import logging
import sys
import types
from collections.abc import AsyncIterable
from typing import Any, Dict, Generic, Mapping, Optional, TypeVar, cast

import socketio

from .constants import (
    DEFAULT_CONNECT_RETRY_DELAY_MS,
    DEFAULT_NUM_CONNECT_RETRIES,
    get_base_url,
    get_package_version,
)
from .options import (
    ServerOptionsDict,
    StreamOptionsDict,
    _ServerOptions,
    _StreamOptions,
    normalize_server_options,
    normalize_stream_options,
)
from .protocol import (
    CURRENT_PROTOCOL_VERSION,
    ConnectionServerToClientEvents,
    ProducerClientToServerEvents,
    ProducerHandshakeAuth,
    ProducerServerToClientEvents,
    StreamEndAck,
    StreamEndNotification,
    StreamEndReason,
    StreamErrorPayload,
    StreamInfoPayload,
)
from .utils import ensure_async_iterable


def _default_encode_chunk(chunk: Any) -> str:
    """Encode outbound payloads, supporting Pydantic v2 models by default."""

    model_dump_json = getattr(chunk, "model_dump_json", None)
    if callable(model_dump_json):
        # Pydantic v2 models expose ``model_dump_json`` which already returns a ``str``.
        return cast(str, model_dump_json())

    return json.dumps(chunk, separators=(",", ":"))


logger = logging.getLogger(__name__)

C = TypeVar("C")


class StreamstraightServerError(Exception):
    """Raised when the Streamstraight server SDK encounters an error."""


class StreamstraightServerAbortError(StreamstraightServerError):
    """Raised when a connection attempt is intentionally aborted."""

    def __init__(self) -> None:
        super().__init__("connect aborted")


class _ConnectionAttemptError(Exception):
    """Internal sentinel used to retry socket connection attempts."""


class StreamstraightServer(Generic[C]):
    def __init__(self, options: _ServerOptions | ServerOptionsDict | Mapping[str, Any]):
        options = normalize_server_options(options)
        if not options.api_key:
            raise StreamstraightServerError("api_key is required")

        self._options = options
        self._socket: Optional[socketio.AsyncClient] = None
        self._stream_options: Optional[_StreamOptions[C]] = None
        self._seq = 0
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._connect_lock = asyncio.Lock()
        self._connect_aborted = False
        self._connect_waiter: Optional[asyncio.Future[None]] = None
        self._disconnect_error: Optional[StreamstraightServerError] = None
        self._streaming = False  # Track if we're actively streaming

    async def connect(
        self, stream_options: _StreamOptions[C] | StreamOptionsDict | Mapping[str, Any]
    ) -> None:
        stream_options = normalize_stream_options(stream_options)
        logger.info(
            "[streamstraight-server] connect requested stream_id=%s overwrite=%s keep_open=%s",
            stream_options.stream_id,
            stream_options.overwrite_existing_stream,
            stream_options.keep_open,
        )

        num_retries_raw = self._options.num_connect_retries
        num_retries = max(
            0, num_retries_raw if num_retries_raw is not None else DEFAULT_NUM_CONNECT_RETRIES
        )
        retry_delay_raw = self._options.connect_retry_delay_ms
        retry_delay_ms = max(
            0, retry_delay_raw if retry_delay_raw is not None else DEFAULT_CONNECT_RETRY_DELAY_MS
        )

        async with self._connect_lock:
            # Check inside lock to prevent concurrent connections
            if self._socket and self._socket.connected:
                logger.warning("[streamstraight-server] socket already connected")
                return

            self._connect_aborted = False
            self._disconnect_error = None

            url = self._options.base_url or get_base_url()
            base_auth: ProducerHandshakeAuth = {
                "role": "producer",
                "streamId": stream_options.stream_id,
                "version": CURRENT_PROTOCOL_VERSION,
                "sdkVersion": get_package_version(),
            }
            if stream_options.overwrite_existing_stream:
                base_auth["overwriteExistingStream"] = True

            headers = {"Authorization": f"Bearer {self._options.api_key}"}

            for index in range(0, num_retries + 1):
                if self._connect_aborted:
                    await self.disconnect()
                    raise StreamstraightServerAbortError()

                self._stream_options = stream_options
                self._loop = asyncio.get_running_loop()
                self._seq = 0
                self._socket = socketio.AsyncClient()
                # Keep reference to socket for cleanup even if self._socket is cleared
                current_socket = self._socket
                self._connect_waiter = self._loop.create_future()
                connect_waiter = self._connect_waiter

                self._register_handlers()

                logger.info(
                    "[streamstraight-server] connecting url=%s role=%s stream_id=%s attempt=%s/%s",
                    url,
                    base_auth["role"],
                    stream_options.stream_id,
                    index + 1,
                    num_retries + 1,
                )

                try:
                    connect_task = asyncio.create_task(
                        current_socket.connect(url, auth=dict(base_auth), headers=headers)
                    )
                    if connect_waiter is None:
                        raise StreamstraightServerError("connect waiter not initialized")

                    # Do this so that we abort the other coroutine when one fails.
                    done, pending = await asyncio.wait(
                        {connect_task, connect_waiter},
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    if connect_waiter in done:
                        try:
                            await asyncio.shield(connect_waiter)
                        except Exception as exc:
                            # We care more about the connect_waiter error than the connect_task error
                            connect_task.cancel()
                            try:
                                await connect_task
                            except asyncio.CancelledError:
                                pass
                            except Exception:
                                pass  # Ignore this error; instead, raise the error from connect_waiter
                            raise exc
                        if connect_task not in done:
                            await asyncio.shield(connect_task)
                    else:
                        await asyncio.shield(connect_task)
                        await asyncio.shield(connect_waiter)

                    # Final abort check after successful connection
                    if self._connect_aborted:
                        try:
                            await current_socket.disconnect()
                        except Exception:
                            pass
                        self._socket = None
                        raise StreamstraightServerAbortError()

                    logger.info(
                        "[streamstraight-server] socket connected stream_id=%s attempts=%s",
                        stream_options.stream_id,
                        index + 1,
                    )
                    return
                except Exception as exc:  # pragma: no cover - passthrough to caller
                    # Ensure we disconnect the socket we were trying to connect, even if
                    # self._socket was already cleared by a concurrent disconnect() call
                    if current_socket:
                        try:
                            await current_socket.disconnect()
                        except Exception:
                            pass

                    await self._cleanup_socket()

                    if isinstance(exc, _ConnectionAttemptError):
                        self._connect_aborted = False

                    if isinstance(exc, asyncio.CancelledError):
                        raise
                    if self._connect_aborted:
                        # If exception is already StreamstraightServerAbortError, preserve it
                        if isinstance(exc, StreamstraightServerAbortError):
                            raise
                        raise StreamstraightServerAbortError()

                    logger.warning(
                        "[streamstraight-server] connect attempt failed stream_id=%s attempt=%s/%s error=%s aborted=%s",
                        stream_options.stream_id,
                        index + 1,
                        num_retries + 1,
                        exc,
                        self._connect_aborted,
                    )

                    if index == num_retries:
                        if isinstance(exc, StreamstraightServerError):
                            raise exc
                        raise StreamstraightServerError(str(exc)) from exc

                    backoff_seconds = (retry_delay_ms / 1000) * (2**index)
                    await asyncio.sleep(backoff_seconds)
                finally:
                    self._connect_waiter = None

    async def _cleanup_socket(self) -> None:
        # Capture socket reference and clear it BEFORE calling disconnect
        # This prevents recursive disconnect via on_disconnect handler
        socket = self._socket
        self._socket = None
        self._stream_options = None
        self._loop = None
        self._connect_waiter = None

        if socket:
            try:
                await socket.disconnect()
            except Exception:  # pragma: no cover - best effort cleanup
                pass

    def _register_handlers(self) -> None:
        if not self._socket:
            return

        # Capture current socket reference for handlers
        current_socket = self._socket

        async def on_connect() -> None:
            logger.debug("[streamstraight-server] connected")
            if self._connect_waiter and not self._connect_waiter.done():
                self._connect_waiter.set_result(None)

        async def on_disconnect() -> None:
            logger.debug("[streamstraight-server] disconnected")
            # Only call disconnect if this socket is still the current one
            # Prevents recursive disconnect during cleanup
            if self._socket is current_socket:
                await self.disconnect()

        async def on_connect_error(error: Any) -> None:
            message = str(error) if error is not None else "unknown connect error"
            logger.error("[streamstraight-server] connect_error %s", error)
            # Always print to stderr so users see connection errors even without logging configured
            print(f"[streamstraight-server] Connection error: {message}", file=sys.stderr)

            if self._connect_waiter and not self._connect_waiter.done():
                self._connect_waiter.set_exception(_ConnectionAttemptError(message))
            await self._cleanup_socket()

        async def on_runtime_error(payload: Dict[str, Any]) -> None:
            logger.error(
                "[streamstraight-server] %s %s",
                ConnectionServerToClientEvents.ERROR,
                payload,
            )
            message = payload.get("message") if isinstance(payload, Mapping) else None
            await self.disconnect(StreamstraightServerError(message or "connection error"))

        async def on_error(payload: StreamErrorPayload) -> None:
            logger.error(
                "[streamstraight-server] %s %s",
                ProducerServerToClientEvents.ERROR,
                payload,
            )
            await self.disconnect(
                StreamstraightServerError(payload.get("message", "producer error")),
            )

        async def on_info(payload: StreamInfoPayload) -> None:
            logger.debug(
                "[streamstraight-server] %s %s",
                ProducerServerToClientEvents.INFO,
                payload,
            )

        self._socket.on("connect", on_connect)
        self._socket.on("disconnect", on_disconnect)
        self._socket.on("connect_error", on_connect_error)
        self._socket.on(
            ConnectionServerToClientEvents.ERROR,
            on_runtime_error,
        )
        self._socket.on(ProducerServerToClientEvents.ERROR, on_error)
        self._socket.on(ProducerServerToClientEvents.INFO, on_info)

    async def _send_chunk(self, data: str) -> None:
        if not self._socket or not self._socket.connected:
            raise StreamstraightServerError("socket not initialized")

        seq = self._seq
        self._seq += 1

        logger.debug("[streamstraight-server] emitting chunk seq=%s size=%s", seq, len(data))

        payload = {"seq": seq, "data": data}

        try:
            await self._socket.emit(ProducerClientToServerEvents.CHUNK, payload)
        except Exception as exc:
            raise StreamstraightServerError(str(exc)) from exc

    async def _finalize_stream(
        self, start_seq: int, *, reason: StreamEndReason = "completed"
    ) -> None:
        """Send END frame to finalize the stream."""
        # If socket was disconnected due to an error, raise that error
        if self._disconnect_error:
            raise self._disconnect_error

        end_seq = self._seq
        chunk_count = end_seq - start_seq

        await self._send_end(chunk_count, reason=reason)

    async def _send_end(
        self,
        chunk_count: int,
        *,
        reason: StreamEndReason = "completed",
    ) -> None:
        if not self._socket or not self._socket.connected:
            raise StreamstraightServerError("socket not initialized")

        last_seq = max(self._seq - 1, 0)

        end_payload: StreamEndNotification = {
            "reason": reason,
            "lastSeq": last_seq,
        }

        logger.info(
            "[streamstraight-server] emitting end frame last_seq=%s chunks=%s reason=%s",
            last_seq,
            chunk_count,
            reason,
        )

        try:
            # Use call() instead of emit() to wait for server acknowledgment
            # This ensures the END frame is processed before we disconnect
            ack: StreamEndAck = await self._socket.call(
                ProducerClientToServerEvents.END, end_payload, timeout=5.0
            )
            if not ack.get("success"):
                error = ack.get("error", "unknown error")
                logger.error("[streamstraight-server] server failed to finalize stream: %s", error)
        except Exception as exc:
            raise StreamstraightServerError(str(exc)) from exc

    async def _send_iterable(self, source: AsyncIterable[C] | Any) -> None:
        # Check if we have a disconnect error first to provide better context
        if self._disconnect_error:
            raise StreamstraightServerError(
                f"cannot start stream iteration: {self._disconnect_error}"
            ) from self._disconnect_error
        if not self._socket or not self._socket.connected:
            raise StreamstraightServerError("socket not connected in _send_iterable")
        if not self._stream_options:
            raise StreamstraightServerError("stream options not initialized in _send_iterable")

        encoder = self._stream_options.encoder or _default_encode_chunk

        logger.info(
            "[streamstraight-server] starting stream emission stream_id=%s",
            self._stream_options.stream_id,
        )

        start_seq = self._seq
        self._streaming = True
        try:
            async for chunk in ensure_async_iterable(source):
                encoded_chunk = encoder(chunk)
                if not isinstance(encoded_chunk, str):
                    raise StreamstraightServerError("encoder must return a string")
                if encoded_chunk == "":
                    continue
                logger.debug(
                    "[streamstraight-server] queueing chunk seq=%s length=%s",
                    self._seq,
                    len(encoded_chunk),
                )
                await self._send_chunk(encoded_chunk)

            await self._finalize_stream(start_seq, reason="completed")
        except Exception as exc:
            stream_error = (
                exc
                if isinstance(exc, StreamstraightServerError)
                else StreamstraightServerError(str(exc))
            )
            stream_id = self._stream_options.stream_id if self._stream_options else "<unknown>"
            logger.exception(
                "[streamstraight-server] stream emission failed stream_id=%s error=%s",
                stream_id,
                stream_error,
            )

            # Always send END frame even on error, so stream is properly closed
            try:
                await self._finalize_stream(start_seq, reason="producer-error")
            except Exception as finalize_error:
                logger.error(
                    "[streamstraight-server] failed to send END frame on error: %s",
                    finalize_error,
                )

            await self.disconnect(stream_error)

            if stream_error is exc:
                raise
            raise stream_error from exc
        finally:
            self._streaming = False

    async def stream(self, source: AsyncIterable[C] | Any) -> None:
        # Check if we have a disconnect error first to provide better context
        if self._disconnect_error:
            raise StreamstraightServerError(
                f"cannot call stream(): {self._disconnect_error}"
            ) from self._disconnect_error
        if not self._socket or not self._socket.connected:
            raise StreamstraightServerError("socket not connected in stream()")
        if not self._stream_options:
            raise StreamstraightServerError("stream options not initialized in stream()")

        logger.info(
            "[streamstraight-server] streaming payload stream_id=%s",
            self._stream_options.stream_id,
        )
        try:
            await self._send_iterable(source)
        except Exception:
            # _send_iterable already disconnects and wraps the error; just propagate.
            raise
        else:
            if not self._stream_options.keep_open:
                logger.debug("[streamstraight-server] keep_open disabled; disconnecting")
                await self.disconnect()

    async def disconnect(self, error: StreamstraightServerError | None = None) -> None:
        self._connect_aborted = True
        final_error = error or StreamstraightServerError("socket disconnected")
        # Always store the disconnect error so we can provide better error messages
        self._disconnect_error = final_error

        # Log disconnect with streaming context for debugging
        stream_id = self._stream_options.stream_id if self._stream_options else None
        if self._streaming:
            logger.warning(
                (
                    "[streamstraight-server] disconnect during active streaming "
                    "stream_id=%s seq=%s error=%s"
                ),
                stream_id,
                self._seq,
                final_error,
            )
        elif stream_id and self._seq == 0:
            logger.info(
                (
                    "[streamstraight-server] disconnect before streaming started "
                    "stream_id=%s error=%s"
                ),
                stream_id,
                final_error,
            )

        if self._connect_waiter and not self._connect_waiter.done():
            self._connect_waiter.set_exception(StreamstraightServerAbortError())
        await self._cleanup_socket()

    def stream_writer(self) -> "StreamWriter[C]":
        return StreamWriter(self)


class StreamWriter(Generic[C]):
    def __init__(self, server: StreamstraightServer[C]) -> None:
        self._server = server
        self._start_seq = 0
        self._closed = False
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> "StreamWriter[C]":
        # Check if we have a disconnect error first to provide better context
        if self._server._disconnect_error:
            raise StreamstraightServerError(
                f"cannot enter stream_writer context: {self._server._disconnect_error}"
            ) from self._server._disconnect_error
        if not self._server._socket or not self._server._socket.connected:
            raise StreamstraightServerError("socket not connected in stream_writer.__aenter__")
        if not self._server._stream_options:
            raise StreamstraightServerError(
                "stream options not initialized in stream_writer.__aenter__"
            )

        # Capture the starting sequence number for this writer session
        self._start_seq = self._server._seq
        self._closed = False
        self._server._streaming = True
        return self

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        reason: StreamEndReason = "completed" if exc_type is None else "producer-error"
        self._server._streaming = False
        try:
            # Shield close so cancellation of the surrounding task does not skip socket cleanup.
            await asyncio.shield(self.close(reason=reason))
        except asyncio.CancelledError:
            # Propagate cancellation but make sure the close coroutine keeps running in the background.
            logger.warning(
                "[streamstraight-server] writer close interrupted by cancellation; cleanup continues"
            )
            raise
        except Exception:
            if exc_type is None:
                raise
            logger.exception("[streamstraight-server] writer close failed during context exit")

    async def send(self, chunk: C) -> None:
        if self._closed:
            raise StreamstraightServerError("stream writer already closed")

        # Check if we have a disconnect error first to provide better context
        if self._server._disconnect_error:
            raise StreamstraightServerError(
                f"cannot send chunk: {self._server._disconnect_error}"
            ) from self._server._disconnect_error
        if not self._server._socket or not self._server._socket.connected:
            raise StreamstraightServerError("socket not connected in stream_writer.send")
        if not self._server._stream_options:
            raise StreamstraightServerError("stream options not initialized in stream_writer.send")

        # Use encoder directly from server's stream options
        encoder = self._server._stream_options.encoder or _default_encode_chunk
        encoded_chunk = encoder(chunk)
        if not isinstance(encoded_chunk, str):
            raise StreamstraightServerError("encoder must return a string")
        if encoded_chunk == "":
            return

        async with self._lock:
            if self._closed:
                raise StreamstraightServerError("stream writer already closed")
            await self._server._send_chunk(encoded_chunk)

    async def close(self, *, reason: StreamEndReason = "completed") -> None:
        async with self._lock:
            if self._closed:
                return
            self._closed = True

        try:
            await self._server._finalize_stream(self._start_seq, reason=reason)
        finally:
            options = self._server._stream_options
            if not options or not options.keep_open:
                try:
                    await asyncio.shield(self._server.disconnect())
                except asyncio.CancelledError:
                    logger.warning(
                        "[streamstraight-server] disconnect cancelled; forcing close to continue",
                    )
                    raise
                except Exception:
                    logger.exception(
                        "[streamstraight-server] disconnect failed after closing stream",
                    )
