from __future__ import annotations

import uuid
from typing import List, Optional

from nsj_pyRPA.dto.notification_team_dto import NotificationTeamDTO
from nsj_pyRPA.services.notification_team_service import NotificationTeamRepository


class DbNotificationTeamRepository(NotificationTeamRepository):

    def __init__(self, db_adapter):
        self._db = db_adapter

    def list_teams(self) -> List[NotificationTeamDTO]:
        sql = (
            self._base_query()
            + """
            GROUP BY eq.destinatario, eq.codigo, eq.nome
            ORDER BY eq.codigo
        """
        )
        rows = self._db.execute_query(sql)
        return [self._row_to_dto(row) for row in rows]

    def get_team(self, codigo: str) -> NotificationTeamDTO:
        dto = self._fetch_team(
            """
            WHERE eq.codigo = :codigo
        """,
            codigo=codigo,
        )
        if dto is None:
            raise ValueError(f"Equipe '{codigo}' não encontrada")
        return dto

    def save_team(self, team: NotificationTeamDTO) -> NotificationTeamDTO:
        if team.equipe_id:
            sql = f"""
                UPDATE persona.automacoesdestinatarios
                   SET codigo = :codigo,
                       nome = :nome,
                       lastupdate = CURRENT_TIMESTAMP
                 WHERE destinatario = :destinatario
                 RETURNING destinatario
            """
            params = {
                "codigo": team.codigo,
                "nome": team.nome,
                "destinatario": team.equipe_id,
            }
        else:
            new_id = str(uuid.uuid4())
            sql = f"""
                INSERT INTO persona.automacoesdestinatarios (
                    destinatario,
                    codigo,
                    nome,
                    created_at,
                    lastupdate
                ) VALUES (
                    :destinatario,
                    :codigo,
                    :nome,
                    CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP
                )
                RETURNING destinatario
            """
            params = {
                "destinatario": new_id,
                "codigo": team.codigo,
                "nome": team.nome,
            }

        _, returning = self._db.execute(sql, **params)
        if not returning:
            raise RuntimeError("Falha ao salvar equipe")
        equipe_id = str(returning[0]["destinatario"])

        self._replace_users(equipe_id, team.emails)

        return self._fetch_team_by_id(equipe_id)

    def delete_team(self, codigo: str) -> None:
        equipe_id = self._get_team_id_by_code(codigo)

        self._db.execute(
            f"DELETE FROM persona.automacoesdestinatariosempresas WHERE destinatario = :destinatario",
            destinatario=equipe_id,
        )
        self._db.execute(
            f"DELETE FROM persona.automacoesdestinatariosusuarios WHERE destinatario = :destinatario",
            destinatario=equipe_id,
        )
        affected, _ = self._db.execute(
            f"DELETE FROM persona.automacoesdestinatarios WHERE destinatario = :destinatario",
            destinatario=equipe_id,
        )
        if affected == 0:
            raise ValueError(f"Equipe '{codigo}' não encontrada")

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #

    def _base_query(self) -> str:
        return f"""
            SELECT
                eq.destinatario,
                eq.codigo,
                eq.nome,
                COALESCE(string_agg(DISTINCT u.email, ', ' ORDER BY u.email), '') AS emails,
                COUNT(DISTINCT u.email) AS membros
            FROM persona.automacoesdestinatarios eq
            LEFT JOIN persona.automacoesdestinatariosusuarios u
              ON u.destinatario = eq.destinatario
        """

    def _fetch_team(self, where_clause: str, **params) -> Optional[NotificationTeamDTO]:
        sql = (
            self._base_query()
            + f"""
            {where_clause}
            GROUP BY eq.destinatario, eq.codigo, eq.nome
            LIMIT 1
        """
        )
        row = self._db.execute_query_first_result(sql, **params)
        if not row:
            return None
        return self._row_to_dto(row)

    def _fetch_team_by_id(self, equipe_id: str) -> NotificationTeamDTO:
        dto = self._fetch_team(
            """
            WHERE eq.destinatario = :destinatario
        """,
            destinatario=equipe_id,
        )
        if dto is None:
            raise RuntimeError("Equipe não encontrada após salvar")
        return dto

    def _replace_users(self, equipe_id: str, emails: str) -> None:
        self._db.execute(
            f"DELETE FROM persona.automacoesdestinatariosusuarios WHERE destinatario = :destinatario",
            destinatario=equipe_id,
        )
        cleaned = [email.strip() for email in emails.replace(";", ",").split(",") if email.strip()]
        if not cleaned:
            return

        insert_sql = f"""
            INSERT INTO persona.automacoesdestinatariosusuarios (
                destinatariousuario,
                destinatario,
                email,
                created_at,
                lastupdate
            ) VALUES (
                :destinatariousuario,
                :destinatario,
                :email,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
        """
        for email in cleaned:
            params = {
                "destinatariousuario": str(uuid.uuid4()),
                "destinatario": equipe_id,
                "email": email,
            }
            self._db.execute(insert_sql, **params)

    def _get_team_id_by_code(self, codigo: str) -> str:
        row = self._db.execute_query_first_result(
            f"SELECT destinatario FROM persona.automacoesdestinatarios WHERE codigo = :codigo",
            codigo=codigo,
        )
        if not row:
            raise ValueError(f"Equipe '{codigo}' não encontrada")
        return str(row["destinatario"])

    def _row_to_dto(self, row) -> NotificationTeamDTO:
        return NotificationTeamDTO(
            equipe_id=str(row.get("destinatario") or row.get("equipe") or ""),
            codigo=str(row.get("codigo") or ""),
            nome=str(row.get("nome") or ""),
            emails=str(row.get("emails") or ""),
            membros=int(row.get("membros") or 0),
        )
