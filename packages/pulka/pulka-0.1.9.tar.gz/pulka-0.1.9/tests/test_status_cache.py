from __future__ import annotations

from time import monotonic
from unittest.mock import Mock

import pytest

from pulka.render.status_cache import StatusLineCache


class _DummyViewer:
    def __init__(self) -> None:
        self._status_dirty = True

    def is_status_dirty(self) -> bool:
        return self._status_dirty

    def mark_status_dirty(self) -> None:
        self._status_dirty = True

    def acknowledge_status_rendered(self) -> None:
        self._status_dirty = False


def test_status_cache_reuses_fragments(monkeypatch: pytest.MonkeyPatch) -> None:
    viewer = _DummyViewer()
    cache = StatusLineCache(viewer, resource_refresh_seconds=10.0)

    render_mock = Mock(return_value=[("", "status")])
    sample_mock = Mock(return_value=123)
    monkeypatch.setattr("pulka.render.status_cache.render_status_line", render_mock)
    monkeypatch.setattr("pulka.render.status_cache.sample_memory_usage", sample_mock)

    first = cache.get_status()
    assert first.recomputed is True
    assert render_mock.call_count == 1
    assert sample_mock.call_count == 1
    assert viewer.is_status_dirty() is False

    second = cache.get_status()
    assert second.recomputed is False
    assert render_mock.call_count == 1
    assert sample_mock.call_count == 1

    viewer.mark_status_dirty()
    third = cache.get_status()
    assert third.recomputed is True
    assert render_mock.call_count == 2
    assert sample_mock.call_count == 1


def test_status_cache_refreshes_resource(monkeypatch: pytest.MonkeyPatch) -> None:
    viewer = _DummyViewer()
    cache = StatusLineCache(viewer, resource_refresh_seconds=0.5)

    render_mock = Mock(return_value=[("", "status")])
    sample_mock = Mock(return_value=456)
    monkeypatch.setattr("pulka.render.status_cache.render_status_line", render_mock)
    monkeypatch.setattr("pulka.render.status_cache.sample_memory_usage", sample_mock)

    cache.get_status()
    assert render_mock.call_count == 1
    assert sample_mock.call_count == 1

    cache._resource_sample_at = monotonic() - 2  # force refresh
    viewer.acknowledge_status_rendered()
    refresher = cache.get_status()
    assert refresher.recomputed is True
    assert render_mock.call_count == 2
    assert sample_mock.call_count == 2
