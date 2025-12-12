"""Parser for the semi-compact synthetic dataset specification."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from zoneinfo import ZoneInfo

from .dtypes import DTypeParseError, parse_dtype
from .lexer import SpecLexer, SpecSyntaxError
from .normalize import to_decimal
from .types import (
    ColumnSpec,
    ExpressionColumnSpec,
    GeneratedColumnSpec,
    GeneratorKind,
    GeneratorSpec,
    Modifier,
    ModifierKind,
    SeasonComponent,
    Spec,
    StructFieldSpec,
)


@dataclass
class ParserConfig:
    """Configuration hooks for the parser."""

    allowed_row_suffixes: dict[str, int] = None

    def __post_init__(self) -> None:
        if self.allowed_row_suffixes is None:
            self.allowed_row_suffixes = {
                "k": 1_000,
                "m": 1_000_000,
                "g": 1_000_000_000,
                "t": 1_000_000_000_000,
            }


class SpecParser:
    """Hand-rolled parser for the semi-compact specification grammar."""

    def __init__(self, source: str, config: ParserConfig | None = None):
        self.lexer = SpecLexer(source)
        self.config = config or ParserConfig()

    def parse(self) -> Spec:
        rows = self._parse_row_header()
        columns = [self._parse_column()]
        while self.lexer.optional(";"):
            columns.append(self._parse_column())
        if not self.lexer.eof():
            raise SpecSyntaxError("unexpected trailing content", self.lexer.location())
        return Spec(rows=rows, columns=tuple(columns))

    def _parse_row_header(self) -> int:
        literal = self.lexer.consume_number_literal()
        multiplier = 1
        peek = self.lexer.peek()
        if peek and peek.lower() in self.config.allowed_row_suffixes:
            multiplier = self.config.allowed_row_suffixes[peek.lower()]
            self.lexer.advance()
        self.lexer.expect("r")
        rows_decimal = to_decimal(literal) * multiplier
        if rows_decimal <= 0:
            raise SpecSyntaxError("row count must be positive", self.lexer.location())
        if rows_decimal != rows_decimal.to_integral():
            raise SpecSyntaxError("row count must be an integer", self.lexer.location())
        rows = int(rows_decimal)
        self.lexer.expect("/")
        return rows

    def _parse_column(self) -> ColumnSpec:
        name = self.lexer.consume_column_name()
        dtype = None
        if self.lexer.optional(":"):
            fragment = self._consume_dtype_annotation()
            try:
                dtype = parse_dtype(fragment)
            except DTypeParseError as exc:
                raise SpecSyntaxError(str(exc), self.lexer.location()) from exc
        self.lexer.expect("=")
        if self.lexer.optional("@"):
            expression = self._parse_expression()
            return ColumnSpec(
                name=name,
                dtype=dtype,
                definition=ExpressionColumnSpec(expression=expression),
            )
        generator = self._parse_generator()
        modifiers = []
        while True:
            modifier = self._maybe_parse_modifier()
            if modifier is None:
                break
            modifiers.append(modifier)
        return ColumnSpec(
            name=name,
            dtype=dtype,
            definition=GeneratedColumnSpec(generator=generator, modifiers=tuple(modifiers)),
        )

    def _consume_dtype_annotation(self) -> str:
        self.lexer.skip_ignored()
        start = self.lexer.index
        depth = 0
        while True:
            if self.lexer.index >= self.lexer.length:
                raise SpecSyntaxError("unterminated dtype annotation", self.lexer.location())
            ch = self.lexer.source[self.lexer.index]
            if ch == "=" and depth == 0:
                break
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                if depth == 0:
                    raise SpecSyntaxError(
                        "unexpected closing bracket in dtype annotation",
                        self.lexer.location(),
                    )
                depth -= 1
            self.lexer.advance()
        end = self.lexer.index
        fragment = self.lexer.source[start:end].strip()
        if not fragment:
            raise SpecSyntaxError("dtype annotation cannot be empty", self.lexer.location())
        return fragment

    def _parse_expression(self) -> str:
        self.lexer.expect("(")
        expr = self._consume_balanced("(", ")")
        return expr.strip()

    def _parse_generator(self) -> GeneratorSpec:
        ident = self.lexer.consume_identifier().lower()
        if ident == "normal":
            params = self._parse_numeric_args(2)
            return GeneratorSpec(
                kind=GeneratorKind.NORMAL,
                params={"mean": params[0], "stddev": params[1]},
            )
        if ident == "lognormal":
            params = self._parse_numeric_args(2)
            return GeneratorSpec(
                kind=GeneratorKind.LOGNORMAL,
                params={"mean": params[0], "stddev": params[1]},
            )
        if ident == "uniform":
            params = self._parse_numeric_args(2)
            return GeneratorSpec(
                kind=GeneratorKind.UNIFORM,
                params={"low": params[0], "high": params[1]},
            )
        if ident == "exp":
            params = self._parse_numeric_args(1)
            return GeneratorSpec(kind=GeneratorKind.EXP, params={"lambda": params[0]})
        if ident == "beta":
            params = self._parse_numeric_args(2)
            alpha, beta = params
            if alpha != alpha.to_integral() or beta != beta.to_integral():
                raise SpecSyntaxError(
                    "beta() expects integer alpha and beta",
                    self.lexer.location(),
                )
            return GeneratorSpec(
                kind=GeneratorKind.BETA,
                params={"alpha": int(alpha), "beta": int(beta)},
            )
        if ident == "laplace":
            params = self._parse_numeric_args(2)
            return GeneratorSpec(
                kind=GeneratorKind.LAPLACE,
                params={"mean": params[0], "scale": params[1]},
            )
        if ident == "weibull":
            params = self._parse_numeric_args(2)
            return GeneratorSpec(
                kind=GeneratorKind.WEIBULL,
                params={"shape": params[0], "scale": params[1]},
            )
        if ident == "poisson":
            (lam,) = self._parse_numeric_args(1)
            return GeneratorSpec(kind=GeneratorKind.POISSON, params={"lambda": lam})
        if ident == "gamma":
            shape, scale = self._parse_numeric_args(2)
            return GeneratorSpec(
                kind=GeneratorKind.GAMMA,
                params={"shape": shape, "scale": scale},
            )
        if ident == "zipf":
            (alpha,) = self._parse_numeric_args(1)
            return GeneratorSpec(kind=GeneratorKind.ZIPF, params={"alpha": alpha})
        if ident == "pareto":
            (alpha,) = self._parse_numeric_args(1)
            return GeneratorSpec(kind=GeneratorKind.PARETO, params={"alpha": alpha})
        if ident == "categorical":
            params = self._parse_numeric_args(1)
            count_decimal = params[0]
            if count_decimal != count_decimal.to_integral():
                raise SpecSyntaxError("categorical() expects an integer", self.lexer.location())
            return GeneratorSpec(
                kind=GeneratorKind.CATEGORICAL,
                params={"count": int(count_decimal)},
            )
        if ident == "enum":
            labels = self._parse_enum_labels()
            return GeneratorSpec(kind=GeneratorKind.ENUM, params={"labels": labels})
        if ident == "sequence":
            args = self._parse_maybe_empty_numeric_args()
            if len(args) == 0:
                start, step = Decimal(1), Decimal(1)
            elif len(args) == 1:
                start, step = args[0], Decimal(1)
            elif len(args) == 2:
                start, step = args
            else:
                raise SpecSyntaxError(
                    "sequence() accepts at most two arguments",
                    self.lexer.location(),
                )
            return GeneratorSpec(
                kind=GeneratorKind.SEQUENCE,
                params={"start": start, "step": step},
            )
        if ident == "date":
            start_date, end_date = self._parse_date_range()
            return GeneratorSpec(
                kind=GeneratorKind.DATE,
                params={"start": start_date, "end": end_date},
            )
        if ident == "bool":
            self._ensure_no_arguments("bool")
            return GeneratorSpec(kind=GeneratorKind.BOOLEAN, params={})
        if ident == "binary":
            length = self._parse_binary_length()
            return GeneratorSpec(kind=GeneratorKind.BINARY, params={"length": length})
        if ident == "datetime":
            params = self._parse_datetime_range()
            return GeneratorSpec(kind=GeneratorKind.DATETIME, params=params)
        if ident == "time":
            params = self._parse_time_bounds()
            return GeneratorSpec(kind=GeneratorKind.TIME, params=params)
        if ident == "duration":
            params = self._parse_duration_bounds()
            return GeneratorSpec(kind=GeneratorKind.DURATION, params=params)
        if ident == "list_int":
            params = self._parse_list_int_args()
            return GeneratorSpec(kind=GeneratorKind.LIST_INT, params=params)
        if ident == "list":
            element = self._parse_nested_generated_column("list")
            min_length, max_length = self._parse_list_bounds()
            return GeneratorSpec(
                kind=GeneratorKind.LIST,
                params={
                    "element": element,
                    "min_length": min_length,
                    "max_length": max_length,
                },
            )
        if ident == "array":
            element = self._parse_nested_generated_column("array")
            size = self._parse_array_size()
            return GeneratorSpec(
                kind=GeneratorKind.ARRAY,
                params={"element": element, "size": size},
            )
        if ident == "struct":
            fields = self._parse_struct_fields()
            return GeneratorSpec(kind=GeneratorKind.STRUCT, params={"fields": fields})
        if ident == "null":
            self._ensure_no_arguments("null")
            return GeneratorSpec(kind=GeneratorKind.NULL, params={})
        if ident == "ts":
            params = self._parse_ts()
            return GeneratorSpec(kind=GeneratorKind.TIME_SERIES, params=params)
        if ident == "enum[":
            raise SpecSyntaxError(
                "enum syntax should be enum[...], not enum([...)",
                self.lexer.location(),
            )
        raise SpecSyntaxError(f"unknown generator '{ident}'", self.lexer.location())

    def _ensure_no_arguments(self, name: str) -> None:
        args = self._parse_arguments("(", ")")
        if args:
            raise SpecSyntaxError(f"{name}() takes no arguments", self.lexer.location())

    def _parse_binary_length(self) -> int:
        (length_dec,) = self._parse_numeric_args(1)
        if length_dec != length_dec.to_integral():
            raise SpecSyntaxError("binary() expects an integer length", self.lexer.location())
        length = int(length_dec)
        if length <= 0:
            raise SpecSyntaxError("binary() length must be positive", self.lexer.location())
        return length

    def _parse_datetime_range(self) -> dict[str, object]:
        tokens = self._parse_arguments("[", "]")
        if len(tokens) < 2:
            raise SpecSyntaxError("datetime[...] requires start and end", self.lexer.location())
        start = self._parse_datetime_literal(tokens[0], "start")
        end = self._parse_datetime_literal(tokens[1], "end")
        if end < start:
            raise SpecSyntaxError("datetime end must be >= start", self.lexer.location())
        time_unit = "us"
        time_zone: str | None = None
        for token in tokens[2:]:
            if token.startswith("unit="):
                time_unit = token[len("unit=") :].strip()
                if not time_unit:
                    raise SpecSyntaxError("unit= must provide a value", self.lexer.location())
            elif token.startswith("tz="):
                candidate = token[len("tz=") :].strip()
                if not candidate:
                    raise SpecSyntaxError("tz= must provide a value", self.lexer.location())
                try:
                    ZoneInfo(candidate)
                except Exception as exc:  # pragma: no cover - timezone DB may be missing
                    raise SpecSyntaxError(
                        f"unknown timezone '{candidate}'",
                        self.lexer.location(),
                    ) from exc
                time_zone = candidate
            elif token:
                raise SpecSyntaxError("unexpected token in datetime[...]", self.lexer.location())
        return {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "time_unit": time_unit,
            "time_zone": time_zone,
        }

    def _parse_time_bounds(self) -> dict[str, object]:
        tokens = self._parse_arguments("[", "]")
        if not tokens:
            return {"start": None, "end": None}
        if len(tokens) != 2:
            raise SpecSyntaxError(
                "time[...] expects either zero or two values", self.lexer.location()
            )
        start = self._parse_time_literal(tokens[0], "start")
        end = self._parse_time_literal(tokens[1], "end")
        if end < start:
            raise SpecSyntaxError("time end must be >= start", self.lexer.location())
        return {"start": start.isoformat(), "end": end.isoformat()}

    def _parse_duration_bounds(self) -> dict[str, Decimal]:
        bounds = self._parse_numeric_args(2)
        low, high = bounds
        if high < low:
            raise SpecSyntaxError(
                "duration upper bound must be >= lower bound", self.lexer.location()
            )
        return {"low": low, "high": high}

    def _parse_list_int_args(self) -> dict[str, int]:
        args = self._parse_arguments("(", ")")
        if not args:
            raise SpecSyntaxError(
                "list_int() requires at least one argument", self.lexer.location()
            )
        if len(args) not in {1, 2, 4}:
            raise SpecSyntaxError("list_int() expects 1, 2, or 4 arguments", self.lexer.location())
        numbers = [to_decimal(arg) for arg in args]
        ints: list[int] = []
        for value in numbers:
            if value != value.to_integral():
                raise SpecSyntaxError(
                    "list_int() arguments must be integers", self.lexer.location()
                )
            ints.append(int(value))
        if len(ints) == 1:
            min_len = max_len = ints[0]
            low, high = 0, 100
        elif len(ints) == 2:
            min_len, max_len = ints
            low, high = 0, 100
        else:
            min_len, max_len, low, high = ints
        if min_len < 0 or max_len < 0:
            raise SpecSyntaxError("list lengths must be non-negative", self.lexer.location())
        if max_len < min_len:
            raise SpecSyntaxError(
                "list_int max length must be >= min length", self.lexer.location()
            )
        if high < low:
            raise SpecSyntaxError("list_int high must be >= low", self.lexer.location())
        return {
            "min_length": min_len,
            "max_length": max_len,
            "low": low,
            "high": high,
        }

    def _parse_list_bounds(self) -> tuple[int, int]:
        if self.lexer.peek() != "(":
            return 1, 3
        self.lexer.expect("(")
        inner = self._consume_balanced("(", ")")
        tokens = [token.strip() for token in self._split_arguments(inner) if token.strip()]
        if not tokens:
            raise SpecSyntaxError("list(...) requires at least one length", self.lexer.location())
        numbers = [to_decimal(token) for token in tokens]
        lengths: list[int] = []
        for value in numbers:
            if value != value.to_integral():
                raise SpecSyntaxError("list(...) lengths must be integers", self.lexer.location())
            lengths.append(int(value))
        if len(lengths) == 1:
            min_length = max_length = lengths[0]
        elif len(lengths) == 2:
            min_length, max_length = lengths
        else:
            raise SpecSyntaxError("list(...) expects one or two integers", self.lexer.location())
        if min_length < 0 or max_length < 0:
            raise SpecSyntaxError("list lengths must be non-negative", self.lexer.location())
        if max_length < min_length:
            raise SpecSyntaxError("list max length must be >= min length", self.lexer.location())
        return min_length, max_length

    def _parse_array_size(self) -> int:
        if self.lexer.peek() != "(":
            raise SpecSyntaxError("array(...) requires a size", self.lexer.location())
        self.lexer.expect("(")
        inner = self._consume_balanced("(", ")")
        tokens = [token.strip() for token in self._split_arguments(inner) if token.strip()]
        if len(tokens) != 1:
            raise SpecSyntaxError(
                "array(...) expects exactly one integer size",
                self.lexer.location(),
            )
        size_dec = to_decimal(tokens[0])
        if size_dec != size_dec.to_integral():
            raise SpecSyntaxError("array size must be an integer", self.lexer.location())
        size = int(size_dec)
        if size < 0:
            raise SpecSyntaxError("array size must be non-negative", self.lexer.location())
        return size

    def _parse_struct_fields(self) -> tuple[StructFieldSpec, ...]:
        self.lexer.expect("{")
        inner = self._consume_balanced("{", "}")
        parts = [part.strip() for part in self._split_arguments(inner) if part.strip()]
        if not parts:
            raise SpecSyntaxError("struct{} requires at least one field", self.lexer.location())
        fields: list[StructFieldSpec] = []
        seen: set[str] = set()
        for part in parts:
            if "=" not in part:
                raise SpecSyntaxError("struct field must use name=generator", self.lexer.location())
            name_token, fragment = part.split("=", 1)
            field_name = name_token.strip()
            if not field_name:
                raise SpecSyntaxError("struct field name cannot be empty", self.lexer.location())
            if not all(ch.isalnum() or ch in "._-" for ch in field_name):
                raise SpecSyntaxError("invalid struct field name", self.lexer.location())
            if field_name in seen:
                raise SpecSyntaxError("duplicate struct field name", self.lexer.location())
            definition = self._parse_generated_fragment(fragment)
            fields.append(StructFieldSpec(name=field_name, definition=definition))
            seen.add(field_name)
        return tuple(fields)

    def _parse_nested_generated_column(self, owner: str) -> GeneratedColumnSpec:
        self.lexer.expect("{")
        inner = self._consume_balanced("{", "}")
        if not inner.strip():
            raise SpecSyntaxError(f"{owner}{{}} requires an inner generator", self.lexer.location())
        return self._parse_generated_fragment(inner)

    def _parse_generated_fragment(self, fragment: str) -> GeneratedColumnSpec:
        source = fragment.strip()
        if not source:
            raise SpecSyntaxError("expected generator fragment", self.lexer.location())
        fake_spec = f"1r/__={source}"
        nested_parser = SpecParser(fake_spec, self.config)
        nested_spec = nested_parser.parse()
        if len(nested_spec.columns) != 1:
            raise SpecSyntaxError(
                "nested generator must resolve to a single definition",
                self.lexer.location(),
            )
        column = nested_spec.columns[0]
        if not isinstance(column.definition, GeneratedColumnSpec):
            raise SpecSyntaxError("nested generator cannot be an expression", self.lexer.location())
        return column.definition

    def _parse_time_literal(self, token: str, role: str) -> time:
        try:
            parsed = time.fromisoformat(token)
        except ValueError as exc:
            raise SpecSyntaxError(f"invalid {role} time '{token}'", self.lexer.location()) from exc
        return parsed

    def _parse_datetime_literal(self, token: str, role: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(token)
        except ValueError as exc:
            raise SpecSyntaxError(
                f"invalid {role} datetime '{token}'", self.lexer.location()
            ) from exc
        return parsed

    def _parse_numeric_args(self, expected: int) -> Sequence[Decimal]:
        args = self._parse_arguments("(", ")")
        if len(args) != expected:
            raise SpecSyntaxError(
                f"expected {expected} arguments but received {len(args)}", self.lexer.location()
            )
        return tuple(to_decimal(arg) for arg in args)

    def _parse_maybe_empty_numeric_args(self) -> Sequence[Decimal]:
        args = self._parse_arguments("(", ")")
        if len(args) == 1 and args[0] == "":
            return ()
        return tuple(to_decimal(arg) for arg in args if arg != "")

    def _parse_enum_labels(self) -> Sequence[str]:
        self.lexer.expect("[")
        content = self._consume_balanced("[", "]")
        tokens = [item.strip() for item in content.split(",") if item.strip()]
        if not tokens:
            raise SpecSyntaxError("enum requires at least one label", self.lexer.location())
        for token in tokens:
            if not all(ch.isalnum() or ch in "._-" for ch in token):
                raise SpecSyntaxError("invalid enum label", self.lexer.location())
        return tuple(tokens)

    def _parse_date_range(self) -> tuple[str, str]:
        self.lexer.expect("[")
        inner = self._consume_balanced("[", "]")
        parts = [part.strip() for part in inner.split(",") if part.strip()]
        if len(parts) != 2:
            raise SpecSyntaxError("date[...] expects two ISO dates", self.lexer.location())
        try:
            date.fromisoformat(parts[0])
            date.fromisoformat(parts[1])
        except ValueError as exc:
            raise SpecSyntaxError("invalid ISO date", self.lexer.location()) from exc
        return parts[0], parts[1]

    def _parse_ts(self) -> dict[str, object]:
        args = self._parse_arguments("(", ")")
        if len(args) < 2:
            raise SpecSyntaxError("ts() requires at least freq and start", self.lexer.location())
        freq = args[0].strip()
        start = args[1].strip()
        if not freq:
            raise SpecSyntaxError("ts() requires non-empty frequency", self.lexer.location())
        if not start:
            raise SpecSyntaxError("ts() requires non-empty start", self.lexer.location())
        trend = Decimal(0)
        seasons: list[SeasonComponent] = []
        noise: GeneratorSpec | None = None
        for token in args[2:]:
            if token.startswith("trend="):
                trend = to_decimal(token.split("=", 1)[1])
            elif token.startswith("season="):
                seasons = list(self._parse_season_components(token.split("=", 1)[1]))
            elif token.startswith("noise="):
                noise = self._parse_noise_spec(token.split("=", 1)[1])
            elif token:
                raise SpecSyntaxError("unknown ts() parameter", self.lexer.location())
        return {
            "freq": freq,
            "start": start,
            "trend": trend,
            "seasons": tuple(seasons),
            "noise": noise,
        }

    def _parse_noise_spec(self, fragment: str) -> GeneratorSpec:
        fragment = fragment.strip()
        if not fragment.lower().startswith("normal"):
            raise SpecSyntaxError("noise must be normal(mean,stddev)", self.lexer.location())
        remainder = fragment[len("normal") :].strip()
        if not remainder.startswith("(") or not remainder.endswith(")"):
            raise SpecSyntaxError("noise normal(...) missing parentheses", self.lexer.location())
        inner = remainder[1:-1]
        args = [part.strip() for part in self._split_arguments(inner)] if inner else []
        if len(args) != 2:
            raise SpecSyntaxError("noise normal(...) expects two arguments", self.lexer.location())
        mean, stddev = (to_decimal(arg) for arg in args)
        return GeneratorSpec(
            kind=GeneratorKind.NORMAL,
            params={"mean": mean, "stddev": stddev},
        )

    def _parse_season_components(self, fragment: str) -> Iterable[SeasonComponent]:
        components = fragment.split("+") if fragment else []
        for component in components:
            component = component.strip()
            if not component:
                continue
            if ":" not in component:
                raise SpecSyntaxError("season must be period:amplitude", self.lexer.location())
            period_str, amplitude_str = component.split(":", 1)
            yield SeasonComponent(to_decimal(period_str), to_decimal(amplitude_str))

    def _parse_arguments(self, open_char: str, close_char: str) -> Sequence[str]:
        self.lexer.expect(open_char)
        inner = self._consume_balanced(open_char, close_char)
        if not inner:
            return ()
        return tuple(self._split_arguments(inner))

    def _maybe_parse_modifier(self) -> Modifier | None:
        peek = self.lexer.peek()
        if peek is None:
            return None
        if peek == "~":
            self.lexer.advance()
            keyword = self.lexer.consume_identifier()
            if keyword != "clip":
                raise SpecSyntaxError("expected clip modifier", self.lexer.location())
            bounds = self._parse_numeric_args(2)
            return Modifier(kind=ModifierKind.CLIP, params={"low": bounds[0], "high": bounds[1]})
        if peek == "+":
            self.lexer.advance()
            next_char = self.lexer.peek()
            if next_char is None:
                raise SpecSyntaxError("dangling '+'", self.lexer.location())
            if next_char.isalpha():
                ident = self.lexer.consume_identifier().lower()
                if ident != "noise":
                    raise SpecSyntaxError("unknown + modifier", self.lexer.location())
                name = self.lexer.consume_identifier().lower()
                if name != "normal":
                    raise SpecSyntaxError(
                        "noise modifier requires normal(...)",
                        self.lexer.location(),
                    )
                params = self._parse_numeric_args(2)
                return Modifier(
                    kind=ModifierKind.NOISE_NORMAL,
                    params={"mean": params[0], "stddev": params[1]},
                )
            number = to_decimal(self.lexer.consume_number_literal())
            return Modifier(kind=ModifierKind.OFFSET, params={"value": number})
        if peek == "*":
            self.lexer.advance()
            value = to_decimal(self.lexer.consume_number_literal())
            return Modifier(kind=ModifierKind.SCALE, params={"value": value})
        if peek == "|":
            self.lexer.advance()
            ident = self.lexer.consume_identifier().lower()
            if ident == "log":
                return Modifier(kind=ModifierKind.LOG, params={})
            if ident == "exp":
                return Modifier(kind=ModifierKind.EXP, params={})
            if ident == "abs":
                return Modifier(kind=ModifierKind.ABS, params={})
            raise SpecSyntaxError("unknown | modifier", self.lexer.location())
        if peek == "?":
            self.lexer.advance()
            percent = to_decimal(self.lexer.consume_number_literal())
            return Modifier(kind=ModifierKind.NULL_PERCENT, params={"value": percent})
        if peek == "!":
            self.lexer.advance()
            return Modifier(kind=ModifierKind.UNIQUE, params={})
        return None

    def _consume_balanced(self, open_char: str, close_char: str) -> str:
        depth = 1
        start = self.lexer.index
        while depth:
            ch = self.lexer.advance()
            if ch == open_char:
                depth += 1
            elif ch == close_char:
                depth -= 1
        end = self.lexer.index - 1
        return self.lexer.source[start:end]

    def _split_arguments(self, fragment: str) -> Iterable[str]:
        args: list[str] = []
        depth = 0
        start = 0
        for idx, ch in enumerate(fragment):
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            elif ch == "," and depth == 0:
                args.append(fragment[start:idx].strip())
                start = idx + 1
        args.append(fragment[start:].strip())
        return args


def parse_spec(source: str) -> Spec:
    """Parse ``source`` into a :class:`~pulka.synth.types.Spec`."""

    parser = SpecParser(source)
    return parser.parse()


__all__ = ["parse_spec", "SpecParser", "ParserConfig"]
