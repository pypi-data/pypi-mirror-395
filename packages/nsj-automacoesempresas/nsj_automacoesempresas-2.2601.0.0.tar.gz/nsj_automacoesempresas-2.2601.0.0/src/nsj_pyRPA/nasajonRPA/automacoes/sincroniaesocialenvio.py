from nsj_pyRPA.resources.envConfig import EnvConfig, getLog

from nsj_pyRPA.nasajonRPA.automacoes.AbstractAutomacao import AbstractAutomacao

#"esocial:consultar-lote"

class SincroniaESocialEnvio(AbstractAutomacao):
    def __init__(self, a_escopo, a_faixa, a_tipo_evento, a_considera_excluido, a_considera_rejeitado):
        super().__init__()
        
        self.escopo = a_escopo
        self.faixacodigos = a_faixa
        self.tipo_evento = a_tipo_evento
        self.considera_excluido = a_considera_excluido
        self.considera_rejeitado = a_considera_rejeitado
        
    def NomeComando(self):
        return "esocial:enviar-evento"
        
    def GetNomeAutomacao(self)-> list:
        return "Sincronia eSocial - Envio de Eventos"

    def GetArgs(self)-> list:
        _fullArgs = [ "--empresa:" + self.faixacodigos ,
                      "--tipoeventoesocial:" + self.tipo_evento.upper() ]        

        return _fullArgs
