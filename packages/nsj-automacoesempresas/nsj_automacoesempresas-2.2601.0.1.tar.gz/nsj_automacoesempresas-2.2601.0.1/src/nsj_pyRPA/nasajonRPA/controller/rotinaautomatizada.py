from nsj_pyRPA.nasajonRPA.controller import controllerBase
from nsj_pyRPA.nasajonRPA.dto.rotinaautomatizada import RotinaAutomatizadaDto
from nsj_pyRPA.nasajonRPA.entity.rotinaautomatizada import RotinaAutomatizadaEntity

class RotinaAutomatizadaController(controllerBase.ControllerBase):
    def getEntityType(self):
        return RotinaAutomatizadaEntity
    
    def getDTOType(self):
        return RotinaAutomatizadaDto
    
    
def RecuperaRotinaAutomatizada(a_codigo : str) -> RotinaAutomatizadaDto:
    _filtro = {}
    _filtro.update({"codigo": a_codigo})

    if len(_filtro) == 0:
        _filtro = None

    _controller = RotinaAutomatizadaController()
    _lst = _controller.getService().list(after=None,
                                         limit=2,
                                         fields={"root" : _controller.getDTOType().resume_fields},
                                         filters=_filtro,
                                         order_fields=None)        
    if len(_lst) == 1:
        return _lst[0]
    if len(_lst) == 2:
        raise Exception("Mais de uma configuração de rotina automatizada foi encontrada.")    
    else:        
        raise Exception("Não foi localizada configuração de rotina automatizada.")