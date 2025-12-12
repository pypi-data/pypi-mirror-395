from __future__ import annotations

from typing import Optional

from nsj_pyRPA.dto.notification_team_dto import NotificationTeamDTO


class NotificationTeamAssignmentRepository:

    def __init__(self, db_adapter):
        self._db = db_adapter

    def get_assigned_team(self, automacaoempresa: str) -> Optional[NotificationTeamDTO]:
        sql = f"""
            SELECT
                link.destinatario,
                team.codigo,
                team.nome,
                COALESCE(
                    (
                        SELECT string_agg(email, ', ' ORDER BY email)
                        FROM persona.automacoesdestinatariosusuarios users
                        WHERE users.destinatario = team.destinatario
                    ),
                    ''
                ) AS emails,
                COALESCE(
                    (
                        SELECT COUNT(*)
                        FROM persona.automacoesdestinatariosusuarios users
                        WHERE users.destinatario = team.destinatario
                    ),
                    0
                ) AS membros
            FROM persona.automacoesdestinatariosempresas link
            INNER JOIN persona.automacoesdestinatarios team
                ON team.destinatario = link.destinatario
            WHERE link.automacaoempresa = :automacaoempresa
            ORDER BY link.lastupdate DESC
            LIMIT 1
        """
        row = self._db.execute_query_first_result(sql, automacaoempresa=automacaoempresa)
        if not row:
            return None
        return NotificationTeamDTO(
            equipe_id=str(row.get("destinatario") or ""),
            codigo=str(row.get("codigo") or ""),
            nome=str(row.get("nome") or ""),
            emails=str(row.get("emails") or ""),
            membros=int(row.get("membros") or 0),
        )

    def assign_team(self, automacaoempresa: str, equipe_id: str) -> None:
        self._db.execute(
            f"DELETE FROM persona.automacoesdestinatariosempresas WHERE automacaoempresa = :automacaoempresa",
            automacaoempresa=automacaoempresa,
        )
        sql = f"""
            INSERT INTO persona.automacoesdestinatariosempresas (
                automacaoempresa,
                destinatario,
                created_at,
                lastupdate
            ) VALUES (
                :automacaoempresa,
                :destinatario,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
        """
        self._db.execute(sql, automacaoempresa=automacaoempresa, destinatario=equipe_id)

    def clear_assignment(self, automacaoempresa: str) -> None:
        self._db.execute(
            f"DELETE FROM persona.automacoesdestinatariosempresas WHERE automacaoempresa = :automacaoempresa",
            automacaoempresa=automacaoempresa,
        )
