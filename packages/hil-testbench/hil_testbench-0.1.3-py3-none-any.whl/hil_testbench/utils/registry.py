"""Central pint UnitRegistry and formatting helpers.

This module provides a singleton UnitRegistry and convenience functions for
formatting quantities with automatic SI prefix scaling.
"""

from __future__ import annotations

import contextlib
import threading
from typing import TYPE_CHECKING, Any, cast

try:
    import pint
except ModuleNotFoundError:
    pint = None

UnitRegistryType = Any
QuantityType = Any

if TYPE_CHECKING:  # pragma: no cover - aid static analyzers only
    from pint import Quantity as _PintQuantity  # noqa: F401
    from pint import UnitRegistry as _PintUnitRegistry  # noqa: F401

_REGISTRY_LOCK = threading.Lock()
_UNIT_REGISTRY: UnitRegistryType | None = None
_HAS_PINT = pint is not None


def _create_unit_registry() -> UnitRegistryType:
    """Create a fresh pint registry instance."""

    if pint is None:
        raise RuntimeError("pint is required for unit formatting")
    return pint.UnitRegistry(auto_reduce_dimensions=True)


def get_registry() -> UnitRegistryType:
    """Return the shared pint UnitRegistry instance."""

    global _UNIT_REGISTRY
    registry = _UNIT_REGISTRY
    if registry is not None:
        return registry
    with _REGISTRY_LOCK:
        if _UNIT_REGISTRY is None:
            _UNIT_REGISTRY = _create_unit_registry()
        return _UNIT_REGISTRY


def reset_registry_cache() -> None:
    """Clear the cached pint UnitRegistry (tests only)."""

    global _UNIT_REGISTRY
    with _REGISTRY_LOCK:
        _UNIT_REGISTRY = None


def format_quantity(
    value: float | int,
    unit: str = "",
    precision: int = 2,
    strategy: str = "auto",
) -> str:
    """Format a numeric value with unit using pint.

    Strategies:
    - raw: do not rescale, just show value with unit
    - auto: use pint's to_compact() for intelligent SI prefix scaling
    """
    if not _HAS_PINT:
        parts = [f"{value:.{precision}f}"]
        if unit:
            parts.append(unit)
        return " ".join(parts).strip()

    reg = get_registry()
    # Treat empty unit as dimensionless
    if unit:
        quantity = cast(QuantityType, value * reg(unit))
    else:
        quantity = cast(QuantityType, value * reg.dimensionless)

    if strategy == "auto":
        with contextlib.suppress(Exception):
            quantity = cast(QuantityType, quantity.to_compact())
    # Separate magnitude and unit for formatting
    magnitude = float(quantity.magnitude)
    # Use compact short notation (e.g., "Mbit/s" instead of "Mbit / s")
    unit_str = f"{quantity.units:~P}" if strategy == "auto" else f"{quantity.units:~}"
    unit_str = unit_str.strip()
    if unit_str:
        return f"{magnitude:.{precision}f} {unit_str}"
    return f"{magnitude:.{precision}f}"


class PintValueFormatter:
    """Formatter wrapping pint for consistent interface with display backend."""

    def __init__(
        self,
        unit: str = "",
        precision: int = 2,
        strategy: str = "raw",
    ) -> None:
        self.unit = unit
        self.precision = precision
        self.strategy = strategy  # 'raw' | 'auto'

    def format(self, value: float | int | None) -> str:
        if value is None:
            return "N/A"
        return format_quantity(value, self.unit, self.precision, self.strategy)

    def format_magnitude_only(self, value: float | int | None) -> str:
        """Format value with scaling applied but without unit string."""
        if value is None:
            return "—"
        if not _HAS_PINT:
            return f"{value:.{self.precision}f}"
        reg = get_registry()
        if self.unit:
            quantity = cast(QuantityType, value * reg(self.unit))
        else:
            quantity = cast(QuantityType, value * reg.dimensionless)

        if self.strategy == "auto":
            with contextlib.suppress(Exception):
                quantity = cast(QuantityType, quantity.to_compact())
        magnitude = float(quantity.magnitude)
        return f"{magnitude:.{self.precision}f}"
