import datetime

from nsj_pyRPA.resources.envConfig import getDb
from nsj_gcf_utils.json_util import json_dumps

class logconsumoapi():
    def __init__(self, 
                 a_started_at : datetime,
                 a_finished_at : datetime,
                 a_tenant : int,
                 a_caso_de_uso : str,
                 a_url : str,
                 a_filtros : dict,
                 a_qtd_registros : int):
        self.started_at = a_started_at
        self.finished_at = a_finished_at
        self.tenant = a_tenant
        self.caso_de_uso = a_caso_de_uso
        self.url = a_url
        self.filtros = a_filtros
        self.qtd_registros = a_qtd_registros


def InsereLogConsumoAPI(a_started_at : datetime,
                        a_finished_at : datetime,
                        a_tenant : int,
                        a_caso_de_uso : str,
                        a_url : str,
                        a_filtros : dict,
                        a_qtd_registros : int):
    _sql = """
            insert into ponto.logsconsumosapis(started_at, finished_at, tenant, casodeuso, url, filtros, qtdregistros) 
            values (:v_started_at, :v_finished_at, :v_tenant, :v_casodeuso, :v_url, :v_filtros, :v_qtdregistros)
        """            
    
    _retorno = getDb().execute(_sql, 
                               v_started_at=a_started_at, 
                               v_finished_at=a_finished_at, 
                               v_tenant=a_tenant, 
                               v_casodeuso=a_caso_de_uso, 
                               v_url=a_url,
                               v_filtros=json_dumps(a_filtros), 
                               v_qtdregistros=a_qtd_registros)
    
    return _retorno