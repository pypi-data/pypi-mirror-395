from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class NotificationTeamDTO:
    """
    Simple representation of a notification team used by the service/UI layers.

    Each team groups one or more e-mail addresses that should receive automation
    notifications.
    """

    codigo: str
    nome: str
    emails: str
    membros: int = 0
    equipe_id: Optional[str] = None

    def members_from_emails(self) -> int:
        """Helper that derives the member count from the e-mail list."""
        if not self.emails:
            return 0
        return len([token for token in self.emails.split(",") if token.strip()])
