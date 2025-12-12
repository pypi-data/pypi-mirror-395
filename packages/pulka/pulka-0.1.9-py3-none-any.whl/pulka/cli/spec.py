"""CLI helpers for spec-centric commands."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from ..synth import normalize_spec, parse_spec, spec_id
from ..synth.capsule import CapsuleError, from_capsule, is_capsule, to_capsule


def spec_main(argv: Sequence[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "normalize":
        spec = parse_spec(args.input)
        print(normalize_spec(spec))
        return 0

    if args.command == "to-capsule":
        spec = parse_spec(args.input)
        print(to_capsule(spec))
        return 0

    if args.command == "from-capsule":
        try:
            payload = from_capsule(args.input)
        except CapsuleError as exc:
            parser.error(str(exc))
            return 2
        print(payload.normalized)
        return 0

    if args.command == "id":
        normalized = _load_normalized(args.input)
        print(spec_id(normalized))
        return 0

    parser.error("unknown command")
    return 2


def _load_normalized(value: str) -> str:
    if is_capsule(value):
        payload = from_capsule(value)
        return payload.normalized
    spec = parse_spec(value)
    return normalize_spec(spec)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pulka spec", description="Spec utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    normalize_parser = subparsers.add_parser("normalize", help="Normalize a semi-compact spec")
    normalize_parser.add_argument("input", help="Semi-compact specification string")

    to_capsule_parser = subparsers.add_parser(
        "to-capsule", help="Convert semi-compact spec to capsule64"
    )
    to_capsule_parser.add_argument("input", help="Semi-compact specification string")

    from_capsule_parser = subparsers.add_parser(
        "from-capsule", help="Convert capsule64 to normalized spec"
    )
    from_capsule_parser.add_argument("input", help="Capsule64 string")

    id_parser = subparsers.add_parser("id", help="Print stable ID of a spec or capsule")
    id_parser.add_argument("input", help="Specification string or capsule64")

    return parser


__all__ = ["spec_main"]
