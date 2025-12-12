from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CompanyDTO:
    """Representation of a company row used by the UI/service layers."""

    codigo: str
    nome: str
    padrao: bool
    ativo: bool
    empresa: str
    automacaoempresa: str
    tenant: int
    use_default: bool = False
    notified_teams: str = ""


@dataclass
class ScheduleConfig:
    """Shared representation for a schedule block."""

    enabled: bool
    frequency: str
    day_of_month: Optional[int]
    weekday: Optional[str]
    time: str
    cron: Optional[str] = None
    allowed_frequencies: Optional[List[str]] = None


@dataclass
class CompanySettingsDTO:
    """Collection of automation schedules keyed by automation type."""

    automacaoempresa: str
    schedules: Dict[str, ScheduleConfig]
