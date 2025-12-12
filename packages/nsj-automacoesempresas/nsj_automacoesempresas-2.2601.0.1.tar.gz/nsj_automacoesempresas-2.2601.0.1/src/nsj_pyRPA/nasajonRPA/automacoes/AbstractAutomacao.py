import subprocess
import os
from pathlib import Path

from nsj_pyRPA.resources.envConfig import EnvConfig, getLog
from nsj_pyRPA.resources.const import UTILITARIO_PERSONACLI, UTILITARIO_PERSONACLI_DEB

class AbstractAutomacao():
    def __init__(self):
        pass     

    def GetNomeAutomacao(self)-> list:
        raise Exception("Método GetNomeAutomacao() não implementado na classe filha")

    def GetArgs(self)-> list:
        raise Exception("Método GetArgs() não implementado na classe filha")        

    def GetNomeExecutavel(self):
        _path = Path(os.environ.get("PATH_PERSONACLI", UTILITARIO_PERSONACLI))

        if not _path.exists():
            raise Exception("Utilitário personacli.exe não localizado")

        return _path
    
    def GetArgsPadrao(self):
        return [self.GetNomeExecutavel() ,
                "--database:" + EnvConfig.instance().getDataBase_name() ,
                "--servidor:" + EnvConfig.instance().getDataBase_host() ,
                "--porta:"    + EnvConfig.instance().getDataBase_port() ,
                "--user:"     + EnvConfig.instance().getDataBase_user() ,
                "--password:" + EnvConfig.instance().getDataBase_pass() ]

    def Processa(self):
        status_code = 0
        status_msg = None

        try:
            try:
                getLog().info(f"Executando automação {self.GetNomeAutomacao()}")

                _fullArgs = self.GetArgsPadrao() + [ self.NomeComando() ] + self.GetArgs()

                subprocess.run( _fullArgs )

                return status_code, status_msg
            except Exception as e:
                return 3, f"[{self.GetNomeAutomacao()}] {e}"
        finally:
            pass
            #self.AoTerminar()