"""Plugin loader for Pulka."""

from __future__ import annotations

import inspect
import logging
from contextlib import ExitStack
from importlib import import_module, metadata
from types import ModuleType
from typing import Any

from .api import PluginError

LOGGER = logging.getLogger(__name__)


def _normalize_identifier(name: str) -> str:
    """Normalize ``name`` for case-insensitive comparisons."""

    return name.strip().lower()


class PluginManager:
    """Load plugins from entry points or explicit module paths."""

    def __init__(
        self,
        *,
        entry_points_group: str = "pulka.plugins",
        modules: list[str] | None = None,
    ) -> None:
        self.entry_points_group = entry_points_group
        self._modules = modules or []
        self.failures: list[tuple[str, str]] = []
        self.loaded_details: list[dict[str, str | None]] = []
        self.disabled_canonical: list[str] = []

    def load(
        self,
        *,
        commands: Any | None = None,
        sheets: Any | None = None,
        scanners: Any | None = None,
        include_entry_points: bool = True,
        disabled: set[str] | None = None,
    ) -> list[str]:
        """Load configured plugins.

        Parameters
        ----------
        commands, sheets, scanners:
            Registries exposed to plugins.
        include_entry_points:
            If ``True`` (default) Python entry points are considered in addition
            to explicitly configured modules.
        disabled:
            Names of entry points that should be skipped.
        """

        registries = {
            "commands": commands,
            "sheets": sheets,
            "scanners": scanners,
        }
        provided_registries = {k: v for k, v in registries.items() if v is not None}

        self.failures = []
        self.loaded_details = []
        loaded: list[str] = []
        seen: set[str] = set()
        disabled = {_normalize_identifier(name) for name in (disabled or set())}
        entry_point_aliases: dict[str, str] = {}
        disabled_canonical: set[str] = set()

        if include_entry_points:
            try:
                entry_points = metadata.entry_points().select(group=self.entry_points_group)
            except Exception:  # pragma: no cover - defensive
                LOGGER.exception("Failed to enumerate plugin entry points")
            else:
                for entry_point in sorted(entry_points, key=lambda ep: ep.name):
                    module_name, _, attr = entry_point.value.partition(":")
                    canonical_name = entry_point.name
                    keys = {canonical_name, module_name, entry_point.value}
                    if attr:
                        keys.add(f"{module_name}:{attr}")
                    normalized_keys = {_normalize_identifier(key) for key in keys if key}
                    canonical_key = _normalize_identifier(canonical_name)
                    normalized_keys.add(canonical_key)

                    for key in normalized_keys:
                        entry_point_aliases[key] = canonical_name

                    if normalized_keys & disabled:
                        disabled_canonical.add(canonical_name)
                        continue
                    if normalized_keys & seen:
                        continue
                    seen.update(normalized_keys)

                    try:
                        module = import_module(module_name)
                        target: Any = getattr(module, attr) if attr else module
                    except Exception as exc:  # pragma: no cover - defensive
                        LOGGER.exception("Failed to import plugin '%s' (%s)", canonical_name, exc)
                        continue

                    if self._activate_plugin(canonical_name, target, provided_registries):
                        loaded.append(canonical_name)
                        self._record_loaded_plugin(
                            canonical_name,
                            module,
                            module_name or canonical_name,
                        )

        for module_path in sorted(self._modules):
            normalized_module = _normalize_identifier(module_path)
            canonical_name = entry_point_aliases.get(normalized_module, module_path)
            canonical_key = _normalize_identifier(canonical_name)
            normalized_keys = {normalized_module, canonical_key}
            if normalized_keys & seen:
                continue
            if normalized_keys & disabled:
                disabled_canonical.add(canonical_name)
                continue
            seen.update(normalized_keys)

            try:
                module = import_module(module_path)
            except Exception:  # pragma: no cover - defensive
                LOGGER.exception("Failed to import plugin module '%s'", module_path)
                continue

            if self._activate_plugin(canonical_name, module, provided_registries):
                loaded.append(canonical_name)
                self._record_loaded_plugin(
                    canonical_name,
                    module,
                    module_path,
                )

        self.disabled_canonical = sorted(disabled_canonical)
        return loaded

    def _activate_plugin(self, name: str, target: Any, registries: dict[str, Any]) -> bool:
        try:
            with ExitStack() as stack:
                for registry in registries.values():
                    if registry is None:
                        continue
                    scope = getattr(registry, "provider_scope", None)
                    if callable(scope):
                        stack.enter_context(scope(name))
                if self._dispatch(target, registries):
                    return True
            raise PluginError("no registration hooks found")
        except Exception as exc:
            LOGGER.exception("Plugin '%s' failed to load", name)
            summary = str(exc) or exc.__class__.__name__
            self.failures.append((name, summary))
            return False

    def _dispatch(self, target: Any, registries: dict[str, Any]) -> bool:
        if inspect.isroutine(target):
            target(**registries)
            return True

        register = getattr(target, "register", None)
        if callable(register):
            register(**registries)
            return True

        used = False
        for key, registry in registries.items():
            method = getattr(target, f"register_{key}", None)
            if callable(method):
                method(registry)
                used = True

        if used:
            return True

        if isinstance(target, ModuleType):
            for attr_name in ("plugin", "PLUGIN"):
                candidate = getattr(target, attr_name, None)
                if (
                    candidate is not None
                    and candidate is not target
                    and self._dispatch(candidate, registries)
                ):
                    return True

        return False

    def _record_loaded_plugin(
        self,
        name: str,
        module: ModuleType | None,
        module_name: str | None,
    ) -> None:
        version = self._resolve_version(module, module_name)
        module_label = module_name or (module.__name__ if module is not None else None)
        self.loaded_details.append(
            {
                "name": name,
                "module": module_label,
                "version": version,
            }
        )

    def _resolve_version(self, module: ModuleType | None, module_name: str | None) -> str | None:
        if module is not None:
            version_attr = getattr(module, "__version__", None)
            if isinstance(version_attr, str) and version_attr:
                return version_attr

        candidates: list[str] = []
        if module is not None:
            package = getattr(module, "__package__", None)
            if package:
                candidates.append(package)
            module_qualname = getattr(module, "__name__", None)
            if module_qualname:
                candidates.append(module_qualname)
                candidates.append(module_qualname.split(".")[0])
        if module_name:
            candidates.append(module_name)
            candidates.append(module_name.split(".")[0])

        seen_candidate: set[str] = set()
        for candidate in candidates:
            if not candidate:
                continue
            normalized = candidate.strip()
            if not normalized or normalized in seen_candidate:
                continue
            seen_candidate.add(normalized)
            try:
                return metadata.version(normalized)
            except metadata.PackageNotFoundError:
                continue
        return None
