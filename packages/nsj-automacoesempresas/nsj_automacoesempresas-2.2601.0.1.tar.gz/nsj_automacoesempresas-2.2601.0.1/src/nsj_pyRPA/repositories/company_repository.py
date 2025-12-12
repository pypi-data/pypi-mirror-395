from __future__ import annotations

from typing import Dict, List, Optional, Protocol

from nsj_pyRPA.dto.company_dto import CompanyDTO
from nsj_pyRPA.services.company_service import CompanyRepository


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    return text in {"1", "true", "t", "y", "yes", "sim", "s"}


class DbCompanyRepository(CompanyRepository):
    """Database-backed implementation that reads companies from Persona tables."""

    def __init__(self, db_adapter):
        self._db = db_adapter

    def list_companies(self) -> List[CompanyDTO]:
        sql = f"""
            SELECT
                e.codigo AS codigo,
                e.razaosocial AS nome,
                e.empresa as empresa,
                e.tenant AS tenant,
                ae.automacaoempresa AS automacaoempresa,
                ae.padrao AS padrao,
                ae.ativo AS ativo,
                ae.usapadrao AS use_default
            FROM ns.empresas e
            LEFT JOIN persona.automacoesempresas ae
            ON ae.empresa = e.empresa
            ORDER BY e.codigo
        """
        rows = self._db.execute_query(sql)
        return [
            CompanyDTO(
                codigo=str(row["codigo"]),
                nome=str(row.get("nome") or ""),
                padrao=_to_bool(row.get("padrao")),
                ativo=_to_bool(row.get("ativo", True)),
                empresa=str(row.get("empresa")),
                automacaoempresa=row.get("automacaoempresa"),
                tenant=int(row.get("tenant")),
                use_default=_to_bool(row.get("use_default")),
                notified_teams=str(row.get("notified_teams") or ""),
            )
            for row in rows
        ]
        
    def get_company_by_id(self, empresa_id: str) -> CompanyDTO:
        sql = f"""
            SELECT
                e.codigo AS codigo,
                e.razaosocial AS nome,
                e.empresa  AS empresa,
                e.tenant AS tenant,
                ae.padrao AS padrao,
                ae.usapadrao AS use_default,
                ae.automacaoempresa AS automacaoempresa,
                ae.ativo AS ativo
            FROM ns.empresas e
            LEFT JOIN persona.automacoesempresas ae
              ON ae.empresa = e.empresa
            WHERE e.empresa = :empresa
        """
        row = self._db.execute_query_first_result(sql, empresa=empresa_id)
        if row is None:
            raise ValueError(f"Empresa '{empresa_id}' não encontrada")

        return CompanyDTO(
            codigo=str(row["codigo"]),
            nome=str(row.get("nome") or ""),
            padrao=_to_bool(row.get("padrao")),
            ativo=_to_bool(row.get("ativo", True)),
            empresa=str(row["empresa"]),
            automacaoempresa=row.get("automacaoempresa"),
            tenant=int(row.get("tenant")),
            use_default=_to_bool(row.get("use_default")),
            notified_teams=str(row.get("notified_teams") or ""),
        )

        
    def save_company(self, company: CompanyDTO) -> CompanyDTO:
        columns = [
            "empresa",
            "codigo",
            "nome",
            "ativo",
            "padrao",
            "tenant",
            "usapadrao",
            # "equipesnotificadas",
        ]
        values = [
            ":empresa",
            ":codigo",
            ":nome",
            ":ativo",
            ":padrao",
            ":tenant",
            ":use_default",
            # ":notified_teams",
        ]
        updates = [
            "ativo = :ativo",
            "padrao = :padrao",
            "usapadrao = :use_default",
            # "equipesnotificadas = :notified_teams",
        ]

        sql = f"""    
            INSERT INTO persona.automacoesempresas (
                {', '.join(columns)}
            ) VALUES (
                {', '.join(values)}
            ) ON CONFLICT (empresa)
            DO UPDATE
                SET {', '.join(updates)}
            RETURNING empresa;
        """

        params = {
            "empresa": company.empresa,
            "codigo": company.codigo,
            "nome": company.nome,
            "ativo": company.ativo,
            "padrao": company.padrao,
            "tenant": company.tenant,
            "use_default": company.use_default,
            # "notified_teams": company.notified_teams,
        }

        affected, returning = self._db.execute(sql, **params)
        print("affected:", affected, "returning:", returning)
        if not returning:
            raise RuntimeError("Insert/update did not return data")

        empresa = returning[0]["empresa"]
        
        updated = self.get_company_by_id(empresa)
        return updated
