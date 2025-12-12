import uuid
from datetime import time

from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.dto.dto_base import DTOBase

@DTO()
class RotinaAutomatizadaDto(DTOBase):
    rotina : uuid.UUID = DTOField(resume=True, pk=True, not_null=True, use_default_validator=False)
    codigo : str = DTOField(resume=True, strip=True, min=1, max=30)
    descricao : str = DTOField(resume=True, strip=True, min=0, max=250)
    processacalculo : bool = DTOField(resume=True, default_value=False)
    parametroprocessamentocalculo : str = DTOField(resume=True, strip=True)
    sincronizaesocial : bool = DTOField(resume=True, default_value=False)
    parametrosincronizacaoesocial : str = DTOField(resume=True, strip=True)
    #gerarelatorio : bool = DTOField(resume=True, default_value=False)
    #parametrogeracaorelatorio : str = DTOField(resume=True, strip=True)

    def __init__(self, entity: any = None, **kwargs):
        super().__init__(entity=entity, kwargs=kwargs)
        
