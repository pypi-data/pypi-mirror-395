from __future__ import annotations

from typing import Dict, List, Optional

AUTOMATION_TYPE_EMPLOYEES = "CALC_FOLHA_FUNC"
AUTOMATION_TYPE_DIRECTORS = "CALC_FOLHA_DIR"
AUTOMATION_TYPE_AUTONOMOS = "CALC_FOLHA_AUTO"
AUTOMATION_TYPE_COOPERADOS = "CALC_FOLHA_COOP"

ALL_FREQUENCIES: List[str] = ["Mensalmente", "Semanalmente", "Diariamente"]

GENERIC_DEFAULT = {
    "label": "Automação",
    "enabled": False,
    "frequency": "Mensalmente",
    "day_of_month": 1,
    "weekday": "Segunda",
    "time": "08:00",
    "allowed_frequencies": ALL_FREQUENCIES
}

AUTOMATION_TYPE_DEFAULTS: Dict[str, Dict[str, object]] = {
    AUTOMATION_TYPE_EMPLOYEES: {
        **GENERIC_DEFAULT,
        "label": "Folha de Funcionários",
        "allowed_frequencies": ["Mensalmente", "Semanalmente"]
    },
    AUTOMATION_TYPE_DIRECTORS: {
        **GENERIC_DEFAULT,
        "label": "Folha de Diretores",
        "allowed_frequencies": ["Mensalmente", "Semanalmente"]
    },
    AUTOMATION_TYPE_AUTONOMOS: {
        **GENERIC_DEFAULT,
        "label": "Folha de Autônomos",
    },
    AUTOMATION_TYPE_COOPERADOS: {
        **GENERIC_DEFAULT,
        "label": "Folha de Cooperados",
        "frequency": "Semanalmente",
        "allowed_frequencies": ["Mensalmente", "Semanalmente"]
    },
}

AUTOMATION_TYPES: List[str] = [
    AUTOMATION_TYPE_EMPLOYEES,
    AUTOMATION_TYPE_DIRECTORS,
    AUTOMATION_TYPE_AUTONOMOS,
    AUTOMATION_TYPE_COOPERADOS,
]

CALC_TYPES: List[str] = [
    AUTOMATION_TYPE_EMPLOYEES,
    AUTOMATION_TYPE_DIRECTORS,
    AUTOMATION_TYPE_AUTONOMOS,
    AUTOMATION_TYPE_COOPERADOS,
]


def automation_type_label(automation_type: str) -> str:
    return AUTOMATION_TYPE_DEFAULTS.get(automation_type, GENERIC_DEFAULT)["label"] or automation_type


def automation_default_values(automation_type: str) -> Dict[str, object]:
    base = AUTOMATION_TYPE_DEFAULTS.get(automation_type, GENERIC_DEFAULT)
    allowed = base.get("allowed_frequencies") or ALL_FREQUENCIES
    return {
        "enabled": bool(base.get("enabled", False)),
        "frequency": str(base.get("frequency", "Mensalmente")),
        "day_of_month": base.get("day_of_month"),
        "weekday": base.get("weekday"),
        "time": str(base.get("time", "08:00")),
        "allowed_frequencies": list(allowed),
    }
