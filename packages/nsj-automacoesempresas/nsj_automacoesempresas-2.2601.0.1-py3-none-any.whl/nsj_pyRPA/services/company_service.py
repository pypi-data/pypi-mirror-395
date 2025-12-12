from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Optional, Protocol

from nsj_pyRPA.dto.company_dto import CompanyDTO, CompanySettingsDTO
from nsj_pyRPA.dto.notification_team_dto import NotificationTeamDTO
from nsj_pyRPA.services.company_settings_service import CompanySettingsService
from nsj_pyRPA.services.notification_team_service import NotificationTeamRepository


class CompanyRepository(Protocol):
    """Abstraction for company CRUD operations."""

    def list_companies(self) -> List[CompanyDTO]:
        ...

    def save_company(self, company: CompanyDTO) -> Optional[CompanyDTO]:
        ...


class NotificationTeamAssignmentStore(Protocol):
    """Abstraction for linking companies and notification teams."""

    def get_assigned_team(self, automacaoempresa: str) -> Optional[NotificationTeamDTO]:
        ...

    def assign_team(self, automacaoempresa: str, equipe_id: str) -> None:
        ...

    def clear_assignment(self, automacaoempresa: str) -> None:
        ...



class CompanyService:
    """
    Coordinates operations between the UI layer and repositories.

    The service keeps business rules (e.g. only one company can be padrão) away
    from the Qt widgets while remaining storage-agnostic via injected repos.
    """

    def __init__(
        self,
        company_repo: CompanyRepository,
        settings_service: CompanySettingsService,
        notification_team_repo: NotificationTeamRepository,
        team_assignment_repo: NotificationTeamAssignmentStore,
    ):
        self._company_repo = company_repo
        self._settings_service = settings_service
        self._team_repo = notification_team_repo
        self._team_assignment_repo = team_assignment_repo

    # --- Companies -----------------------------------------------------
    def list_companies(self) -> List[CompanyDTO]:
        return self._company_repo.list_companies()

    def set_company_active(self, company: CompanyDTO, ativo: bool) -> CompanyDTO:
        updated = replace(company, ativo=ativo)
        persisted = self._company_repo.save_company(updated)
        return persisted if persisted is not None else updated

    def set_default_company(self, company_code: str) -> CompanyDTO:
        companies = self._company_repo.list_companies()
        updated_dto: Optional[CompanyDTO] = None
        for dto in companies:
            new_value = dto.codigo == company_code
            if dto.padrao != new_value:
                changed = replace(dto, padrao=new_value)
                self._company_repo.save_company(changed)
                if changed.codigo == company_code:
                    updated_dto = changed
        if updated_dto is None:
            raise ValueError(f"Company '{company_code}' not found")
        return updated_dto

    def update_company_preferences(
        self, company: CompanyDTO, use_default: bool, notified_teams: str
    ) -> CompanyDTO:
        updated = replace(
            company,
            use_default=use_default,
            notified_teams=notified_teams,
        )
        persisted = self._company_repo.save_company(updated)
        return persisted if persisted is not None else updated

    def ensure_company_automation(self, company: CompanyDTO) -> CompanyDTO:
        if company.automacaoempresa:
            return company
        persisted = self._company_repo.save_company(company)
        if persisted is None:
            raise RuntimeError("Nao foi possivel criar registro em automacoesempresas")
        return persisted

    # --- Settings ------------------------------------------------------
    def get_company_settings(self, company_code: str) -> CompanySettingsDTO:
        return self._settings_service.get_settings(company_code)

    def save_company_settings(self, settings: CompanySettingsDTO) -> CompanySettingsDTO:
        return self._settings_service.save_settings(settings)

    # --- Notification teams -------------------------------------------
    def list_notification_teams(self) -> List[NotificationTeamDTO]:
        return self._team_repo.list_teams()

    def get_assigned_notification_team(
        self, automacaoempresa: Optional[str]
    ) -> Optional[NotificationTeamDTO]:
        if not automacaoempresa:
            return None
        return self._team_assignment_repo.get_assigned_team(automacaoempresa)

    def save_notification_team_assignment(
        self, automacaoempresa: str, equipe_id: Optional[str]
    ) -> Optional[NotificationTeamDTO]:
        if not automacaoempresa:
            raise ValueError("Automacaoempresa é obrigatório para vincular equipe")
        if not equipe_id:
            self._team_assignment_repo.clear_assignment(automacaoempresa)
            return None
        self._team_assignment_repo.assign_team(automacaoempresa, equipe_id)
        return self._team_assignment_repo.get_assigned_team(automacaoempresa)


# ---------------------------------------------------------------------------
# Optional in-memory repositories for experimentation/tests
# ---------------------------------------------------------------------------


class InMemoryCompanyRepository:
    def __init__(self, companies: Optional[List[CompanyDTO]] = None):
        self._companies: Dict[str, CompanyDTO] = {
            dto.codigo: dto for dto in (companies or [])
        }

    def list_companies(self) -> List[CompanyDTO]:
        return list(self._companies.values())

    def save_company(self, company: CompanyDTO) -> None:
        self._companies[company.codigo] = company


class InMemoryCompanySettingsRepository:
    def __init__(self):
        self._settings: Dict[str, CompanySettingsDTO] = {}

    def get_settings(self, company_code: str) -> CompanySettingsDTO:
        if company_code not in self._settings:
            raise KeyError(
                f"Settings for company '{company_code}' not found. "
                "Initialize them before opening the editor."
            )
        return self._settings[company_code]

    def save_settings(self, settings: CompanySettingsDTO) -> None:
        self._settings[settings.automacaoempresa] = settings
