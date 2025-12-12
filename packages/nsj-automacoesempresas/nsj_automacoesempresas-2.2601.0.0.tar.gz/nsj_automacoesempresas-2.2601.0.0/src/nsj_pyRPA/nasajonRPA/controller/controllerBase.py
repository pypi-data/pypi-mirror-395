import uuid

from nsj_rest_lib.dao.dao_base import DAOBase
from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.service.service_base import ServiceBase
from nsj_rest_lib import injector_factory_base
from nsj_gcf_utils.json_util import convert_to_dumps
from nsj_pyRPA.resources.envConfig import getDb, getVersaoMinimaAtendida

class ControllerBase():    
    def __init__(self):
        self._service = ServiceBase(injector_factory=injector_factory_base.NsjInjectorFactoryBase(),
                               dao=DAOBase(getDb(), self.getEntityType()),
                               dto_class=self.getDTOType(),
                               entity_class=self.getEntityType()) 
        
    
    def getEntityType(self):
        """Função que retorna o tipo de entidade da especialização, sem instancia-la
           Deve ser implementado nas classes filhas"""
        raise Exception("Método getEntityType() não implmentado na classe fila")
    
    
    def getDTOType(self):
        """Função que retorna o tipo de entidade da especialização, sem instancia-la
           Deve ser implementado nas classes filhas"""
        raise Exception("Método getDTOType() não implmentado na classe fila")
    
    
    def getEntityIstance(self):
        """Função que retorna o tipo de entidade da especialização, em forma de instancia"""
        return self.getEntityType()()
    
    def getDTOIstance(self):
        """Função que retorna o tipo de DTO da especialização, em forma de instancia"""
        return self.getDTOType()()
        
    
    def getDto(self):
        return self.getService()._dto_class
        
    
    def getDao(self):
        return self.getService()._dao
        
    
    def getService(self):
        return self._service
    

    def InsertItens(self, a_lst_dto : list):
        _tabela = self.getEntityType().get_table_name();
        _fields_tables, _fields_values = self.getDao()._sql_insert_fields()
    
        for _item in a_lst_dto:
            _values_map = convert_to_dumps(_item.convert_to_entity(self.getEntityType()))
            
            _sql = (
                "INSERT INTO " + _tabela + "(" + _fields_tables + 
                ") VALUES (" + _fields_values + ")"
            )

            getDb().execute(_sql, **_values_map)

        
    def UpInsertItens(self, a_lst_dto : list):
        """UpInsertItens é responsável por tentar inserir uma registro dentro de uma lista de registros
           caso a inserção não seja possível por conta de já haver um registor com mesma PK, a rotina
           se encarrega de atualizar o registro em questão""" 
        
        if not getVersaoMinimaAtendida():
            self.UpInsertItensOldPostgreSQL(a_lst_dto)
            return
        
        _fields_tables, _fields_values = self.getDao()._sql_insert_fields()         
        
        _entity = self.getEntityIstance()
        _fields_for_update = ','.join([
                    f"{k} = EXCLUDED.{k}"
                    for k in _entity.__dict__
                        if not callable(getattr(_entity, k, None)) and not k.startswith("_") and (k != _entity.get_pk_field())
                ])
        

        for _item in a_lst_dto:
            _values_map = convert_to_dumps(_item.convert_to_entity(self.getEntityType()))
            
            _sql = f"""
                INSERT INTO {_entity.get_table_name()} ( {_fields_tables} ) 
                VALUES ({_fields_values})
                ON CONFLICT ({_entity.get_pk_field()}) 
                DO UPDATE SET
                {_fields_for_update}
            """

            getDb().execute(_sql, **_values_map)


    def UpInsertItensOldPostgreSQL(self, a_lst_dto : list):
        """UpInsertItensOldPostgreSQL é usada quando a versão do postgres não
        é compatível com uma versão mínimo necessária que contenha o recurso
        'ON CONFLICT' para o comando insert""" 
        
        _fields_tables, _fields_values = self.getDao()._sql_insert_fields()        
        _entity = self.getEntityIstance()
        
        for _item in a_lst_dto:
            _values_map = convert_to_dumps(_item.convert_to_entity(self.getEntityType()))
            
            _sql = f"""
                INSERT INTO {_entity.get_table_name()} ( {_fields_tables} ) 
                SELECT {_fields_values}
                WHERE NOT EXISTS (SELECT 1 FROM {_entity.get_table_name()} 
                                    WHERE {_entity.get_pk_field()} = '{_values_map[_entity.get_pk_field()]}')
            """

            if getDb().execute(_sql, **_values_map)[0] == 0:
                self._service.update(dto=_item, id=_values_map[_entity.get_pk_field()])