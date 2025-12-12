import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any, Dict, List, Optional, Tuple

import pytest

from streamstraight_server import ServerOptionsDict, StreamOptionsDict
from streamstraight_server.constants import get_package_version
from streamstraight_server.protocol import (
    ProducerClientToServerEvents,
    ProducerServerToClientEvents,
    StreamEndAck,
)
from streamstraight_server.server import (
    StreamstraightServer,
    StreamstraightServerAbortError,
    StreamstraightServerError,
)


class FakeAsyncClient:
    def __init__(self, end_ack: Optional[StreamEndAck] = None) -> None:
        self.connected = False
        self.emitted: List[Tuple[str, Dict[str, Any]]] = []
        self.called: List[Tuple[str, Dict[str, Any]]] = []
        self.disconnect_calls = 0
        self.connect_args: Dict[str, Any] | None = None
        self.connect_attempts = 0
        self.connect_side_effects: List[Optional[Exception]] = []
        self.connect_block: Optional[asyncio.Event] = None
        self.connect_error_events: List[Optional[Exception]] = []
        self._handlers: Dict[str, List[Any]] = {}
        self._ack_waiters: Dict[int, asyncio.Future[Dict[str, Any]]] = {}
        self.end_ack = end_ack or {"success": True, "endRedisId": "redis-end-123"}

    def on(self, event: str, handler):
        """Register event handler - matches socketio.AsyncClient.on() API."""
        self._handlers.setdefault(event, []).append(handler)
        return handler

    async def connect(self, url: str, auth, headers):
        self.connect_attempts += 1
        self.connect_args = {
            "url": url,
            "auth": auth,
            "headers": headers,
        }
        if self.connect_block is not None:
            block = self.connect_block
            if not block.is_set():
                await block.wait()
            self.connect_block = None

        if self.connect_side_effects:
            effect = self.connect_side_effects.pop(0)
            if effect is not None:
                raise effect

        error_event: Optional[Exception] = None
        if self.connect_error_events:
            error_event = self.connect_error_events.pop(0)
        if error_event is not None:
            for handler in self._handlers.get("connect_error", []):
                await handler(error_event)
            self.connected = False
            return

        self.connected = True
        # Fire all connect handlers (matches socketio.on("connect", handler) behavior)
        for handler in self._handlers.get("connect", []):
            await handler()

    async def emit(self, event: str, payload: Dict[str, Any]):
        self.emitted.append((event, payload))
        if event == ProducerClientToServerEvents.CHUNK:
            await asyncio.sleep(0)
            ack_payload = {"seq": payload["seq"], "redisId": f"redis-{payload['seq']}"}
            for handler in self._handlers.get(ProducerServerToClientEvents.ACK, []):
                await handler(ack_payload)
            waiter = self._ack_waiters.pop(payload["seq"], None)
            if waiter and not waiter.done():
                waiter.set_result(ack_payload)
        if event == ProducerClientToServerEvents.END:
            await asyncio.sleep(0)
            seq = payload.get("lastSeq", 0) + 1
            ack_payload = {"seq": seq, "redisId": payload.get("redisId", f"redis-{seq}")}
            for handler in self._handlers.get(ProducerServerToClientEvents.ACK, []):
                await handler(ack_payload)
            waiter = self._ack_waiters.pop(seq, None)
            if waiter and not waiter.done():
                waiter.set_result(ack_payload)

    async def disconnect(self):
        self.disconnect_calls += 1
        was_connected = self.connected
        self.connected = False
        # Fire disconnect handlers only if we were actually connected
        if was_connected:
            for handler in self._handlers.get("disconnect", []):
                await handler()

    async def wait_for_ack(self, seq: int, timeout: float = 5.0):
        waiter = asyncio.get_running_loop().create_future()
        self._ack_waiters[seq] = waiter
        return await asyncio.wait_for(waiter, timeout=timeout)

    async def call(self, event: str, payload: Dict[str, Any], timeout: float = 5.0) -> StreamEndAck:
        """Emit event and wait for acknowledgment - matches socketio.AsyncClient.call() API."""
        self.called.append((event, payload))
        if event == ProducerClientToServerEvents.END:
            await asyncio.sleep(0)
            return self.end_ack
        raise NotImplementedError(f"call() not implemented for event: {event}")


