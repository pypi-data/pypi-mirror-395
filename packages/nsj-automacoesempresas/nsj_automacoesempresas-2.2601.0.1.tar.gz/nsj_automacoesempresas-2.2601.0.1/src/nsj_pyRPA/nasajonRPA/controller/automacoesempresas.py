from nsj_pyRPA.resources.envConfig import getDb
from nsj_pyRPA.repositories.company_settings_repository import DbCompanySettingsRepository

import ast, re
from nsj_gcf_utils.json_util import json_loads
from nsj_pyRPA.resources.const import *
    
def RecuperaAutomacoesEmpresas(automacaoempresaparametro : str, automacaotipo : str) -> dict:
    
    _filtros = {}
    _filtros = {"automacaoempresaparametro": automacaoempresaparametro, "tipo": automacaotipo}
    
    if len(_filtros) == 0:
        _filtros = None

    _db_adapter = getDb()
    if _db_adapter is None:
        raise RuntimeError("Conexão com o banco não configurada.")

    _lst = DbCompanySettingsRepository(db_adapter=_db_adapter).list_company_parameters(_filtros)
    
    if len(_lst) == 1:
        return _lst[0]
    if len(_lst) == 2:
        raise Exception("Mais de uma configuração de automações foi encontrada.")    
    else:        
        raise Exception("Não foi localizada configuração de automações.")
