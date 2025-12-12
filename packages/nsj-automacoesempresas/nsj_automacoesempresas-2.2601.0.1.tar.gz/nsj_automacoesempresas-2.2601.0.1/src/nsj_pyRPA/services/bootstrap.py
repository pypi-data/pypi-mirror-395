from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from nsj_pyRPA.repositories import (
    DbCompanyRepository,
    DbCompanySettingsRepository,
    DbNotificationTeamRepository,
    NotificationTeamAssignmentRepository,
)
from nsj_pyRPA.resources.conexao_banco import create_pool
from nsj_pyRPA.resources.criptografia_erp2 import CriptografiaERP2
from nsj_pyRPA.resources.db_adapter3 import DBAdapter3
from nsj_pyRPA.resources.envConfig import EnvConfig
from nsj_pyRPA.services.company_service import CompanyService
from nsj_pyRPA.services.company_settings_service import CompanySettingsService
from nsj_pyRPA.services.notification_team_service import NotificationTeamService


@dataclass
class DatabaseConfig:
    database: str
    user: str
    password: str
    host: str
    port: str

    def missing_fields(self) -> List[str]:
        required = ("database", "user", "password", "host", "port")
        return [field for field in required if not getattr(self, field)]

    def resolved_credentials(self) -> tuple[str, str]:
        if self.user.lower() == "postgres":
            return "postgres", "postgres"
        username = self.user.lower() # modificado para comportar env persona
        password = self.password
        # password = CriptografiaERP2().codificar(self.password)
        return username, password


class _DatabaseServiceFactory:
    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._engine = None
        self._connection = None
        self._adapter: Optional[DBAdapter3] = None

    def _build_adapter(self) -> DBAdapter3:
        if self._adapter is not None:
            return self._adapter

        missing = self._config.missing_fields()
        if missing:
            raise ValueError(f"Preencha os campos: {', '.join(missing)}")

        EnvConfig.instance().set_dados_conexao(
            self._config.database,
            self._config.user,
            self._config.password,
            self._config.host,
            self._config.port,
        )

        username, password = self._config.resolved_credentials()
        engine = create_pool(
            username,
            password,
            self._config.host,
            self._config.port,
            self._config.database,
        )
        connection = engine.connect()
        adapter = DBAdapter3(connection)
        EnvConfig.instance().set_db(adapter)

        self._engine = engine
        self._connection = connection
        self._adapter = adapter

        return adapter

    def dispose(self) -> None:
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None

        if self._engine is not None:
            try:
                self._engine.dispose()
            except Exception:
                pass
            self._engine = None

        self._adapter = None
        EnvConfig.instance().set_db(None)


class CompanyServiceFactory(_DatabaseServiceFactory):
    """
    Centralizes the bootstrap of repositories, EnvConfig, and DB resources so
    UI/controllers can simply request a ready-to-use CompanyService instance.
    """

    def build(self) -> CompanyService:
        adapter = self._build_adapter()
        settings_repo = DbCompanySettingsRepository(adapter)
        settings_service = CompanySettingsService(settings_repo)
        company_repo = DbCompanyRepository(adapter)
        team_repo = DbNotificationTeamRepository(adapter)
        assignment_repo = NotificationTeamAssignmentRepository(adapter)
        return CompanyService(company_repo, settings_service, team_repo, assignment_repo)


class NotificationTeamServiceFactory(_DatabaseServiceFactory):
    """Bootstrap helper dedicated to the notification teams UI."""

    def build(self) -> NotificationTeamService:
        adapter = self._build_adapter()
        repository = DbNotificationTeamRepository(adapter)
        return NotificationTeamService(repository)
