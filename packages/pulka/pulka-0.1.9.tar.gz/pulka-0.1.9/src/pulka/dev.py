"""Development tools and scripts for Pulka."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import subprocess
import sys
from collections.abc import Iterable, Iterator, Sequence
from io import TextIOWrapper
from pathlib import Path
from typing import Any

from .render.style_resolver import StyleComponents

_MIN_ARG_COUNT = 2  # Minimum number of arguments required for the script
_MYPY_TARGETS = ["src/pulka/core", "src/pulka/render", "src/pulka/session.py"]


def _run_cmd(cmd: list[str], description: str = "") -> int:
    """Run a command and return its exit code."""
    if description:
        print(f"🔄 {description}")

    try:
        subprocess.run(cmd, check=True, cwd=Path(__file__).parent.parent.parent)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print(f"❌ Command not found: {' '.join(cmd)}")
        return 1


def lint() -> None:
    """Run ruff linter."""
    print("📋 Running ruff linter...")
    exit_code = _run_cmd(["uv", "run", "ruff", "check", "."])
    if exit_code == 0:
        print("✅ Lint check passed!")
    sys.exit(exit_code)


def format() -> None:
    """Format code with ruff."""
    print("🎨 Formatting code with ruff...")
    exit_code = _run_cmd(["uv", "run", "ruff", "format", "."])
    if exit_code == 0:
        print("✅ Code formatted!")
    sys.exit(exit_code)


def lint_imports() -> None:
    """Run import-linter to enforce architecture layering."""
    print("🏗️ Checking import contracts...")
    exit_code = _run_cmd(["uv", "run", "lint-imports"])
    if exit_code == 0:
        print("✅ Import contracts satisfied!")
    sys.exit(exit_code)


def typecheck() -> None:
    """Run mypy in strict mode over the core/render/session packages."""
    print("🧾 Running mypy type checks...")
    exit_code = _run_cmd(["uv", "run", "mypy", "--config-file", "mypy.ini", *_MYPY_TARGETS])
    if exit_code == 0:
        print("✅ Type checks passed!")
    sys.exit(exit_code)


def test() -> None:
    """Run tests."""
    print("🧪 Running tests...")
    exit_code = _run_cmd(["uv", "run", "python", "-m", "pytest", "--tb=short"])
    if exit_code == 0:
        print("✅ All tests passed!")
    sys.exit(exit_code)


def check() -> None:
    """Run all quality checks (lint + format + import contracts + types + tests)."""
    print("🔍 Running Pulka development checks...")

    # Run lint check
    print("\n📋 1. Running ruff linter...")
    exit_code = _run_cmd(["uv", "run", "ruff", "check", "."])
    if exit_code != 0:
        sys.exit(exit_code)

    # Check formatting
    print("\n🎨 2. Checking ruff formatting...")
    exit_code = _run_cmd(["uv", "run", "ruff", "format", "--check", "--diff", "."])
    if exit_code != 0:
        print("❌ Code is not properly formatted. Run 'pulka-format' to fix.")
        sys.exit(exit_code)

    # Check architecture import contracts
    print("\n🏗️ 3. Checking import contracts...")
    exit_code = _run_cmd(["uv", "run", "lint-imports"])
    if exit_code != 0:
        print("❌ Import contracts failed.")
        print("Run 'uv run python -m pulka.dev lint-imports' for details.")
        sys.exit(exit_code)

    # Run mypy strict checks
    print("\n🧾 4. Running mypy type checks...")
    exit_code = _run_cmd(["uv", "run", "mypy", "--config-file", "mypy.ini", *_MYPY_TARGETS])
    if exit_code != 0:
        print("❌ Mypy type checks failed.")
        print("Run 'uv run python -m pulka.dev typecheck' for details.")
        sys.exit(exit_code)

    # Run tests
    print("\n🧪 5. Running tests...")
    exit_code = _run_cmd(["uv", "run", "python", "-m", "pytest", "--tb=short"])
    if exit_code != 0:
        sys.exit(exit_code)

    print("\n✅ All checks passed! Ready to commit.")


def fix() -> None:
    """Auto-fix issues and run tests."""
    print("🔧 Auto-fixing Pulka code issues...")

    # Format code
    print("\n🎨 1. Running ruff formatter...")
    exit_code = _run_cmd(["uv", "run", "ruff", "format", "."])
    if exit_code != 0:
        sys.exit(exit_code)

    # Fix linting issues
    print("\n📋 2. Running ruff auto-fixes...")
    exit_code = _run_cmd(["uv", "run", "ruff", "check", "--fix", "."])
    if exit_code != 0:
        sys.exit(exit_code)

    # Run tests to verify
    print("\n🧪 3. Running tests to verify fixes...")
    exit_code = _run_cmd(["uv", "run", "python", "-m", "pytest", "--tb=short", "-x"])
    if exit_code != 0:
        print("❌ Tests failed after fixes. Please review the changes.")
        sys.exit(exit_code)

    print("\n✅ Auto-fixes applied! Review changes before committing.")


def inspect_style(argv: Sequence[str] | None = None) -> None:
    """Pretty-print ``render_line_styles`` recorder events."""

    parser = argparse.ArgumentParser(description="Inspect recorded render styles")
    parser.add_argument("recording", help="Path to the recorder JSONL or JSONL.zst file")
    parser.add_argument(
        "--component",
        "-c",
        help="Filter events to a specific component (e.g. table_control)",
    )
    parser.add_argument(
        "--max-events",
        "-n",
        type=int,
        default=None,
        help="Limit the number of events displayed",
    )
    args = parser.parse_args(list(argv) if argv is not None else sys.argv[2:])

    path = Path(args.recording).expanduser()
    if not path.exists():
        print(f"❌ Recording not found: {path}")
        sys.exit(1)

    try:
        events = list(
            _iter_render_style_events(
                path,
                component_filter=args.component,
                limit=args.max_events,
            )
        )
    except RuntimeError as exc:
        print(f"❌ {exc}")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"❌ Failed to parse recording: {exc}")
        sys.exit(1)

    if not events:
        print("No render_line_styles events found.")
        sys.exit(0)

    for event in events:
        payload = event.get("payload", {})
        component = payload.get("component", "<unknown>")
        theme_epoch = payload.get("theme_epoch")
        step_index = event.get("step_index")
        header = f"Step {step_index} — component {component}"
        if theme_epoch is not None:
            header = f"{header} (theme_epoch={theme_epoch})"
        print(header)

        for line in payload.get("lines", []):
            line_index = line.get("line_index")
            plain_text = line.get("plain_text", "")
            print(f"  Line {line_index}: {plain_text!r}")
            for segment in line.get("segments", []):
                classes = segment.get("classes") or []
                comp = StyleComponents(
                    foreground=segment.get("foreground"),
                    background=segment.get("background"),
                    extras=tuple(segment.get("extras") or ()),
                )
                extras = ", ".join(comp.extras) if comp.extras else "-"
                style_str = comp.to_prompt_toolkit()
                ansi_prefix = comp.to_ansi_prefix()
                text = segment.get("text", "")
                print(f"    classes: {', '.join(classes) or '-'}")
                print(f"      text: {text!r}")
                print(
                    "      fg="
                    f"{comp.foreground or 'default'} "
                    f"bg={comp.background or 'default'} "
                    f"extras={extras}"
                )
                if style_str:
                    print(f"      prompt_toolkit: {style_str}")
                if ansi_prefix:
                    print(f"      ansi_prefix: {ansi_prefix}")


def _iter_render_style_events(
    path: Path,
    *,
    component_filter: str | None,
    limit: int | None,
) -> Iterator[dict[str, Any]]:
    count = 0
    for event in _iter_recorder_events(path):
        if event.get("type") != "render_line_styles":
            continue
        payload = event.get("payload", {})
        if component_filter and payload.get("component") != component_filter:
            continue
        yield event
        count += 1
        if limit is not None and count >= limit:
            break


def _iter_recorder_events(path: Path) -> Iterable[dict[str, Any]]:
    if path.suffix == ".zst" or path.name.endswith(".zst"):
        zstd = _maybe_import_zstandard()
        if zstd is None:
            raise RuntimeError(
                "zstandard is required to read compressed recordings (pip install zstandard)"
            )
        with path.open("rb") as fh:
            reader = zstd.ZstdDecompressor().stream_reader(fh)
            text_stream = TextIOWrapper(reader, encoding="utf-8")
            for line in text_stream:
                if line.strip():
                    yield json.loads(line)
            reader.close()
    else:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    yield json.loads(line)


def _maybe_import_zstandard() -> Any | None:
    spec = importlib.util.find_spec("zstandard")
    if spec is None:
        return None
    return importlib.import_module("zstandard")


if __name__ == "__main__":
    if len(sys.argv) < _MIN_ARG_COUNT:
        print("Usage: python -m pulka.dev <command>")
        print("Commands: lint, format, lint-imports, typecheck, test, check, fix, inspect-style")
        sys.exit(1)

    command = sys.argv[1]
    if command == "lint":
        lint()
    elif command == "format":
        format()
    elif command == "lint-imports":
        lint_imports()
    elif command == "typecheck":
        typecheck()
    elif command == "test":
        test()
    elif command == "check":
        check()
    elif command == "fix":
        fix()
    elif command == "inspect-style":
        inspect_style(sys.argv[2:])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
