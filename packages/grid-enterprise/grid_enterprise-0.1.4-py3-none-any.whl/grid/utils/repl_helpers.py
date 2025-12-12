"""Helper utilities used by the GRID REPL implementation."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

DEFAULT_INTERFACE = "ui"
VALID_INTERFACES = frozenset({"nb", "sim", "viz", "code", "ui", "dc"})


def resolve_interface(
    args: Sequence[str],
    valid_interfaces: Iterable[str] | None = None,
    default: str | None = DEFAULT_INTERFACE,
) -> str | None:
    """Return the requested interface or the default when no args are provided."""
    choices = VALID_INTERFACES if valid_interfaces is None else frozenset(valid_interfaces)
    if not args:
        return default

    candidate = args[0]
    if candidate in choices:
        return candidate
    return None