from nsj_rest_lib.entity.entity_base import EntityBase

class RotinaAutomatizadaEntity(EntityBase):

    def __init__(self): 
        self.rotina = None
        self.codigo = None
        self.descricao = None
        self.processacalculo = None
        self.parametroprocessamentocalculo = None
        self.sincronizaesocial = None
        self.parametrosincronizacaoesocial = None
        #self.gerarelatorio = None
        #self.parametrogeracaorelatorio = None

    def get_table_name(self) :
        return 'persona.rotinas'
    
    def get_pk_field(self) :
        return 'rotina'
    
    def get_pk_column_name(self) :
        return 'rotina'

    def get_default_order_fields(self):
        return ['codigo'] 
        