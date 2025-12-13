from __future__ import annotations

from pulka.api import Runtime


def test_runtime_respects_env_job_workers(monkeypatch):
    monkeypatch.setenv("PULKA_JOB_WORKERS", "6")
    runtime = Runtime(load_entry_points=False)
    try:
        runner = runtime.job_runner
        assert getattr(runner, "_max_workers", None) == 6
    finally:
        runtime.close()
        monkeypatch.delenv("PULKA_JOB_WORKERS", raising=False)


def test_runtime_uses_config_job_workers(monkeypatch, tmp_path):
    config_path = tmp_path / "pulka.toml"
    config_path.write_text("[jobs]\nmax_workers = 7\n", encoding="utf-8")
    monkeypatch.delenv("PULKA_JOB_WORKERS", raising=False)
    monkeypatch.setenv("PULKA_CONFIG", str(config_path))
    runtime = Runtime(load_entry_points=False)
    try:
        runner = runtime.job_runner
        assert getattr(runner, "_max_workers", None) == 7
    finally:
        runtime.close()
        monkeypatch.delenv("PULKA_CONFIG", raising=False)