@pytest.fixture(autouse=True)
def patch_socketio(monkeypatch):
    fake_client = FakeAsyncClient()
    monkeypatch.setattr(
        "streamstraight_server.server.socketio.AsyncClient",
        lambda: fake_client,
    )
    return fake_client


@pytest.mark.asyncio
async def test_connect_uses_auth_headers(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc", base_url="http://example"))
    await server.connect(StreamOptionsDict(stream_id="stream-1"))

    assert fake_client.connect_args is not None
    assert fake_client.connect_args["url"] == "http://example"
    assert fake_client.connect_args["auth"]["streamId"] == "stream-1"
    assert fake_client.connect_args["auth"]["sdkVersion"] == get_package_version()
    assert fake_client.connect_args["headers"]["Authorization"] == "Bearer abc"


@pytest.mark.asyncio
async def test_connect_retries_before_success(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    fake_client.connect_side_effects = [RuntimeError("nope")]

    server = StreamstraightServer(
        ServerOptionsDict(api_key="abc", connect_retry_delay_ms=0, base_url="http://example"),
    )

    await server.connect(StreamOptionsDict(stream_id="retry-stream"))

    assert fake_client.connect_attempts == 2
    assert fake_client.connected is True


@pytest.mark.asyncio
async def test_connect_retries_when_connect_error_event_emitted(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    fake_client.connect_error_events = [RuntimeError("handshake failed"), None]

    server = StreamstraightServer(
        ServerOptionsDict(api_key="abc", connect_retry_delay_ms=0, base_url="http://example"),
    )

    await server.connect(StreamOptionsDict(stream_id="retry-stream"))

    assert fake_client.connect_attempts == 2
    assert fake_client.connected is True


@pytest.mark.asyncio
async def test_connect_attempts_once_when_no_retries(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    fake_client.connect_side_effects = [RuntimeError("fail")]

    server = StreamstraightServer(
        ServerOptionsDict(
            api_key="abc",
            num_connect_retries=0,
            connect_retry_delay_ms=0,
        ),
    )

    with pytest.raises(StreamstraightServerError, match="fail"):
        await server.connect(StreamOptionsDict(stream_id="single-attempt"))

    assert fake_client.connect_attempts == 1
    assert fake_client.connected is False


@pytest.mark.asyncio
async def test_connect_raises_after_retry_exhaustion(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    fake_client.connect_side_effects = [RuntimeError("fail"), RuntimeError("fail again")]

    server = StreamstraightServer(
        ServerOptionsDict(
            api_key="abc",
            base_url="http://example",
            num_connect_retries=1,
            connect_retry_delay_ms=0,
        ),
    )

    with pytest.raises(StreamstraightServerError, match="fail again"):
        await server.connect(StreamOptionsDict(stream_id="retry-stream"))

    assert fake_client.connect_attempts == 2
    assert fake_client.connected is False


@pytest.mark.asyncio
async def test_connect_aborts_when_disconnect_called(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    fake_client.connect_block = asyncio.Event()

    server = StreamstraightServer(
        ServerOptionsDict(
            api_key="abc",
            base_url="http://example",
            num_connect_retries=2,
            connect_retry_delay_ms=0,
        )
    )

    connect_task = asyncio.create_task(server.connect(StreamOptionsDict(stream_id="abort-stream")))
    await asyncio.sleep(0)
    await server.disconnect()
    fake_client.connect_block.set()

    with pytest.raises(StreamstraightServerAbortError):
        await connect_task

    assert fake_client.connect_attempts == 1
    assert fake_client.connected is False


@pytest.mark.asyncio
async def test_stream_sends_chunks_and_end(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    async def generate() -> AsyncIterator[str]:
        yield "first"
        yield "second"

    await server.connect(StreamOptionsDict(stream_id="demo", encoder=lambda value: value))
    await server.stream(generate())

    chunk_events = [
        event for event in fake_client.emitted if event[0] == ProducerClientToServerEvents.CHUNK
    ]
    assert len(chunk_events) == 2

    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.disconnect_calls == 1


@pytest.mark.asyncio
async def test_stream_default_encoder_handles_model_dump_json(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    class DummyModel:
        def __init__(self, text: str) -> None:
            self.text = text

        def model_dump_json(self) -> str:
            return json.dumps({"text": self.text})

    async def generate() -> AsyncIterator[DummyModel]:
        yield DummyModel("hello")

    await server.connect(StreamOptionsDict(stream_id="demo"))
    await server.stream(generate())

    first_event = fake_client.emitted[0]
    assert first_event[0] == ProducerClientToServerEvents.CHUNK
    assert first_event[1]["data"] == json.dumps({"text": "hello"})


@pytest.mark.asyncio
async def test_stream_disconnects_when_source_errors(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    async def generate() -> AsyncIterator[str]:
        yield "first"
        raise RuntimeError("explode")

    await server.connect(StreamOptionsDict(stream_id="demo", encoder=lambda value: value))

    with pytest.raises(StreamstraightServerError, match="explode"):
        await server.stream(generate())

    # CRITICAL: Should send END frame with reason="producer-error" even when source errors
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.called[0][1]["reason"] == "producer-error"
    assert fake_client.disconnect_calls == 1
    assert fake_client.connected is False


@pytest.mark.asyncio
async def test_stream_writer_context_sends_chunks_and_end(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    await server.connect(StreamOptionsDict(stream_id="writer", encoder=lambda value: value))

    async with server.stream_writer() as writer:
        await writer.send("hello")

    chunk_events = [
        event for event in fake_client.emitted if event[0] == ProducerClientToServerEvents.CHUNK
    ]
    assert len(chunk_events) == 1
    assert chunk_events[0][1]["data"] == "hello"

    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.called[0][1]["reason"] == "completed"

    assert fake_client.disconnect_calls == 1
    assert fake_client.connected is False


@pytest.mark.asyncio
async def test_stream_writer_aborts_on_exception(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    await server.connect(StreamOptionsDict(stream_id="writer", encoder=lambda value: value))

    with pytest.raises(RuntimeError, match="boom"):
        async with server.stream_writer() as writer:
            await writer.send("chunk")
            raise RuntimeError("boom")

    # CRITICAL: Should send END frame with reason="producer-error" even when exception occurs
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.called[0][1]["reason"] == "producer-error"
    assert fake_client.disconnect_calls == 1
    assert fake_client.connected is False


@pytest.mark.asyncio
async def test_stream_writer_send_after_close_raises(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    await server.connect(StreamOptionsDict(stream_id="writer", encoder=lambda value: value))

    writer = server.stream_writer()
    await writer.__aenter__()
    await writer.close()

    with pytest.raises(StreamstraightServerError, match="already closed"):
        await writer.send("chunk")

    assert fake_client.disconnect_calls == 1


@pytest.mark.asyncio
async def test_stream_writer_reuses_existing_stream_options(patch_socketio):
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    await server.connect(StreamOptionsDict(stream_id="writer", encoder=lambda value: value))

    async with server.stream_writer() as writer:
        await writer.send("chunk")

    chunk_events = [
        event for event in fake_client.emitted if event[0] == ProducerClientToServerEvents.CHUNK
    ]
    assert len(chunk_events) == 1
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END


@pytest.mark.asyncio
async def test_stream_sends_end_frame_with_aborted_when_encoder_throws(patch_socketio):
    """CRITICAL: Ensure END frame with reason='aborted' is sent even when encoder throws."""
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    async def generate() -> AsyncIterator[str]:
        yield "first"
        yield "second"

    def bad_encoder(value: str) -> str:
        if value == "second":
            raise RuntimeError("encoder explosion")
        return value

    await server.connect(StreamOptionsDict(stream_id="demo", encoder=bad_encoder))

    with pytest.raises(StreamstraightServerError, match="encoder explosion"):
        await server.stream(generate())

    # Should send END frame with reason="producer-error" even when encoder throws
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.called[0][1]["reason"] == "producer-error"
    assert fake_client.disconnect_calls == 1


@pytest.mark.asyncio
async def test_stream_sends_end_frame_with_aborted_when_iterable_throws(patch_socketio):
    """CRITICAL: Ensure END frame with reason='aborted' is sent even when iterable throws."""
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    async def generate() -> AsyncIterator[str]:
        yield "first"
        raise RuntimeError("iterable explosion")

    await server.connect(StreamOptionsDict(stream_id="demo", encoder=lambda value: value))

    with pytest.raises(StreamstraightServerError, match="iterable explosion"):
        await server.stream(generate())

    # Should send END frame with reason="producer-error" even when iterable throws
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.called[0][1]["reason"] == "producer-error"
    assert fake_client.disconnect_calls == 1


@pytest.mark.asyncio
async def test_stream_sends_end_frame_with_completed_on_success(patch_socketio):
    """CRITICAL: Ensure END frame with reason='completed' is sent on successful stream."""
    fake_client: FakeAsyncClient = patch_socketio
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    async def generate() -> AsyncIterator[str]:
        yield "first"
        yield "second"

    await server.connect(StreamOptionsDict(stream_id="demo", encoder=lambda value: value))
    await server.stream(generate())

    # Should send END frame with reason="completed" on success
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.called[0][1]["reason"] == "completed"


@pytest.mark.asyncio
async def test_stream_writer_requires_stream_options():
    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    with pytest.raises(
        StreamstraightServerError,
        match="socket not connected in stream_writer.__aenter__",
    ):
        async with server.stream_writer():
            pass


@pytest.mark.asyncio
async def test_stream_writer_handles_disconnect_after_connect(monkeypatch):
    """Test that disconnection after connect() but before writer context gives clear error."""
    fake_client = FakeAsyncClient()
    monkeypatch.setattr("socketio.AsyncClient", lambda: fake_client)

    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))
    await server.connect(StreamOptionsDict(stream_id="test-stream"))

    # Simulate socket disconnecting after connect() returns
    await fake_client.disconnect()

    # Should get error indicating disconnect happened with context
    with pytest.raises(
        StreamstraightServerError,
        match="cannot enter stream_writer context: socket disconnected",
    ):
        async with server.stream_writer() as writer:
            await writer.send("test")


@pytest.mark.asyncio
async def test_stream_handles_disconnect_after_connect(monkeypatch):
    """Test that disconnection after connect() but before stream() gives clear error."""
    fake_client = FakeAsyncClient()
    monkeypatch.setattr("socketio.AsyncClient", lambda: fake_client)

    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))
    await server.connect(StreamOptionsDict(stream_id="test-stream"))

    # Simulate socket disconnecting after connect() returns
    await fake_client.disconnect()

    # Should get error indicating disconnect happened with context
    with pytest.raises(
        StreamstraightServerError,
        match="cannot call stream\\(\\): socket disconnected",
    ):
        async def gen():
            yield "test"

        await server.stream(gen())


@pytest.mark.asyncio
async def test_receives_successful_acknowledgment_when_stream_ends(monkeypatch):
    """Test that successful acknowledgment is received and processed."""
    success_ack: StreamEndAck = {"success": True, "endRedisId": "redis-123"}
    fake_client = FakeAsyncClient(end_ack=success_ack)
    monkeypatch.setattr("socketio.AsyncClient", lambda: fake_client)

    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    async def chunks():
        yield "chunk1"

    await server.connect(StreamOptionsDict(stream_id="ack-test"))
    await server.stream(chunks())

    # Should have called with END event
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END
    assert fake_client.called[0][1]["reason"] == "completed"

    # Should have disconnected after successful ack
    assert fake_client.disconnect_calls == 1


@pytest.mark.asyncio
async def test_logs_error_when_server_returns_error_acknowledgment(monkeypatch, caplog):
    """Test that error acknowledgment is logged but doesn't block stream completion."""
    error_ack: StreamEndAck = {"success": False, "error": "Stream finalization failed"}
    fake_client = FakeAsyncClient(end_ack=error_ack)
    monkeypatch.setattr("socketio.AsyncClient", lambda: fake_client)

    server = StreamstraightServer(ServerOptionsDict(api_key="abc"))

    async def chunks():
        yield "chunk1"

    await server.connect(StreamOptionsDict(stream_id="error-ack-test"))
    await server.stream(chunks())

    # Should have called with END event
    assert len(fake_client.called) == 1
    assert fake_client.called[0][0] == ProducerClientToServerEvents.END

    # Should still disconnect even with error ack
    assert fake_client.disconnect_calls == 1

    # Should log the error
    assert "server failed to finalize stream" in caplog.text
    assert "Stream finalization failed" in caplog.text
