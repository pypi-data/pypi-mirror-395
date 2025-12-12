from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime
from typing import Dict, List, Optional, Protocol

from croniter import croniter

from nsj_pyRPA.dto.company_dto import CompanySettingsDTO, ScheduleConfig
from nsj_pyRPA.dto.jobschedule_dto import JobScheduleDTO
from nsj_pyRPA.resources.automation_types import (
    AUTOMATION_TYPES,
    automation_default_values,
)


class CompanySettingsPersistence(Protocol):
    def fetch_active_settings(self, company_code: str) -> List[Dict]:
        ...

    def list_existing_types(self, company_code: str) -> set[str]:
        ...

    def upsert_parameter(
        self,
        company_code: str,
        automation_type: str,
        payload: str,
        ativo: bool,
    ) -> Dict:
        ...

    def save_job_schedule(self, parametro_id, job: JobScheduleDTO) -> Optional[str]:
        ...

    def automation_jobtype(self) -> str:
        ...


class CompanySettingsService:
    """Encapsulates business rules for automation schedules and job syncing."""

    def __init__(self, repository: CompanySettingsPersistence):
        self._repository = repository

    def get_settings(self, company_code: str) -> CompanySettingsDTO:
        if not company_code:
            raise ValueError("Company identifier is required to load settings")
        rows = self._repository.fetch_active_settings(company_code)
        schedules: Dict[str, ScheduleConfig] = {}
        for row in rows:
            automation_type = row.get("tipo") or ""
            payload = row.get("parametros") or {}
            schedules[automation_type] = self._schedule_from_payload(payload, automation_type)

        dto = CompanySettingsDTO(automacaoempresa=company_code, schedules=schedules)
        return self._ensure_default_schedules(dto)

    def save_settings(self, settings: CompanySettingsDTO) -> CompanySettingsDTO:
        if not settings.automacaoempresa:
            raise ValueError("Company identifier is required to save settings")
        normalized = self._normalize_schedule_fields(settings)
        finalized = self._apply_cron_fields(normalized)
        self._persist(finalized)
        return finalized

    # ------------------------------------------------------------------
    # Persistence coordination
    # ------------------------------------------------------------------
    def _persist(self, settings: CompanySettingsDTO) -> None:
        existing_types = self._repository.list_existing_types(settings.automacaoempresa)
        jobtype_id = self._repository.automation_jobtype()

        for automation_type, schedule in settings.schedules.items():
            has_row = automation_type in existing_types
            if not has_row and not schedule.enabled:
                continue

            serialized = self._serialize_schedule(schedule)
            ativo = serialized.get("enabled", False)
            payload = json.dumps(serialized)

            row = self._repository.upsert_parameter(
                settings.automacaoempresa,
                automation_type,
                payload,
                ativo,
            )

            parametro_id = row["automacaoempresaparametro"]
            existing_job_id = row.get("jobschedule")
            job = JobScheduleDTO(
                jobtype=jobtype_id,
                tenant=0,
                jobschedule=str(existing_job_id) if existing_job_id else None,
                entrada={
                    "automacaotipo": automation_type,
                    "automacaoempresaparametro": str(parametro_id),
                },
                status=0 if ativo else 3,
                tipoagendamento=4,
                agendamento=self._next_agendamento(schedule.cron),
                codigo=automation_type,
                expressaocron=schedule.cron,
            )
            self._repository.save_job_schedule(parametro_id, job)

    # ------------------------------------------------------------------
    # DTO transformations
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize_schedule_fields(settings: CompanySettingsDTO) -> CompanySettingsDTO:
        normalized = {
            automation_type: CompanySettingsService._normalize_schedule(config)
            for automation_type, config in settings.schedules.items()
        }
        return replace(settings, schedules=normalized)

    @staticmethod
    def _normalize_schedule(config: ScheduleConfig) -> ScheduleConfig:
        if config.frequency == "Mensalmente":
            return replace(config, weekday=None)
        if config.frequency == "Semanalmente":
            return replace(config, day_of_month=None)
        return replace(config, day_of_month=None, weekday=None)

    @staticmethod
    def _apply_cron_fields(settings: CompanySettingsDTO) -> CompanySettingsDTO:
        with_cron = {
            automation_type: CompanySettingsService._attach_cron(config)
            for automation_type, config in settings.schedules.items()
        }
        return replace(settings, schedules=with_cron)

    @staticmethod
    def _attach_cron(config: ScheduleConfig) -> ScheduleConfig:
        cron = CompanySettingsService._cron_expression(
            config.frequency, config.day_of_month, config.weekday, config.time
        )
        return replace(config, cron=cron)

    def _schedule_from_payload(self, payload: Dict, automation_type: str) -> ScheduleConfig:
        schedule = self._default_schedule(automation_type)
        if not isinstance(payload, dict):
            return schedule

        frequency = str(payload.get("frequency", schedule.frequency))
        if schedule.allowed_frequencies and frequency not in schedule.allowed_frequencies:
            frequency = schedule.allowed_frequencies[0]

        return ScheduleConfig(
            enabled=_to_bool(payload.get("enabled"), schedule.enabled),
            frequency=frequency,
            day_of_month=payload.get("day_of_month", schedule.day_of_month),
            weekday=payload.get("weekday", schedule.weekday),
            time=str(payload.get("time", schedule.time)),
            cron=payload.get("cron"),
            allowed_frequencies=list(schedule.allowed_frequencies or []),
        )

    def _default_schedule(self, automation_type: str) -> ScheduleConfig:
        defaults = automation_default_values(automation_type)
        allowed: List[str] = list(defaults["allowed_frequencies"])
        return ScheduleConfig(
            enabled=defaults["enabled"],
            frequency=defaults["frequency"],
            day_of_month=defaults["day_of_month"],
            weekday=defaults["weekday"],
            time=defaults["time"],
            allowed_frequencies=allowed,
        )

    @staticmethod
    def _serialize_schedule(config: ScheduleConfig) -> Dict:
        return {
            "enabled": config.enabled,
            "frequency": config.frequency,
            "day_of_month": config.day_of_month,
            "weekday": config.weekday,
            "time": config.time,
            "cron": config.cron,
        }

    def _ensure_default_schedules(self, settings: CompanySettingsDTO) -> CompanySettingsDTO:
        schedules = dict(settings.schedules)
        for automation_type, config in list(schedules.items()):
            if not config.allowed_frequencies:
                defaults = automation_default_values(automation_type)
                schedules[automation_type] = replace(
                    config, allowed_frequencies=defaults["allowed_frequencies"]
                )
        for automation_type in AUTOMATION_TYPES:
            if automation_type not in schedules:
                schedules[automation_type] = self._default_schedule(automation_type)
        return replace(settings, schedules=schedules)

    # ------------------------------------------------------------------
    # Cron helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _next_agendamento(cron_expression: Optional[str]) -> datetime:
        if not cron_expression:
            raise ValueError("Cron expression is required to calculate next execution")
        return croniter(cron_expression, datetime.now()).get_next(datetime)

    @staticmethod
    def _cron_expression(
        frequency: str,
        day_of_month: Optional[int],
        weekday: Optional[str],
        time_str: str,
    ) -> str:
        hour, minute = CompanySettingsService._parse_time(time_str)
        if frequency == "Mensalmente":
            dom = day_of_month or 1
            return f"{minute} {hour} {dom} * *"
        if frequency == "Semanalmente":
            weekday_map = {
                "Domingo": 0,
                "Segunda": 1,
                "Terça": 2,
                "Quarta": 3,
                "Quinta": 4,
                "Sexta": 5,
                "Sábado": 6,
            }
            day = weekday_map.get(weekday or "Segunda", 1)
            return f"{minute} {hour} * * {day}"
        return f"{minute} {hour} * * *"

    @staticmethod
    def _parse_time(value: str) -> tuple[int, int]:
        try:
            hour_str, minute_str = value.split(":")
            return int(hour_str), int(minute_str)
        except ValueError:
            return 8, 0


def _to_bool(value, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "t", "y", "yes", "sim", "s"}

