from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class IndicatorVM:
    id: int
    name: str = ""
    order: int | None = None
    is_active: bool = True
    measurement_unit: str | None = None
    score: float | None = None


@dataclass(slots=True)
class ScopeVM:
    id: int
    name: str = ""
    order: int | None = None
    is_active: bool = True
    system_name: str | None = None
    coefficient: float | None = None
    score: float | None = None
    min_score: float | None = None
    max_score: float | None = None
    indicators: list[IndicatorVM] = field(default_factory=list)


@dataclass(slots=True)
class CategoryVM:
    id: int
    name: str = ""
    order: int | None = None
    is_active: bool = True
    system_name: str | None = None
    coefficient: float | None = None
    score: float | None = None
    scopes: list[ScopeVM] = field(default_factory=list)


@dataclass(slots=True)
class SegmentVM:
    id: int
    name: str = ""
    order: int | None = None
    is_active: bool = True
    system_name: str | None = None
    coefficient: float | None = None
    score: float | None = None
    categories: list[CategoryVM] = field(default_factory=list)
