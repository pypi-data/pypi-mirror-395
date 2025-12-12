import os
import pathlib
import uuid

from nsj_pyRPA.resources.const import *
from nsj_pyRPA.resources.utils import *

class EnvConfig:
    DIR_EXECUCAO = "pyRPA"

    _instance = None

    def __init__(self):
        
        self.appName = "PYRPA"
        
        self.dir_execucao = self._trata_diretorio_execucao()
        self.log_path = self.appName + "_LOGS"
        self.log_level = os.getenv("log_level", "INFO")
        self.notimelog = to_bool( os.getenv("NO_TIME_LOG", "False") )
        self.id_execucao = uuid.uuid4()

        self.database_name = ""
        self.database_user = ""
        self.database_pass = ""
        self.database_host = ""
        self.database_port = 0
        
        self.version_postgres = None
        self.auth = None
        self.log = None
        self.db = None
        self.webconfiguracoes = None
    
    def set_log(self, a_log) : 
        self.log = a_log

    def set_db(self, a_db) : 
        self.db = a_db 

    def set_dados_conexao(self, a_database_name, a_database_user, a_database_pass, a_database_host, a_database_port):
        self.database_name = a_database_name
        self.database_user = a_database_user
        self.database_pass = a_database_pass
        self.database_host = a_database_host
        self.database_port = a_database_port

    def getDataBase_name(self):
        return self.database_name

    def getDataBase_user(self):
        return self.database_user

    def getDataBase_pass(self):
        return self.database_pass

    def getDataBase_host(self):
        return self.database_host

    def getDataBase_port(self):
        return self.database_port

    def define_autenticacao(self, a_auth):
        self.auth = a_auth

    def _trata_diretorio_execucao(self):
        # Recupera diretório de usuário:
        user_home = pathlib.Path.home()

        # Monta path do diretório de configurações:
        dir_job_manager = user_home / EnvConfig.DIR_EXECUCAO

        # Criando o diretório do JobManager, se necessário:
        if not os.path.exists(dir_job_manager):
            os.makedirs(dir_job_manager)

        return dir_job_manager

    @staticmethod
    def instance():
        if (EnvConfig._instance == None):
            EnvConfig._instance = EnvConfig()

        return EnvConfig._instance
        

def getDb():
    return EnvConfig.instance().db


def getLog():
    return EnvConfig.instance().log


def getVersaoMinimaAtendida():
    if EnvConfig.instance().version_postgres is None:
        from nsj_pyRPA.nasajonRPA.rotinas.configuracoes import RecuperaVersaoPostgresSQL
        EnvConfig.instance().version_postgres = RecuperaVersaoPostgresSQL()

    return EnvConfig.instance().version_postgres >= VERSAO_MINIMA_POSTGRES
