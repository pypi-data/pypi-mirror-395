"""CLI command for materialising synthetic specs."""

from __future__ import annotations

import argparse
import tempfile
from collections.abc import Sequence
from pathlib import Path

from ..synth import normalize_spec, parse_spec
from ..synth.capsule import CapsuleError, from_capsule, is_capsule, to_capsule
from ..synth.materialize import materialize_spec
from .presets import (
    PRESET_ENV_VAR,
    PresetConfigError,
    PresetStore,
    load_preset_store,
)
from .progress import file_write_feedback

_FORMAT_HANDLERS = {
    "parquet": lambda frame, path: frame.write_parquet(path),
    "ipc": lambda frame, path: frame.write_ipc(path),
    "csv": lambda frame, path: frame.write_csv(path),
}


def generate_main(argv: Sequence[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        preset_store = load_preset_store()
    except PresetConfigError as exc:
        parser.error(str(exc))
        return 2

    if args.list_presets:
        _print_preset_listing(preset_store)
        return 0

    try:
        raw_input = _pick_input_source(args.input, args.preset, preset_store)
    except PresetResolutionError as exc:
        parser.error(str(exc))
        return 2

    try:
        spec, normalized = _load_spec_or_capsule(raw_input)
    except CapsuleError as exc:
        parser.error(str(exc))
        return 2
    frame = materialize_spec(spec, normalized)

    capsule = to_capsule(spec, normalized)

    handler = _FORMAT_HANDLERS[args.format]
    auto_open = args.out is None
    out_path = args.out or _temporary_output_path(args.format)

    noun = f"{args.format} file"
    with file_write_feedback(out_path, noun=noun):
        handler(frame, out_path)

    if auto_open:
        print(f"Capsule: {capsule}")
    else:
        print(f"Wrote {out_path} ({args.format})")
        print(f"Capsule: {capsule}")
    if not auto_open:
        return 0

    try:
        return _open_viewer(out_path)
    finally:
        out_path.unlink(missing_ok=True)


def _load_spec_or_capsule(value: str):
    if is_capsule(value):
        payload = from_capsule(value)
        return payload.spec, payload.normalized
    spec = parse_spec(value)
    normalized = normalize_spec(spec)
    return spec, normalized


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pulka generate",
        description="Materialise synthetic specs",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Semi-compact spec string or capsule64 (omit when using --preset)",
    )
    parser.add_argument("--preset", help="Name of a preset in the user config file")
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help=f"List configured presets (set {PRESET_ENV_VAR} to override the file location)",
    )
    parser.add_argument("--out", type=Path, help="Output file path")
    parser.add_argument(
        "--format",
        choices=sorted(_FORMAT_HANDLERS.keys()),
        default="parquet",
        help="Output format (default: parquet)",
    )
    return parser


def _temporary_output_path(fmt: str) -> Path:
    suffix = {
        "parquet": ".parquet",
        "ipc": ".ipc",
        "csv": ".csv",
    }[fmt]
    with tempfile.NamedTemporaryFile(prefix="pulka_synth_", suffix=suffix, delete=False) as tmp:
        return Path(tmp.name)


def _open_viewer(path: Path) -> int:
    from . import _run_classic

    return _run_classic([str(path)])


class PresetResolutionError(RuntimeError):
    """Raised when CLI preset usage is invalid."""


def _pick_input_source(
    input_value: str | None,
    preset_name: str | None,
    store: PresetStore,
) -> str:
    if input_value and preset_name:
        msg = "Provide either a spec/capsule or --preset, not both."
        raise PresetResolutionError(msg)
    if preset_name:
        preset = store.get(preset_name)
        if preset is None:
            msg = (
                f"Unknown preset '{preset_name}'. "
                f"Use --list-presets to see options or edit {store.path}"
            )
            raise PresetResolutionError(msg)
        return preset
    if input_value:
        return input_value
    msg = "Missing spec/capsule input. Pass a value or use --preset <name>."
    raise PresetResolutionError(msg)


def _print_preset_listing(store: PresetStore) -> None:
    path = store.path
    print("Available presets:")
    for name in sorted(store.presets):
        value = store.presets[name]
        try:
            spec, normalized = _load_spec_or_capsule(value)
            capsule = to_capsule(spec, normalized)
            display = capsule
        except CapsuleError as exc:
            display = f"(invalid: {exc})"
        print(f"- {name}: {display}")
    print(f"User overrides live at {path} (create/edit this file to customize presets).")


__all__ = ["generate_main"]
