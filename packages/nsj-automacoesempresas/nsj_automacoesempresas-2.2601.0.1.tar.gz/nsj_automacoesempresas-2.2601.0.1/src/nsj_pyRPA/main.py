import argparse
import sys
import time
import base64
import traceback

#from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_pyRPA.resources.db_adapter3 import DBAdapter3
from nsj_pyRPA.resources.conexao_banco import create_pool
from nsj_pyRPA.resources.criptografia_erp2 import CriptografiaERP2
from nsj_pyRPA.resources.log import Log
from nsj_pyRPA.resources.envConfig import EnvConfig
from nsj_pyRPA.resources.const import *
from nsj_gcf_utils.json_util import json_loads
from nsj_pyRPA.resources.utils import formatar_tempo, get_version_number, MsgErro
from nsj_pyRPA import app as companies_app
from nsj_pyRPA import notification_teams_app

from nsj_pyRPA.pyRPA import pyRPA

import logging
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("nsj_gcf_utils").setLevel(logging.CRITICAL)


def internal_main(
    database_name: str,
    database_user: str,
    database_pass: str,
    database_host: str,
    database_port: str,
    entrada: dict,
    log: Log
):
    start_time = time.time()
    status_code = 0
    status_msg = None

    try:                 
        log.info(f"Conectando-se com o banco : {database_name}")

        if (database_user.lower() == 'postgres') and (database_user.lower() == 'postgres'):
            user_name = 'postgres'
            user_pass = 'postgres'
        else: # Criptografia removida para adequação aos parametros do jobmanager
            user_name = database_user.lower()
            user_pass = database_pass
            # user_pass = CriptografiaERP2().codificar(database_pass)

        # Criando o pool de conexoes
        pool = create_pool(
            user_name,
            user_pass,
            database_host,
            database_port,
            database_name
        )

        # Abrindo conexao com o BD
        with pool.connect() as conn:
            # Adicionando o pool de conexoes ao injector para uso nos services
            from nsj_rest_lib import injector_factory_base
            injector_factory_base.db_pool = pool  
            
            # Instanciando o DBAdapter
            db_adapter = DBAdapter3(conn)

            # Instanciar a class
            _automatizar = pyRPA()

            # Executando
            log.info("Iniciando execução do utilitário")
            status_code, status_msg = _automatizar.executar(
                                                        entrada,
                                                        job=None,
                                                        db=db_adapter,
                                                        log=log,
                                                        registro_execucao=log
                                                    )

        log.info("Utilitário encerrado")

        return status_code, status_msg
    finally:
        log.info("--- TEMPO TOTAL %s ---" % (formatar_tempo(time.time() - start_time)))


def main(params=None):
    log = None
    try: 
        if params is None:
            params = sys.argv[1:]
            ui_parser = argparse.ArgumentParser(add_help=False)
            ui_parser.add_argument("--empresas", action="store_true")
            ui_parser.add_argument("--notificacoes", action="store_true")
            ui_args, remainder = ui_parser.parse_known_args(params)

            if ui_args.empresas:
                return companies_app.main(remainder)
            if ui_args.notificacoes:
                return notification_teams_app.main(remainder)
        
        # No UI flags, Initialize direct parser    
        parser = argparse.ArgumentParser(
            description="""Utilitário para inserção de registros no banco."""
        )

        # Adding arguments
        parser.add_argument("-d", "--" + ent_data_base, help="Nome do banco de dados para conexão", required=True)
        parser.add_argument("-u", "--" + ent_user, help="Usuário para conexão com o banco de dados", required=True)
        parser.add_argument("-p", "--" + ent_password, help="Senha para conexão com o banco de dados", required=True)
        parser.add_argument("-t", "--" + ent_host, help="IP ou nome do servidor do banco de dados", required=True)
        parser.add_argument("-o", "--" + ent_port, help="Porta para conexão com o banco de dados", required=True)

        parser.add_argument("-r" , "--" + ent_rotina, help="Código da rotina que seja executada", required=False)
        parser.add_argument("-c" , "--" + ent_competencia, help="Competência de execução", required=False)
        parser.add_argument("-a" , "--" + ent_ano, help="Ano de execução", required=False)
        parser.add_argument("-s" , "--" + ent_semana, help="Semana de Cálculo", required=False)
        parser.add_argument("-sd", "--" + ent_semana_desc, help="Semana de Desconto Ad. Folha", required=False)
        
        parser.add_argument("-e", "--" + ent_escopo, help="Tipo de escopo de execução", required=False)
        parser.add_argument("-f", "--" + ent_faixa, help="Faixa de códigos do escopo", required=False)
        
        # Paramêtros do orquestrador de automações via job manager 
        parser.add_argument("-automacaotipo", "--automacaotipo", help="Tipo da automação via orquestrador", required=False)
        parser.add_argument("-automacaoempresaparametro", "--automacaoempresaparametro", help="ID dos parametros da automação", required=False)

        # Read arguments from command line or console
        if params is None:
            args = parser.parse_args()
        else:
            args = parser.parse_args(params)
            
        _database = args.database
        _user = args.user
        _password = args.password
        _host = args.host
        _port = args.port 

        EnvConfig.instance().set_dados_conexao(_database, _user, _password, _host, _port)
            
        # Instanciando o log
        log = Log(EnvConfig.instance().appName, None)   
        log.info("PyMeuRH - Versão " + get_version_number())

        entrada = {
            ent_user : args.user,
            ent_rotina : args.rotina,
            ent_competencia : args.competencia,
            ent_ano : args.ano,
            ent_semana : args.semana,
            ent_semana_desc : args.semanadesconto,
            ent_escopo : args.escopo,
            ent_faixa : args.faixa,
            automacaotipo : args.automacaotipo,
            automacaoempresaparametro : args.automacaoempresaparametro
        }

            # Calling internal main
        status_code, status_msg = internal_main(
                                    _database,
                                    _user,
                                    _password,
                                    _host,
                                    _port,
                                    entrada,
                                    log=log
                                )

        if status_msg is not None:
            if status_code > 2:
                log.erro(f'{status_msg}')
            else:
                log.atencao(f'{status_msg}')

        # sys.exit(status_code)
        return {'status': status_code, 'mensagem': status_msg}
    except Exception as e:
        if log is not None:
            log.erro(f'{e}')
            log.erro(traceback.format_exc())
            # sys.exit(3)
            raise Exception(f'{e}')

        MsgErro("Erro na inicialização do pyRPA.exe", traceback.format_exc()) 
        sys.exit(3)


if __name__ == '__main__':
    main()

