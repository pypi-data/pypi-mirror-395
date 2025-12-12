from nsj_pyRPA.nasajonRPA.automacoes.AbstractAutomacao import AbstractAutomacao
from nsj_pyRPA.resources.utils import to_bool

""" --database:integratto_master 
    --servidor:localhost 
    --porta:5432 
    --user:USER 
    --password:PASSWORD 
    folha:processar-calculo 
    --empresa:01 
    --ano:2025 
    --mes:6
"""

class ProcessamentoCalculoFerias(AbstractAutomacao):
    def __init__(self, a_escopo, a_faixa, a_mes, a_ano, a_ferias_em_dobro, a_atualiza_pa):
        super().__init__()
        
        self.escopo = a_escopo
        self.faixacodigos = a_faixa
        self.mes = a_mes if a_mes is not None else 0
        self.ano = a_ano if a_ano is not None else 0
        self.ferias_em_dobro = to_bool(a_ferias_em_dobro, "-1") # -1 = true, 0 = false
        self.atualiza_pa = to_bool(a_atualiza_pa, "-1") # -1 = true, 0 = false

    def NomeComando(self):
        return "ferias:processar-calculo"
        
    def GetNomeAutomacao(self)-> list:
        return "Processamento Calculo de Férias"

    def GetArgs(self)-> list:
        _fullArgs = [ "--empresa:"  + self.faixacodigos ,
                      "--ano:"      + self.ano ,
                      "--mes:"      + self.mes ]
        
        if self.ferias_em_dobro:
            _fullArgs = _fullArgs + ["--feriasemdobro" ]

        if self.atualiza_pa:
            _fullArgs = _fullArgs + ["--atualizapa" ]

        return _fullArgs
