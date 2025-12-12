"""Utility helpers for stream iteration."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterable, AsyncIterator, Iterable
from typing import TypeVar, Union

T = TypeVar("T")


async def ensure_async_iterable(
    source: Union[AsyncIterable[T], Iterable[T]],
) -> AsyncIterator[T]:
    if isinstance(source, AsyncIterable):
        async for item in source:
            yield item
        return

    if isinstance(source, Iterable):
        for item in source:
            yield item
            await asyncio.sleep(0)
        return

    raise TypeError("source must be Iterable or AsyncIterable")
