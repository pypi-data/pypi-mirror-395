from __future__ import annotations

import concurrent.futures as futures
import importlib
import importlib.util
import sys

import pytest


def test_jobs_import_does_not_create_thread_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    module_name = "pulka.core.jobs"
    original = sys.modules.pop(module_name, None)

    spec = importlib.util.find_spec(module_name)
    assert spec is not None and spec.loader is not None

    created: list[tuple[tuple[object, ...], dict[str, object]]] = []

    class _SentinelExecutor:
        # pragma: no cover - constructor only
        def __init__(self, *args: object, **kwargs: object) -> None:
            created.append((args, kwargs))

    monkeypatch.setattr(futures, "ThreadPoolExecutor", _SentinelExecutor)

    try:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        assert created == []
    finally:
        sys.modules.pop(module_name, None)
        if original is not None:
            sys.modules[module_name] = original
        else:
            importlib.import_module(module_name)
