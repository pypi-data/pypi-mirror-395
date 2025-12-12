from __future__ import annotations

import pytest

from streamstraight_server.constants import (
    DEFAULT_BASE_URL,
    PackageNotFoundError,
    get_base_url,
    get_package_version,
)


def _clear_caches() -> None:
    for func in (get_base_url, get_package_version):
        cache_clear = getattr(func, "cache_clear", None)
        if callable(cache_clear):
            cache_clear()


def test_base_url_defaults(clear_env):
    _clear_caches()
    assert get_base_url() == DEFAULT_BASE_URL


def test_base_url_env(monkeypatch, clear_env):
    monkeypatch.setenv("STREAMSTRAIGHT_API_BASE_URL", "https://staging.example.com")
    _clear_caches()
    assert get_base_url() == "https://staging.example.com"


def test_package_version_metadata(monkeypatch, clear_env):
    monkeypatch.setattr(
        "streamstraight_server.constants.version",
        lambda _dist: "1.2.3",
    )
    _clear_caches()
    assert get_package_version() == "1.2.3"


def test_package_version_fallback(monkeypatch, clear_env):
    def _raise(_dist: str) -> str:
        raise PackageNotFoundError

    monkeypatch.setattr("streamstraight_server.constants.version", _raise)
    _clear_caches()
    assert get_package_version() == "0.0.0-dev"


@pytest.fixture()
def clear_env(monkeypatch):
    monkeypatch.delenv("STREAMSTRAIGHT_API_BASE_URL", raising=False)
    _clear_caches()
    yield
    monkeypatch.delenv("STREAMSTRAIGHT_API_BASE_URL", raising=False)
    _clear_caches()
