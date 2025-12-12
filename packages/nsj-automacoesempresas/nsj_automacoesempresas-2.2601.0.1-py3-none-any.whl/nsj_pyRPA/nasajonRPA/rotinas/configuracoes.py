from nsj_pyRPA.resources.utils import to_int
from nsj_pyRPA.resources.envConfig import getDb
from nsj_pyRPA.resources.const import *

def RecuperaVersaoPostgresSQL():
    _consulta = getDb().execute_query("show server_version_num")

    if len(_consulta) > 0:
        _version = to_int(_consulta[0]["server_version_num"])
    else :
        _version = 0
    
    return _version


def AtualizaOuInsereConfiguracao(a_campo : int, a_valor : any, a_empresa : str=None, a_grupo : str=None):
    if a_empresa is not None:
        return AtualizaOuInsereConfiguracaoEmpresa(a_empresa, a_campo, a_valor)
    elif a_grupo is not None:
        return AtualizaOuInsereConfiguracaoGrupoEmpresarial(a_grupo, a_campo, a_valor)
    
    _sql = """
            update ns.configuracoes set valor = :valor 
            where (aplicacao = 1) and (grupo = 48) and (campo = :campo)
        """
        
    _returno = getDb().execute(_sql, valor=a_valor, campo=a_campo)

    if (_returno is None) or (len(_returno) == 0) or (_returno[0] == 0):
        _sql = """
                insert into ns.configuracoes(aplicacao, grupo, campo, valor) 
                values (1, 48, :campo, :valor)
            """
            
        _returno = getDb().execute(_sql, valor=a_valor, campo=a_campo)

    return _returno


def AtualizaOuInsereConfiguracaoEmpresa(a_empresa : str, a_campo : int, a_valor : any):
    _sql = """
            update ns.configuracoes set valor = :valor 
            where (aplicacao = 1) and (grupo = 48) and (campo = :campo) and (empresa = :empresa)
        """
    
    _returno = getDb().execute(_sql, valor=a_valor, campo=a_campo, empresa=a_empresa)

    if  (_returno is None) or (len(_returno) == 0) or (_returno[0] == 0):
        _sql = """
                insert into ns.configuracoes(aplicacao, grupo, campo, empresa, valor) 
                values (1, 48, :campo, :empresa, :valor)
            """
        
        _returno = getDb().execute(_sql, campo=a_campo, empresa=a_empresa, valor=a_valor)

    return _returno


def AtualizaOuInsereConfiguracaoGrupoEmpresarial(a_grupo : str, a_campo : int, a_valor : any):
    _sql = """
            update ns.configuracoes set valor = :valor 
            where (aplicacao = 1) and (grupo = 48) and (campo = :campo) and (grupoempresarial = :id_grupo)
        """
    
    _returno = getDb().execute(_sql, valor=a_valor, campo=a_campo, id_grupo=a_grupo)

    if  (_returno is None) or (len(_returno) == 0) or (_returno[0] == 0):
        _sql = """
                insert into ns.configuracoes(aplicacao, grupo, campo, grupoempresarial, valor) 
                values (1, 48, :campo, :id_grupo, :valor)
            """
        
        _returno = getDb().execute(_sql, campo=a_campo, id_grupo=a_grupo, valor=a_valor)

    return _returno 


def RecuperaConfiguracao(a_campo : int, a_empresa : str=None, a_grupoempresarial : str=None):
    _sql = "select valor from ns.configuracoes where aplicacao = 1 and grupo = 48 and campo = :campo"

    if a_empresa is not None:
        _sql = _sql + " and (empresa = :empresa)"
        _consulta = getDb().execute_query(_sql, campo=a_campo, empresa=a_empresa) 
    elif a_grupoempresarial is not None:
        _sql = _sql + " and (grupoempresarial = :id_grupo)"
        _consulta = getDb().execute_query(_sql, campo=a_campo, id_grupo=a_grupoempresarial) 
    else :
        _consulta = getDb().execute_query(_sql, campo=a_campo)

    if len(_consulta) > 0:
        return _consulta[0]["valor"]
    else :
        return None
