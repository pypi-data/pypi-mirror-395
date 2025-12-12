from nsj_pyRPA.resources.db_adapter3 import DBAdapter3
from nsj_pyRPA.resources.envConfig import EnvConfig, getLog, getVersaoMinimaAtendida
from nsj_pyRPA.resources.locking_banco import *

from nsj_pyRPA.nasajonRPA.rotinas.configuracoes import *
from nsj_pyRPA.nasajonRPA.orquestrador import Orquestrar

class pyRPA:

    def __init__(self):
        pass

    def processar(self, a_roteiro):        
        status_code = 0
        tem_sucesso = False
        status_msg = None
        
        for item in a_roteiro :
            aux_sts_code, aux_sts_msg = item.Processa()

            if aux_sts_code == 3:
                status_code = aux_sts_code
                status_msg = aux_sts_msg
                break
            
            if aux_sts_msg is not None:
                if status_msg is not None:
                    status_msg = status_msg + "\n" + aux_sts_msg
                else:
                    status_msg = aux_sts_msg
                
            if aux_sts_code == 0 :
                tem_sucesso = True
            else:
                status_code = aux_sts_code

        if aux_sts_code == 3:
            return status_code, status_msg   
        
        if tem_sucesso :
            if (status_code != 0) and (status_msg is not None):
                status_code = 1
                status_msg = "Alguns processos foram executados com sucesso. " + "\n" + status_msg
        else :
            status_code = 2

        return status_code, status_msg 

    def executar(self, entrada: dict, job, db: DBAdapter3, log, registro_execucao):
        EnvConfig.instance().set_log(log)
        EnvConfig.instance().set_db(db)     

        if not getVersaoMinimaAtendida():
            log.atencao("Verificamos que a versão do PostgreSQL esta desatualiza, para melhor " +
                        "execução do utilitário recomendamos sua atualização para a versão 9.5.25+")            

        log.info("Verificando se há locks no banco para a rotina")
        if not advisory_lock():
            return 3, ("Não foi possível iniciar as rotinas do pyRPA "+
                       "pois outro processo já esta em execução. Favor aguardar.")
        
        try:
            DetalhaEntradasLog(entrada)
                        
            log.info("Orquestrando Operações")
            _roteiro = Orquestrar(entrada)

            status_code, status_msg = self.processar(_roteiro)

            return status_code, status_msg 
        finally:
            advisory_unlock()  
            

def DetalhaEntradasLog(a_entrada):
    getLog().info("Entrada de dados:")
    #getLog().info(f"    Empresa {RecuperaCodigoEmpresa(a_entrada.get(ent_empresa, None))}")
