from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class IndicatorVM:
    id: int
    label: str
    order: int | None
    is_active: bool
    measurement_unit: str | None
    score_value: float | None = None


@dataclass(slots=True)
class ScopeVM:
    id: int
    label: str
    order: int | None
    is_active: bool
    system_name: str | None
    coefficient: float | None
    score_value: float | None
    indicators: list[IndicatorVM] = field(default_factory=list)


@dataclass(slots=True)
class CategoryVM:
    id: int
    label: str
    order: int | None
    is_active: bool
    system_name: str | None
    coefficient: float | None
    score_value: float | None
    scopes: list[ScopeVM] = field(default_factory=list)


@dataclass(slots=True)
class SegmentVM:
    id: int
    label: str
    order: int | None
    is_active: bool
    system_name: str | None
    coefficient: float | None
    score_value: float | None
    categories: list[CategoryVM] = field(default_factory=list)
