"""Registry for sheet implementations."""

from __future__ import annotations

import inspect
from contextlib import contextmanager

from ..core.sheet import Sheet


class SheetRegistry:
    """Manage sheet constructors exposed to a session."""

    def __init__(self) -> None:
        self._kinds: dict[str, type[Sheet]] = {}
        self._providers: dict[str, str] = {}
        self._provider_stack: list[str] = ["core"]

    @contextmanager
    def provider_scope(self, provider: str):
        """Attribute registrations performed in the scope to ``provider``."""

        self._provider_stack.append(provider)
        try:
            yield
        finally:
            self._provider_stack.pop()

    def _current_provider(self) -> str:
        if not self._provider_stack:
            return "unknown"
        return self._provider_stack[-1]

    def register_sheet(self, kind: str, cls: type[Sheet]) -> None:
        """Register a sheet implementation under ``kind``.

        Parameters
        ----------
        kind:
            Unique name identifying the sheet type.
        cls:
            Concrete ``Sheet`` implementation.
        """

        owner = self._current_provider()
        if kind in self._kinds:
            existing = self._providers[kind]
            msg = (
                f"Sheet kind '{kind}' already provided by {existing}; "
                f"{owner} attempted to register a duplicate"
            )
            raise ValueError(msg)

        self._validate_factory(kind, cls)
        self._kinds[kind] = cls
        self._providers[kind] = owner

    def create(self, kind: str, *args, **kwargs) -> Sheet:
        """Instantiate a registered sheet."""

        cls = self._kinds.get(kind)
        if cls is None:
            msg = f"Unknown sheet kind '{kind}'"
            raise KeyError(msg)

        instance = cls(*args, **kwargs)
        self._validate_instance(kind, instance)
        return instance

    def list_kinds(self) -> list[str]:
        """Return registered sheet kinds."""

        return sorted(self._kinds)

    def _validate_factory(self, kind: str, cls: type[Sheet]) -> None:
        """Ensure ``cls`` accepts a base sheet when constructed."""

        try:
            signature = inspect.signature(cls)
        except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
            msg = f"Cannot introspect sheet factory for '{kind}': {exc}"
            raise TypeError(msg) from exc

        params = list(signature.parameters.values())
        if params and params[0].name == "self":
            params = params[1:]
        if not params:
            raise TypeError(f"Sheet '{kind}' must accept the source sheet as the first argument")
        first = params[0]
        if first.kind not in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            raise TypeError(f"Sheet '{kind}' must accept the source sheet as a positional argument")

    def _validate_instance(self, kind: str, instance: Sheet) -> None:
        """Ensure ``instance`` exposes the minimal sheet protocol."""

        required_attrs = [
            "columns",
            "fetch_slice",
            "get_value_at",
        ]
        missing = [name for name in required_attrs if not hasattr(instance, name)]
        if missing:
            joined = ", ".join(missing)
            raise TypeError(f"Sheet '{kind}' returned object missing: {joined}")
