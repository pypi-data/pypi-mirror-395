from scorb_api.models.endpoint import Endpoint
from typing import Union
import asyncio
from scorb_api.models.endpoints.task_request import TaskRequest


class Inventarios(Endpoint):
    def __init__(self, header_auth, cenario_code: str, model: str) -> None:
        super().__init__(header_auth=header_auth)
        self.base_url = f"/api/SCORC/inventory/cenario/{cenario_code}/{model}"

    def read(self):
        return asyncio.run(self.http_request.request(f"{self.base_url}/read", "post", headers=self.header_auth))

    def load(self, body: Union[dict, list[dict]]):
        """Method to bulk load records to inventory model

		To use this method, you need the following permissions:
		- Required permission: "Carga de Dados"

		Args:
			body (Union[dict, list[dict]], mandatory): Body object to send on request
		
		Examples:
			```python
			from scorb_api import ScorbApiClient


			client = ScorbApiClient(company="Company Name", app_name="app_name")
			result = (
				client.inventarios()
				.inventario(cenario_code="code", model="inventory model name")
				.load(body={"field_1": "value", "field_2": "value"})
			)
			```
		"""
        result = asyncio.run(
			self.http_request.request(
				self.base_url, "post",
				headers=self.header_auth,
				json=body
			)
		)

        return TaskRequest(
			header_auth=self.header_auth,
			token=result.get("token"),
			result=result.get("result")
		)
