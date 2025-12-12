from nsj_pyRPA.nasajonRPA.automacoes.AbstractAutomacao import AbstractAutomacao

""" --database:integratto_master 
    --servidor:localhost 
    --porta:5432 
    --user:USER 
    --password:PASSWORD 
    adfolha:processar-calculo 
    --empresa:01 
    --ano:2025 
    --mes:6
"""

class ProcessamentoCalculoAdiantamentoFolha(AbstractAutomacao):
    def __init__(self, a_escopo, a_faixa, a_mes, a_ano, a_semana, a_semanadesconto, a_situacoes):
        super().__init__()
        
        self.escopo = a_escopo
        self.faixacodigos = a_faixa
        self.mes = a_mes if a_mes is not None else 0
        self.ano = a_ano if a_ano is not None else 0
        self.semana = a_semana if a_semana is not None else 0
        self.semana_desc = a_semanadesconto if a_semanadesconto is not None else 0
        self.situacoes = a_situacoes

    def NomeComando(self):
        return "adfolha:processar-calculo"
        
    def GetNomeAutomacao(self)-> list:
        return "Processamento Calculo de Adiantamento de Folha"

    def GetArgs(self)-> list:
        _fullArgs = [ "--empresa:"  + self.faixacodigos ,
                      "--ano:"      + self.ano ,
                      "--mes:"      + self.mes ,
                      "--situacoes:"+ self.situacoes ]
        
        if self.semana > 0:
            _fullArgs = _fullArgs + ["--semana:" + self.semana]
        
        if self.semana_desc > 0:
            _fullArgs = _fullArgs + ["--semanadesconto:" + self.semana_desc]

        return _fullArgs
