from nsj_rest_lib.entity.entity_base import EntityBase

class AutomacaoEmpresaParametroEntity(EntityBase):

    def __init__(self): 
        self.automacaoempresaparametro = None
        self.tipo = None
        self.automacaoempresa = None
        self.parametros = None
        self.jobschedule = None
        self.ativo = None
        self.usapadrao = None

    def get_table_name(self) :
        return 'persona.automacoesempresasparametros'
    
    def get_pk_field(self) :
        return 'automacaoempresaparametro'
    
    def get_pk_column_name(self) :
        return 'automacaoempresaparametro'

    def get_default_order_fields(self):
        return ['tipo'] 
        