from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


JsonPayload = Dict[str, Any]


@dataclass
class JobScheduleDTO:
    """Representation of util.jobschedule rows.

    persona.automacoesempresasparametros.jobschedule references this table,
    so we keep all relevant metadata together in a single structure that can
    be shared across repositories and services.
    """

    jobtype: str
    tenant: int
    jobschedule: Optional[str] = None
    expressaocron: Optional[str] = None
    entrada: Optional[JsonPayload] = None
    status: int = 0
    tipoagendamento: int = 0
    agendamento: Optional[datetime] = None
    datacriacao: Optional[datetime] = None
    lastupdate: Optional[datetime] = None
    codigo: Optional[str] = None
