from scorb_api.models.endpoint import Endpoint
import asyncio

class ResumoHCeSalarioCCeEmpresa(Endpoint):
    def __init__(self, header_auth) -> None:
        super().__init__(header_auth=header_auth)
        self.base_url = "/api/SCORC/crud/Resumo HC _ Salário _CC e Empresa_"
         

    def read(self, body):
        return asyncio.run(self.http_request.request(f"{self.base_url}/read", "post", headers=self.header_auth, json=body))  

