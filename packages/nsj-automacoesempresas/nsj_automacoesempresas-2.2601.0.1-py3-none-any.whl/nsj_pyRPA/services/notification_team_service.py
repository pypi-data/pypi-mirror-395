from __future__ import annotations

from typing import List, Protocol

from nsj_pyRPA.dto.notification_team_dto import NotificationTeamDTO


class NotificationTeamRepository(Protocol):
    def list_teams(self) -> List[NotificationTeamDTO]:
        ...

    def get_team(self, codigo: str) -> NotificationTeamDTO:
        ...

    def save_team(self, team: NotificationTeamDTO) -> NotificationTeamDTO:
        ...

    def delete_team(self, codigo: str) -> None:
        ...


class NotificationTeamService:
    """Applies business rules for notification teams before hitting storage."""

    def __init__(self, repository: NotificationTeamRepository):
        self._repository = repository

    def list_teams(self) -> List[NotificationTeamDTO]:
        return self._repository.list_teams()

    def get_team(self, codigo: str) -> NotificationTeamDTO:
        if not codigo:
            raise ValueError("Informe o código da equipe")
        return self._repository.get_team(codigo)

    def save_team(self, team: NotificationTeamDTO) -> NotificationTeamDTO:
        validated = self._validate(team)
        return self._repository.save_team(validated)

    def delete_team(self, codigo: str) -> None:
        if not codigo:
            raise ValueError("Informe o código da equipe")
        self._repository.delete_team(codigo)

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #

    def _validate(self, team: NotificationTeamDTO) -> NotificationTeamDTO:
        codigo = team.codigo.strip()
        if not codigo:
            raise ValueError("Código da equipe não pode ficar em branco")

        nome = team.nome.strip()
        if not nome:
            raise ValueError("Nome da equipe não pode ficar em branco")

        normalized_emails = self._normalize_emails(team.emails)
        if not normalized_emails:
            raise ValueError("Informe ao menos um e-mail")

        membros = self._count_members(normalized_emails)
        return NotificationTeamDTO(
            codigo=codigo,
            nome=nome,
            emails=normalized_emails,
            membros=membros,
            equipe_id=team.equipe_id,
        )

    def _normalize_emails(self, raw_emails: str) -> str:
        candidates = raw_emails.replace(";", ",").split(",")
        seen = set()
        cleaned: List[str] = []
        for candidate in candidates:
            email = candidate.strip()
            if not email:
                continue
            lowered = email.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            cleaned.append(email)
        return ", ".join(cleaned)

    def _count_members(self, emails: str) -> int:
        if not emails:
            return 0
        return len([token for token in emails.split(",") if token.strip()])
