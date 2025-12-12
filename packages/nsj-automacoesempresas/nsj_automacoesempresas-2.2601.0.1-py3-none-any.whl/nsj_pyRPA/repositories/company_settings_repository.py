from __future__ import annotations

import json
from typing import Dict, List, Optional

from nsj_pyRPA.dto.jobschedule_dto import JobScheduleDTO


class DbCompanySettingsRepository:
    """Low-level persistence for persona.automacoesempresasparametros and util.jobschedule."""

    def __init__(self, db_adapter):
        self._db = db_adapter
        self._automacoes_jobtype_id: Optional[str] = None

    def fetch_active_settings(self, company_code: str) -> List[Dict]:
        sql = """
            SELECT
                aep.tipo AS tipo,
                aep.parametros AS parametros
            FROM persona.automacoesempresasparametros aep
            WHERE aep.automacaoempresa = :automacaoempresa
              AND aep.ativo IS TRUE
            ORDER BY aep.lastupdate DESC
        """
        rows = self._db.execute_query(sql, automacaoempresa=company_code)
        return [
            {
                "tipo": str(row.get("tipo") or ""),
                "parametros": self._coerce_payload(row.get("parametros")),
            }
            for row in rows
        ]

    def list_existing_types(self, company_code: str) -> set[str]:
        sql = """
            SELECT tipo
            FROM persona.automacoesempresasparametros
            WHERE automacaoempresa = :automacaoempresa
        """
        rows = self._db.execute_query(sql, automacaoempresa=company_code)
        return {str(row["tipo"]) for row in rows if row.get("tipo")}
    
    def list_company_parameters(self, parameters: dict) -> List[Dict]:
        sql = """
            SELECT
                a.codigo,
                a.automacaoempresa,
                a.nome,
                a.empresa,
                ap.jobschedule,
                ap.parametros,
                ap.tipo,
                ap.automacaoempresaparametro,
                js.agendamento,
                js.atrasoaceito
            FROM persona.automacoesempresas a
            INNER JOIN persona.automacoesempresasparametros ap
                ON a.automacaoempresa = ap.automacaoempresa 
            INNER JOIN util.jobschedule js 
                ON ap.jobschedule = js.jobschedule
            WHERE ap.automacaoempresaparametro = :automacaoempresaparametro
                AND ap.tipo = :tipo
                AND ap.ativo IS TRUE
            LIMIT 1;
        """
        return self._db.execute_query(sql, automacaoempresaparametro=parameters.get('automacaoempresaparametro'), tipo=parameters.get('tipo'))

    def upsert_parameter(
        self,
        company_code: str,
        automation_type: str,
        payload: str,
        ativo: bool,
    ) -> Dict:
        sql = """
            INSERT INTO persona.automacoesempresasparametros (
                automacaoempresa,
                tipo,
                parametros,
                ativo
            ) VALUES (
                :automacaoempresa,
                :tipo,
                :payload,
                :ativo
            )
            ON CONFLICT (automacaoempresa, tipo)
            DO UPDATE SET
                parametros = EXCLUDED.parametros,
                ativo = EXCLUDED.ativo,
                lastupdate = CURRENT_TIMESTAMP
            RETURNING automacaoempresaparametro, jobschedule
        """
        params = {
            "automacaoempresa": company_code,
            "tipo": automation_type,
            "payload": payload,
            "ativo": ativo,
        }
        _, returning = self._db.execute(sql, **params)
        if not returning:
            raise RuntimeError("Falha ao persistir parametros de automacao")
        return returning[0]

    def save_job_schedule(self, parametro_id, job: JobScheduleDTO) -> Optional[str]:
        if job.jobschedule:
            return self._update_job_schedule(job)

        new_job_id = self._insert_job_schedule(job)
        if new_job_id:
            self._link_job_schedule(parametro_id, new_job_id)
        return new_job_id

    def _insert_job_schedule(self, job: JobScheduleDTO) -> Optional[str]:
        sql = """
            INSERT INTO util.jobschedule (
                jobtype,
                entrada,
                status,
                tipoagendamento,
                agendamento,
                tenant,
                codigo,
                expressaocron
            ) VALUES (
                :jobtype,
                :entrada::json,
                :status,
                :tipoagendamento,
                :agendamento,
                :tenant,
                :codigo,
                :expressaocron
            )
            RETURNING jobschedule
        """
        params = self._job_schedule_params(job)
        params.pop("jobschedule", None)
        _, returning = self._db.execute(sql, **params)
        if not returning:
            return None
        return str(returning[0]["jobschedule"])

    def _update_job_schedule(self, job: JobScheduleDTO) -> Optional[str]:
        sql = """
            UPDATE util.jobschedule
            SET
                jobtype = :jobtype,
                entrada = :entrada::json,
                status = :status,
                tipoagendamento = :tipoagendamento,
                agendamento = :agendamento,
                tenant = :tenant,
                codigo = :codigo,
                expressaocron = :expressaocron,
                lastupdate = CURRENT_TIMESTAMP
            WHERE jobschedule = :jobschedule
            RETURNING jobschedule
        """
        params = self._job_schedule_params(job)
        _, returning = self._db.execute(sql, **params)
        if not returning:
            return None
        return str(returning[0]["jobschedule"])

    def _job_schedule_params(self, job: JobScheduleDTO) -> Dict:
        entrada_json = json.dumps(job.entrada or {})
        return {
            "jobschedule": job.jobschedule,
            "jobtype": job.jobtype,
            "entrada": entrada_json,
            "status": job.status,
            "tipoagendamento": job.tipoagendamento,
            "agendamento": job.agendamento,
            "tenant": job.tenant,
            "codigo": job.codigo,
            "expressaocron": job.expressaocron,
        }

    def _link_job_schedule(self, parametro_id, jobschedule_id: str) -> None:
        sql = """
            UPDATE persona.automacoesempresasparametros
            SET jobschedule = :jobschedule
            WHERE automacaoempresaparametro = :parametro_id
        """
        self._db.execute(sql, jobschedule=jobschedule_id, parametro_id=parametro_id)

    def automation_jobtype(self) -> str:
        if self._automacoes_jobtype_id:
            return self._automacoes_jobtype_id

        sql = """
            SELECT jobtype
            FROM util.jobtypes
            WHERE codigo = :codigo
            LIMIT 1
        """
        rows = self._db.execute_query(sql, codigo="AUTOMACOES_EMPRESAS")
        if not rows:
            raise RuntimeError("jobtype 'AUTOMACOES_EMPRESAS' not found in util.jobtypes")
        self._automacoes_jobtype_id = str(rows[0]["jobtype"])
        return self._automacoes_jobtype_id

    @staticmethod
    def _coerce_payload(payload) -> Dict:
        if payload is None:
            return {}
        if isinstance(payload, str):
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                return {}
        return payload
