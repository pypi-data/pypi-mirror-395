from nsj_pyRPA.resources.envConfig import EnvConfig, getLog

from nsj_pyRPA.nasajonRPA.automacoes.AbstractAutomacao import AbstractAutomacao

class SincroniaESocialConsulta(AbstractAutomacao):
    def __init__(self, a_escopo, a_faixa):
        super().__init__()
        
        self.escopo = a_escopo
        self.faixacodigos = a_faixa
        
    def NomeComando(self):
        return "esocial:consultar-lote"
        
    def GetNomeAutomacao(self)-> list:
        return "Sincronia eSocial - Consulta de Lotes"

    def GetArgs(self)-> list:
        _fullArgs = [ "--empresa:" + self.faixacodigos ]        

        return _fullArgs
