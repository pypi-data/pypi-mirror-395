from scorb_api.models.endpoint import Endpoint
import asyncio

class TabelaCustomizadaGlobais(Endpoint):
    def __init__(self, header_auth) -> None:
        super().__init__(header_auth=header_auth)
        self.base_url = "/api/SCORC/crud/TabelaCustomizada"
         

    def read(self):
        return asyncio.run(self.http_request.request(f"{self.base_url}/read", "post", headers=self.header_auth))  



["CalculoAlcance",
"CalculoAlcanceVerbaDependencia",
"Cargo",
"CenarioVisao",
"CentroCusto",
"CentroCustoVerbaValorReal",
"ContaContabil",
"Cotacao",
"DiasUteis",
"ExpressaoCustomizada",
"FaixaSalarialAlcance",
"FaixaSalarialEsquema",
"FaixaSalarialEsquemaItem",
"FaixaSalarialReajusteAlcance",
"FuncaoCustomizada",
"Funcionario",
"FuncionarioAlocacao",
"FuncionarioPlano",
"FuncionarioSalarioPrevisto",
"FuncionarioTipo",
"FuncionarioVerbaEspecifica",
"GrupoCargo",
"GrupoCentroCusto",
"GrupoEmpregado",
"GrupoNivelSalarial",
"GrupoVerba",
"Moeda",
"NivelSalarial",
"Plano",
"PlanoContas",
"Posicao",
"ReajusteAlcance",
"ReajusteAlcanceMotivo",
"ReportCalculatedField",
"Verba",
"VerbaCategoria",
"VerbaCentroCustoDepara",
"VerbaContaContabilAlcance",
"VerbaReajusteContaContabil",]