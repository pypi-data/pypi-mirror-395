
from scorb_api.models.endpoints import Globais
from scorb_api.models.endpoints import EntidadesDeCenario
from scorb_api.models.endpoints import TabelasCustomizadas
from scorb_api.models.endpoints import EntidadesCustomizadas
from scorb_api.models.endpoints import Reports
from scorb_api.models.endpoints import Inventario


"""This module provides the main client class for the Scorb API."""

from scorb_api.models.authorization import Authorization

class ScorbApiClient:
    """
    The main client class for the Scorb API.
    This class provides a client to interact with the Scorb API.
    It provides methods to authenticate, get and set services required by the endpoints,
    and get an endpoint instance by name.
    """
    def __init__( self, company: str, app_name:str) -> None:
        self.header_auth = Authorization(company=company, app_name=app_name).generate_authorization_header()

    def globais(self)-> Globais:
        return Globais(self.header_auth)
    
    def entidades_de_cenario(self)-> EntidadesDeCenario:
        return EntidadesDeCenario(self.header_auth)
    
    def entidades_customizadas(self)-> EntidadesCustomizadas:
        return EntidadesCustomizadas(self.header_auth)
    
    def tabelas_customizadas(self)-> TabelasCustomizadas:
        return TabelasCustomizadas(self.header_auth)

    def inventarios(self) -> Inventario:
        return Inventario(self.header_auth)
    
    def reports(self)-> Reports:
        return Reports(self.header_auth)
    
__doc__ = """
**ScorbApiClient** is a python package to providing
methods to use Scorb rest api.
"""

