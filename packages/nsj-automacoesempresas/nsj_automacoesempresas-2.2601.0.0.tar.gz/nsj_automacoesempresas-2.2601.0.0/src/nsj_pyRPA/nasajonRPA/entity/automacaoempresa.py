from nsj_rest_lib.entity.entity_base import EntityBase

class AutomacaoEmpresaEntity(EntityBase):

    def __init__(self): 
        self.automacaoempresa = None
        self.codigo = None
        self.nome = None
        self.tenant = None
        self.empresa = None
        self.ativo = None
        self.padrao = None
        self.usapadrao = None

    def get_table_name(self) :
        return 'persona.automacoesempresas'
    
    def get_pk_field(self) :
        return 'automacaoempresa'
    
    def get_pk_column_name(self) :
        return 'automacaoempresa'

    def get_default_order_fields(self):
        return ['codigo'] 
        