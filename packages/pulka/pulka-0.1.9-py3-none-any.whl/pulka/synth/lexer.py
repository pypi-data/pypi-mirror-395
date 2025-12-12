"""Utility lexer for the semi-compact spec grammar."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["SpecSyntaxError", "SpecLexer", "SourceLocation"]


@dataclass(frozen=True)
class SourceLocation:
    """Point within the source string (0-based column)."""

    index: int

    @property
    def column(self) -> int:
        return self.index


class SpecSyntaxError(ValueError):
    """Exception raised when parsing fails."""

    def __init__(self, message: str, location: SourceLocation):
        super().__init__(message)
        self.location = location

    def __str__(self) -> str:
        return f"{super().__str__()} (at column {self.location.column})"


class SpecLexer:
    """Cursor-style lexer for the semi-compact specification grammar."""

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.index = 0

    def location(self) -> SourceLocation:
        return SourceLocation(self.index)

    def eof(self) -> bool:
        return self.index >= self.length

    def peek(self) -> str | None:
        self.skip_ignored()
        if self.index >= self.length:
            return None
        return self.source[self.index]

    def advance(self) -> str:
        if self.index >= self.length:
            raise SpecSyntaxError("unexpected end of spec", self.location())
        ch = self.source[self.index]
        self.index += 1
        return ch

    def expect(self, expected: str) -> None:
        self.skip_ignored()
        actual = self.advance()
        if actual != expected:
            raise SpecSyntaxError(f"expected '{expected}' but found '{actual}'", self.location())

    def consume_while(self, predicate) -> str:
        start = self.index
        while self.index < self.length and predicate(self.source[self.index]):
            self.index += 1
        return self.source[start : self.index]

    def consume_identifier(self) -> str:
        self.skip_ignored()
        ident = self.consume_while(lambda ch: ch.isalnum() or ch in "._-")
        if not ident:
            raise SpecSyntaxError("expected identifier", self.location())
        return ident

    def consume_column_name(self) -> str:
        self.skip_ignored()
        ident = self.consume_while(lambda ch: ch.isalnum() or ch in "._-")
        if not ident:
            raise SpecSyntaxError("expected column name", self.location())
        return ident

    def consume_number_literal(self) -> str:
        self.skip_ignored()
        start = self.index
        if not self.eof() and self.source[self.index] in "+-":
            self.index += 1
        digits = self.consume_while(str.isdigit)
        if not digits:
            raise SpecSyntaxError("expected digits", self.location())
        if not self.eof() and self.source[self.index] == ".":
            self.index += 1
            self.consume_while(str.isdigit)
        if not self.eof() and self.source[self.index] in "eE":
            self.index += 1
            if not self.eof() and self.source[self.index] in "+-":
                self.index += 1
            exponent_digits = self.consume_while(str.isdigit)
            if not exponent_digits:
                raise SpecSyntaxError("invalid exponent", self.location())
        return self.source[start : self.index]

    def consume_until(self, terminators: set[str]) -> str:
        self.skip_ignored()
        start = self.index
        while self.index < self.length and self.source[self.index] not in terminators:
            self.index += 1
        return self.source[start : self.index]

    def optional(self, char: str) -> bool:
        self.skip_ignored()
        if self.peek() == char:
            self.index += 1
            return True
        return False

    def remaining(self) -> str:
        self.skip_ignored()
        return self.source[self.index :]

    def skip_ignored(self) -> None:
        while self.index < self.length and self.source[self.index] in " \t\n\r":
            self.index += 1
