import ast, re
from datetime import date, datetime, timedelta

from nsj_gcf_utils.json_util import json_loads

from nsj_pyRPA.resources.const import *
import nsj_pyRPA.resources.automation_types as automation_types

from nsj_pyRPA.nasajonRPA.automacoes.processamentocalculofolha import ProcessamentoCalculoFolha
from nsj_pyRPA.nasajonRPA.automacoes.processamentocalculoadiantamentofolha import ProcessamentoCalculoAdiantamentoFolha
from nsj_pyRPA.nasajonRPA.automacoes.processamentocalculoferias import ProcessamentoCalculoFerias

from nsj_pyRPA.nasajonRPA.automacoes.sincroniaesocialenvio import SincroniaESocialEnvio
from nsj_pyRPA.nasajonRPA.automacoes.sincroniaesocialconsulta import SincroniaESocialConsulta
from nsj_pyRPA.nasajonRPA.controller.rotinaautomatizada import RecuperaRotinaAutomatizada
from nsj_pyRPA.nasajonRPA.controller.automacoesempresas import RecuperaAutomacoesEmpresas
from nsj_pyRPA.services.company_settings_service import CompanySettingsService

opConsideraExcluido = "consideraeventoexcluido"
opConsideraRejeitado = "consideraeventorejeitado"


def Orquestrar(a_entrada : dict):
    
    _automacoes = []
    
    if a_entrada.get('automacaoempresaparametro') is not None:
        _automacoesempresa = RecuperaAutomacoesEmpresas(a_entrada[automacaoempresaparametro], a_entrada[automacaotipo])
        
        if _automacoesempresa.get('tipo') in automation_types.CALC_TYPES:
            _automacoes.extend( OrquestrarAutomacoesEmpresasCalculo(_automacoesempresa, _automacoesempresa.get('parametros')) )
        return _automacoes
    
    _rotina = RecuperaRotinaAutomatizada(a_entrada[ent_rotina].upper())

    if _rotina.processacalculo:
        _automacoes.extend( OrquestrarProcessamentoCalculo(a_entrada, _rotina.parametroprocessamentocalculo) )
    
    if _rotina.sincronizaesocial:
        _automacoes.extend( OrquestrarSincroniaESocial(a_entrada, _rotina.parametrosincronizacaoesocial) )
    
    if False :#_rotina.sincronizaesocialConsulta:
        _automacoes.extend( [SincroniaESocialConsulta(a_escopo=a_entrada[ent_escopo], a_faixa=a_entrada[ent_faixa] )] )
    
    
    return _automacoes

def OrquestrarSincroniaESocial(a_entrada : dict, a_parametros):
    _automacoes = []
    _parametros = json_loads( ast.literal_eval( a_parametros ) )

    _considera_excluido = opConsideraExcluido in _parametros
    _considera_rejeitado = opConsideraRejeitado in _parametros

    for chave, valor in _parametros.items(): # rodar a cada uma hora, view para verificar se pode rodar automaticamente
        if bool(re.fullmatch(r"S-\d{4}", chave)):
            _automacoes.append( SincroniaESocialEnvio(a_escopo=a_entrada[ent_escopo],
                                                      a_faixa=a_entrada[ent_faixa],
                                                      a_tipo_evento=chave,
                                                      a_considera_excluido=_considera_excluido, 
                                                      a_considera_rejeitado=_considera_rejeitado ) ) 
            
    return _automacoes

def OrquestrarProcessamentoCalculo(a_entrada : dict, a_parametros):
    _automacoes = []

    _parametros = json_loads( ast.literal_eval( a_parametros ) )

    for chave, valor in _parametros.items():
        if chave == "Fo":
            _automacoes.append( ProcessamentoCalculoFolha( a_escopo=a_entrada[ent_escopo],
                                                           a_faixa=a_entrada[ent_faixa],
                                                           a_mes=a_entrada[ent_competencia],
                                                           a_ano=a_entrada[ent_ano],
                                                           a_semana=a_entrada[ent_semana],
                                                           a_situacoes=valor["situacoes"] ) )
            
        if chave == "Ad":
            _automacoes.append( ProcessamentoCalculoAdiantamentoFolha( a_escopo=a_entrada[ent_escopo],
                                                                       a_faixa=a_entrada[ent_faixa],
                                                                       a_mes=a_entrada[ent_competencia],
                                                                       a_ano=a_entrada[ent_ano],
                                                                       a_semana=a_entrada[ent_semana],
                                                                       a_semanadesconto=a_entrada[ent_semana_desc],
                                                                       a_situacoes=valor["situacoes"] ) )
            
        if chave == "Fe":
            _automacoes.append( ProcessamentoCalculoFerias( a_escopo=a_entrada[ent_escopo],
                                                            a_faixa=a_entrada[ent_faixa],
                                                            a_mes=a_entrada[ent_competencia],
                                                            a_ano=a_entrada[ent_ano],
                                                            a_ferias_em_dobro=valor["ferias_em_dobro"],
                                                            a_atualiza_pa=valor["atualizar_pa"]  ) )
            
    return _automacoes


def OrquestrarAutomacoesEmpresasCalculo(a_entrada: dict, _parametros):
    _automacoes = []
    
    data_agendamento = a_entrada.get('agendamento')
    atraso_aceito = a_entrada.get('atrasoaceito', 0)
    hoje = datetime.now()
    
    if data_agendamento is None: raise Exception('A operação não pode ser realizada sem data de agendamento definida.')
    
    limite = data_agendamento + timedelta(minutes=atraso_aceito)
    
    if not hoje >= data_agendamento and hoje <= limite: raise Exception('A operação não está agendada para o presente momento.');

    if a_entrada.get('tipo') == automation_types.AUTOMATION_TYPE_EMPLOYEES:
        _automacoes.append( ProcessamentoCalculoFolha(
            a_escopo='EMPRESA',
            a_faixa=a_entrada.get('codigo'),
            a_mes=str(data_agendamento.month),
            a_ano=str(data_agendamento.year),
            a_semana=None,
            a_situacoes=a_entrada.get('situacoes', "01,03..17") # variavel, adicionar arg na main
        ))
    
    return _automacoes